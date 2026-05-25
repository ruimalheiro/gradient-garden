import torch
import math

from inference.runtime import InferenceRuntime
from config import GlobalConfig, TrainingStage
from engine.dataloaders import init_data_loaders
from tqdm import tqdm


def get_dataloader_root_path(config):
    datasets_paths = config.paths.datasets
    if config.training.stage == TrainingStage.PRETRAINING:
        return datasets_paths.pretraining_path
    elif config.training.stage == TrainingStage.INSTRUCT:
        return datasets_paths.instruct_path
    elif config.training.stage == TrainingStage.DPO:
        return datasets_paths.dpo_path
    else:
        raise ValueError('No valid dataloader root path')

@torch.inference_mode()
def evaluate_validation_ppl(
    inference_runtime: InferenceRuntime,
    config: GlobalConfig,
    batch_size: int,
    validation_steps: int,
    ignore_index: int
):
    model = inference_runtime.model
    device = inference_runtime.device

    _, val_loader = init_data_loaders(
        batch_size=batch_size,
        sequence_length=config.model.max_seq_len,
        is_master_process=True,
        ddp_rank=0,
        ddp_world_size=1,
        data_root=get_dataloader_root_path(config),
        pad_id=inference_runtime.tokenizer.pad_id,
        training_stage=config.training.stage,
        number_of_cpu_processes=config.runtime.number_of_cpu_processes,
        ignore_index=config.tokenizer.ignore_index,
        validation_only=True
    )

    model.eval()

    loss_sum = 0.0
    tokens_sum = 0

    for step in tqdm(range(validation_steps), 'Validating'):
        x, y = val_loader.next_batch()

        x = x.to(device, non_blocking=True)
        y = y.to(device, non_blocking=True)

        loss = model(x, labels=y)['loss'].item()
        n_valid = ((y != ignore_index).sum().float()).item()
        if n_valid == 0:
            continue

        loss_sum += loss * n_valid
        tokens_sum += n_valid

    if tokens_sum == 0:
        raise RuntimeError('No valid tokens found during validation.')

    val_loss = loss_sum / tokens_sum
    perplexity = math.exp(val_loss)

    return {
        'mean_cross_entropy_loss': val_loss,
        'perplexity': perplexity,
        'total_cross_entropy_loss': loss_sum,
        'total_valid_tokens': tokens_sum,
        'steps': validation_steps,
        'batch_size': batch_size,
        'sequence_length': config.model.max_seq_len,
    }
