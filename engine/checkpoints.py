import torch
import os
import torch.distributed as dist
import json
import math

from collections import OrderedDict
from torch.distributed.checkpoint.state_dict import (
    get_model_state_dict,
    get_optimizer_state_dict,
    set_model_state_dict,
    set_optimizer_state_dict,
    StateDictOptions
)
from logger import logger
from dataclasses import dataclass, field
from typing import Any
from config import GlobalConfig, ModelConfig, HFModelConfig, TokenizerPromptFormat


def state_to_cpu(obj):
    # helper to move items from the state to cpu to avoid using more vram
    if torch.is_tensor(obj):
        return obj.cpu()
    if isinstance(obj, dict):
        return {k: state_to_cpu(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        t = type(obj)
        return t(state_to_cpu(v) for v in obj)
    return obj

def manage_checkpoints(directory, max_files, step, pbar=None):
    # List all checkpoint files
    checkpoints = [os.path.join(directory, file) for file in os.listdir(directory) if file.startswith('model_')]
    # Extract steps from filenames and pair them
    steps_files = [(int(file.split('_')[-1].split('.')[0]), file) for file in checkpoints]
    # Sort list by step numbers
    steps_files.sort()

    # save only the last max_files checkpoints- This is to avoid running out of disk space
    if len(steps_files) > max_files:
        cutoff_index = max(0, len(steps_files) - max_files)
        cutoff_step = steps_files[cutoff_index][0]

        # Delete files
        for prev_step, file in steps_files:
            if prev_step < cutoff_step:
                os.remove(file)
                logger.info(f'{step:4d} | deleted old checkpoint: {file}', pbar=pbar)

def save_checkpoint(
    checkpoint_dir,
    model,
    config,
    step,
    last_val_loss,
    best_val_loss,
    optimizers,
    train_loader,
    val_loader,
    extra_metadata,
    max_number_checkpoints,
    is_master_process,
    pbar=None
):
    optimizer_state = {'adamw': None, 'muon': None}
    if dist.is_initialized():
        # ensures we materialize both model / optimizers fully before we attempt to save
        options = StateDictOptions(full_state_dict=True, cpu_offload=True)
        dist.barrier()
        model_state_dict = get_model_state_dict(model, options=options)

        if optimizers.adamw:
            optimizer_state['adamw'] = get_optimizer_state_dict(model, optimizers.adamw, options=options)
        if optimizers.muon:
            optimizer_state['muon'] = get_optimizer_state_dict(model, optimizers.muon, options=options)

        dist.barrier() # we need all ranks to be sync and participate in the above
    else:
        model_state_dict = model.state_dict()

        if optimizers.adamw:
            optimizer_state['adamw'] = optimizers.adamw.state_dict()
        if optimizers.muon:
            optimizer_state['muon'] = optimizers.muon.state_dict()

    model_state_dict = state_to_cpu(model_state_dict)

    if optimizer_state['adamw']:
        optimizer_state['adamw'] = state_to_cpu(optimizer_state['adamw'])
    if optimizer_state['muon']:
        optimizer_state['muon'] = state_to_cpu(optimizer_state['muon'])

    if is_master_process:
        checkpoint_path = os.path.join(checkpoint_dir, f'model_{step}.pt')
        os.makedirs(checkpoint_dir, exist_ok=True)

        checkpoint = {
            'model': model_state_dict,
            'step': step,
            'config': config.model_dump(mode='json'),
            'optimizers': optimizer_state,
            'last_val_loss': float(last_val_loss),
            'best_val_loss': float(best_val_loss),
            'train_dl': train_loader.state_dict(),
            'val_dl': val_loader.state_dict(),
            'metadata': extra_metadata
        }

        torch.save(checkpoint, checkpoint_path)
        logger.info(f'{step:4d} | saved checkpoint: {checkpoint_path}', pbar=pbar)

        manage_checkpoints(directory=checkpoint_dir, max_files=max_number_checkpoints, step=step, pbar=pbar)

@dataclass
class CheckpointData:
    file_path: str | None = None
    model_state: dict[str, Any] | None = None
    optimizers_state: dict[str, Any] | None = None
    resume_step: int = 0
    last_val_loss: float = float('inf')
    best_val_loss: float = float('inf')
    train_loader_state: Any = None
    val_loader_state: Any = None
    is_lora_checkpoint: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            'file_path': self.file_path,
            'resume_step': self.resume_step,
            'last_val_loss': self.last_val_loss if not math.isinf(self.last_val_loss) else None,
            'best_val_loss': self.best_val_loss if not math.isinf(self.best_val_loss) else None,
            'is_lora_checkpoint': self.is_lora_checkpoint,
            'metadata': self.metadata
        }

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

def load_checkpoint(file_path) -> CheckpointData:
    state = torch.load(file_path, map_location='cpu', weights_only=True)

    step = state['step'] + 1
    last_val_loss = state['last_val_loss'] if state['last_val_loss'] is not None else float('inf')
    best_val_loss = state['best_val_loss'] if state['best_val_loss'] is not None else float('inf')

    model_state = state['model']
    assert type(model_state) in {OrderedDict, dict}

    optimizers_state = state['optimizers']
    if optimizers_state['adamw']:
        assert type(optimizers_state['adamw']) == dict
    if optimizers_state['muon']:
        assert type(optimizers_state['muon']) == dict

    train_dl_state = state.get('train_dl', None)
    val_dl_state = state.get('val_dl',   None)

    metadata = state.get('metadata', {})

    logger.section('Model checkpoint loading')
    logger.info(f'model state loaded from checkpoint file: "{file_path}"')
    if optimizers_state is not None:
        logger.info(f'optimizers state loaded from checkpoint')
        if optimizers_state['adamw']:
            logger.info('-- loaded state for adamW')
        if optimizers_state['muon']:
            logger.info('-- loaded state for Muon')

    if train_dl_state is not None and val_dl_state is not None:
        logger.info('Dataloaders state loaded')
        _valid_keys = ['current_shard', 'current_position', 'epoch']

        logger.info('--Train Loader state:')
        logger.info({key: train_dl_state[key] for key in _valid_keys if key in train_dl_state})

        logger.info('--Val Loader state:')
        logger.info({key: val_dl_state[key] for key in _valid_keys if key in val_dl_state})

    logger.section('Loaded config')
    logger.info(state['config'], is_json=True)

    if step > 0:
        logger.info(f'\nResuming from step: {step}')
    else:
        logger.info(f'\nStarting from step: 0')
    logger.info(f'Last calculated loss: {last_val_loss:.4f}')
    logger.info(f'Last calculated best loss: {best_val_loss:.4f}')

    logger.info('\nExtra metadata stored in the checkpoint:')
    logger.info(metadata, is_json=True)
    
    # Delete large state file to free memory
    del state
    if torch.cuda.is_available():
        logger.info('\nClearing cuda cache...\n')
        torch.cuda.empty_cache()

    return CheckpointData(
        file_path=file_path,
        model_state=model_state,
        optimizers_state=optimizers_state,
        resume_step=step,
        last_val_loss=last_val_loss,
        best_val_loss=best_val_loss,
        train_loader_state=train_dl_state,
        val_loader_state=val_dl_state,
        is_lora_checkpoint=metadata.get('lora_enabled', False),
        metadata=metadata
    )

@dataclass
class BaseCheckpointDataInference:
    pass

@dataclass
class CheckpointDataInference(BaseCheckpointDataInference):
    file_path: str
    config: GlobalConfig
    model_state: dict[str, Any]
    step: int
    is_lora_checkpoint: bool = False
    metadata: dict = field(default_factory=dict)
    is_hf_direct_load: bool = False

    def to_dict(self):
        return {
            'file_path': self.file_path,
            'config': self.config,
            'step': self.step,
            'is_lora_checkpoint': self.is_lora_checkpoint,
            'metadata': self.metadata,
            'is_hf_direct_load': self.is_hf_direct_load
        }

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

@dataclass
class HFCheckpointDataInference(BaseCheckpointDataInference):
    config: GlobalConfig
    is_hf_direct_load: bool = True

    def to_dict(self):
        return {
            'config': self.config,
            'is_hf_direct_load': self.is_hf_direct_load
        }

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

def load_checkpoint_for_inference(file_path) -> CheckpointDataInference:
    state = torch.load(file_path, map_location='cpu', weights_only=True)

    config = state['config']
    model_state = state['model']
    step = state['step']
    metadata = state.get('metadata', {})

    del state

    return CheckpointDataInference(
        file_path=file_path,
        config=GlobalConfig.model_validate(config),
        model_state=model_state,
        step=step,
        is_lora_checkpoint=metadata.get('lora_enabled', False),
        metadata=metadata
    )

def load_shallow_hf_checkpoint_for_inference(hf_checkpoint_path: str, *, system_prompt='You are a helpful AI assistant.') -> HFCheckpointDataInference:
    # The purpose of this function is just to prepare the config abstraction.
    config = GlobalConfig()
    config.model = ModelConfig()
    config.model.architecture = 'hf_wrapper'
    config.model.hf_config = HFModelConfig()
    config.model.hf_config.model_name = hf_checkpoint_path
    config.prompts.system_prompt = system_prompt
    config.tokenizer.checkpoint_path = hf_checkpoint_path
    config.tokenizer.prompt_format = TokenizerPromptFormat.HF_CHAT_TEMPLATE

    return HFCheckpointDataInference(config=GlobalConfig.model_validate(config))

def load_model_state(model, checkpoint_state_dict):
    if dist.is_initialized():
        options = StateDictOptions(full_state_dict=True)
        set_model_state_dict(
            model=model,
            model_state_dict=checkpoint_state_dict,
            options=options
        )
    else:
        model.load_state_dict(checkpoint_state_dict)

def load_optimizer_state(optimizer, model, checkpoint_state_dict):
    if dist.is_initialized():
        options = StateDictOptions(full_state_dict=True)
        set_optimizer_state_dict(
            model=model,
            optimizers=optimizer,
            optim_state_dict=checkpoint_state_dict,
            options=options
        )
    else:
        optimizer.load_state_dict(checkpoint_state_dict)
