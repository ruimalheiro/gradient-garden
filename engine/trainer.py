import math
import torch
import torch.distributed as dist

from collections.abc import Callable
from torch.distributed import (
    destroy_process_group,
    broadcast
)
from torch.distributed.tensor import DTensor
from torch.distributed.fsdp import MixedPrecisionPolicy
from torch.nn.utils import clip_grad_norm_
from tqdm.auto import tqdm
from pathlib import Path
from logger import logger
from config import (
    DeviceType,
    TrainingStage,
    TrainingPrecision,
    ModelArchitecture
)
from engine.context import (
    DistributedContext,
    DeviceContext,
    PrecisionContext,
    TrainerContext,
    RunContext
)
from engine.core import (
    TrainerState
)
from engine.optim import (
    classify_trainable_parameters,
    build_optimizer_plan,
    build_optimizers,
    move_optimizer_state_to_param_device
)
from engine.logging import (
    prepare_workload_summary,
    prepare_train_step_log,
    prepare_val_step_log,
    prepare_val_step_no_improve_log,
    prepare_multiple_choice_eval_log,
    prepare_generation_eval_log
)
from engine.torch_profiler import (
    init_torch_profiler_context
)
from engine.snapshot import create_run_snapshot
from engine.distributed import (
    init_multi_gpu,
    prepare_model_for_ddp,
    prepare_model_for_fsdp,
    get_model
)
from engine.dataloaders.dataloader import init_data_loaders
from engine.checkpoints import (
    save_checkpoint,
    load_checkpoint,
    load_model_state,
    load_optimizer_state
)
from engine.wandb import WandbWrapper
from engine.lr_schedulers import (
    cosine_scheduler,
    wsd_scheduler
)
from engine.generation_prompts import resolve_generation_test_prompts
from tokenization.tokenizer import init_tokenizer
from models.registry import build_model
from models.adapters.lora import (
    apply_lora,
    freeze_non_lora_parameters
)
from tasks.factory import get_task
from metrics.memory import (
    reset_memory_usage_metrics,
    compute_memory_usage_metrics
)
from metrics.aggregation import (
    accumulate_weighted_metrics,
    combine_weighted_metrics
)
from metrics.step import (
    StepType,
    StepMetrics
)
from metrics.model_specific import collect_model_specific_metrics
from inference.generation import generate_and_decode
from evals.multiple_choice import (
    load_multiple_choice_eval_file,
    estimate_best_candidate_index_from_logits
)
from evals.ifeval.ifeval import (
    load_ifeval_eval_file,
    score_ifeval_example
)
from evals.custom_sft_smoke.custom_sft_smoke import (
    load_custom_sft_smoke_eval_file,
    score_custom_sft_smoke_example
)
from utils import (
    generate_name,
    set_seed,
    get_architecture_name
)


class Trainer:
    def __init__(self, config, args):
        self.config = config
        self.args = args
        self.trainer_state = TrainerState()
        self.distributed_ctx = None
        self.device_ctx = None
        self.precision_ctx = None
        self.trainer_ctx = None
        self.run_ctx = None
        self.hellaswag_data = None
        self.winogrande_data = None
        self.arc_challenge_data = None
        self.ifeval_no_external_data = None
        self.custom_sft_smoke_data = None
        self.test_generation_prompts = None
        self.tokenizer = None
        self.model = None
        self.train_loader = None
        self.val_loader = None
        self.checkpoint_data = None
        self.task = None
        self.task_assets = None
        self.optimizer_plan = None
        self.optimizers = None
        self.workload_summary = None
        self.wandb = None
        self.torch_profiler_context = None

        self.validate_common_config()

    def validate_training_asset_exists(self, path):
        training_path = Path(path)
        if not training_path.exists():
            raise FileNotFoundError(f'Training dataset path does not exist: {training_path}. Please run `prepare_datasets.py` first to build the assets.')
        training_split = training_path / 'train'
        if not training_split.exists():
            raise FileNotFoundError(f'Training dataset path does not contain the "train" split: {training_path}. Please run `prepare_datasets.py` first to build the assets.')
        validation_split = training_path / 'val'
        if not validation_split.exists():
            raise FileNotFoundError(f'Training dataset path does not contain the "val" split: {training_path}. Please run `prepare_datasets.py` first to build the assets.')

    def validate_eval_asset_exists(self, path):
        asset_path = Path(path)
        if not asset_path.exists():
            raise FileNotFoundError(f'Eval dataset path does not exist: {asset_path}. Please run `prepare_datasets.py` first to build the assets.')
        asset_data_path = asset_path / self.config.paths.evals.data_filename
        if not asset_data_path.exists():
            raise FileNotFoundError(
                f'Eval dataset path does not contain "{self.config.paths.evals.data_filename}": '
                f'{asset_path}. Please run `prepare_datasets.py` first to build the assets.'
            )

    def validate_common_config(self):
        config = self.config

        # device type
        if self.config.runtime.device_type != DeviceType.CUDA:
            raise ValueError('Only cuda is supported at the moment.')

        # validate assets exist
        self.validate_training_asset_exists(self.config.paths.datasets.training_path)
        if self.can_run_scheduled_action(self.config.evals.hellaswag):
            self.validate_eval_asset_exists(self.config.paths.evals.hellaswag_path)
        if self.can_run_scheduled_action(self.config.evals.winogrande):
            self.validate_eval_asset_exists(self.config.paths.evals.winogrande_path)
        if self.can_run_scheduled_action(self.config.evals.arc_challenge):
            self.validate_eval_asset_exists(self.config.paths.evals.arc_challenge_path)
        if self.can_run_scheduled_action(self.config.evals.ifeval_no_external):
            self.validate_eval_asset_exists(self.config.paths.evals.ifeval_no_external_path)
        if self.can_run_scheduled_action(self.config.evals.custom_sft_smoke):
            self.validate_eval_asset_exists(self.config.paths.evals.custom_sft_smoke_path)

    def setup(self):
        self.set_seed()
        self.resolve_config_overrides()
        self.setup_global_torch_optimizations()
        self.build_contexts()
        self.setup_local_logging()
        self.log_distributed_context()
        self.build_components()
        self.load_assets()
        self.resolve_checkpoint()
        self.resolve_apply_lora()
        self.build_task()
        self.prepare_model_for_distributed_context()
        self.move_task_assets_to_device()
        self.build_optimizer_plan()
        self.build_optimizers()
        self.resolve_optimizers_checkpoint()
        self.prepare_runtime()
        self.prepare_workload_summary_json()
        self.log_workload_summary()
        self.save_run_snapshot()
        self.check_all_devices_ready()
        self.setup_wandb()
        self.setup_torch_profiler()

    def set_seed(self):
        set_seed(self.config.training.seed)

    def resolve_config_overrides(self):
        override_messages = []
        if self.args.micro_batch_size is not None:
            override_messages.append(
                f'Overriding config.training.micro_batch_size "{self.config.training.micro_batch_size}" '
                f'with "{self.args.micro_batch_size}".'
            )
            self.config.training.micro_batch_size = self.args.micro_batch_size

        if override_messages:
            logger.section('Config overrides', force=True)
            for message in override_messages:
                logger.warning(message, force=True)
            logger.info('\n', force=True)

    def setup_global_torch_optimizations(self):
        torch.backends.cuda.matmul.fp32_precision = 'tf32'
        torch.backends.cudnn.conv.fp32_precision = 'tf32'
        torch.backends.cuda.enable_cudnn_sdp(True)

    def build_contexts(self):
        device = self.build_distributed_context()
        self.build_device_context(device)
        self.build_precision_context()
        self.build_trainer_context()
        self.build_run_context()

    def get_run_output_dir_path(self):
        return (
            Path(self.config.paths.runs.output_dir_path) /
            self.config.training.stage.value /
            get_architecture_name(self.config) /
            self.run_ctx.name
        )

    def get_checkpoints_dir_path(self):
        return self.get_run_output_dir_path() / 'checkpoints'

    def get_best_checkpoints_dir_path(self):
        return self.get_run_output_dir_path() / 'checkpoints' / 'best'

    def get_snapshots_dir_path(self):
        return self.get_run_output_dir_path() / 'snapshots'

    def get_local_logs_dir_path(self):
        return self.get_run_output_dir_path() / 'logs'

    def load_eval_assets(self):
        self.load_hellaswag_eval_data()
        self.load_winogrande_eval_data()
        self.load_arc_challenge_eval_data()
        self.load_ifeval_no_external_eval_data()
        self.load_custom_sft_smoke_eval_data()

    def load_generation_assets(self):
        self.load_test_generation_prompts()

    def build_components(self):
        self.build_tokenizer()
        self.build_model()
        self.build_data_loaders()

    def load_assets(self):
        self.load_eval_assets()
        self.load_generation_assets()

    def resolve_checkpoint(self):
        checkpoint_req = self.resolve_checkpoint_request()
        if checkpoint_req:
            self.load_checkpoint_data(checkpoint_req)
            self.apply_lora_for_checkpoint()
            self.restore_model_state()
            self.restore_data_loaders_state()

    def build_task(self):
        self.task = get_task(self.config.training.stage)
        self.task.setup(config=self.config, ctx=self.trainer_ctx)
        self.task_assets = self.task.build_assets(tokenizer=self.tokenizer, model=self.model)

    def build_distributed_context(self):
        ddp, ddp_rank, ddp_local_rank, ddp_world_size, is_master_process, device = init_multi_gpu(self.config.runtime.device_type.value)
        self.distributed_ctx = DistributedContext(
            ddp=ddp,
            ddp_rank=ddp_rank,
            ddp_local_rank=ddp_local_rank,
            ddp_world_size=ddp_world_size,
            use_fsdp=self.config.runtime.use_fsdp,
            is_master_process=is_master_process
        )
        return device

    def build_device_context(self, device):
        self.device_ctx = DeviceContext(
            device_type=self.config.runtime.device_type.value,
            device=device
        )

    def setup_local_logging(self):
        logger.set_master(self.distributed_ctx.is_master_process)
        if not self.distributed_ctx.is_master_process or not self.config.logging.write_to_file:
            return
        log_file_path = self.get_local_logs_dir_path() / self.run_ctx.name
        logger.info(f'Logging to: {log_file_path}')
        logger.set_log_file_path(log_file_path)

    def log_distributed_context(self):
        device_type = self.config.runtime.device_type.value
        ddp_rank = self.distributed_ctx.ddp_rank
        ddp_local_rank = self.distributed_ctx.ddp_local_rank
        ddp_world_size = self.distributed_ctx.ddp_world_size

        logger.section('Device setup')
        logger.info(f'Using device type: {device_type}')
        if ddp_rank:
            logger.info(f'DDP rank: {ddp_rank}')
        if ddp_local_rank:
            logger.info(f'DDP local rank: {ddp_local_rank}')
        if ddp_world_size:
            logger.info(f'DDP world size: {ddp_world_size}')

    def build_precision_context(self):
        if self.config.runtime.training_precision == TrainingPrecision.BF16:
            self.precision_ctx = PrecisionContext(
                use_autocast=True,
                scaler=None,
                model_dtype=torch.float32,
                autocast_dtype=torch.bfloat16,
                fsdp_mp=MixedPrecisionPolicy(
                    param_dtype=torch.bfloat16,
                    reduce_dtype=torch.float32
                ) if self.config.runtime.use_fsdp else None
            )
        elif self.config.runtime.training_precision == TrainingPrecision.FP16:
            self.precision_ctx = PrecisionContext(
                use_autocast=True,
                scaler=torch.amp.GradScaler(self.device_ctx.device_type), # need gradscaler when fp16
                model_dtype=torch.float32,
                autocast_dtype=torch.float16,
                fsdp_mp=MixedPrecisionPolicy(
                    param_dtype=torch.float16,
                    reduce_dtype=torch.float32
                ) if self.config.runtime.use_fsdp else None
            )
        elif self.config.runtime.training_precision == TrainingPrecision.FP32:
            self.precision_ctx = PrecisionContext(
                use_autocast=False,
                scaler=None,
                model_dtype=torch.float32,
                autocast_dtype=torch.float32,
                fsdp_mp=None
            )
        else:
            raise ValueError('Invalid training precision')

    def compute_grad_accum_steps(self, ddp_world_size):
        micro_batch_size = self.config.training.micro_batch_size
        #### BATCH SIZE CHECKS (For now assumes token based autoregressive training...)
        # NOTE: total_batch_size is the total batch size in tokens. The micro_batch_size is the number of sequences per device during forward pass (micro batches).
        # The total batch size must be a multiple of (micro_batch_size * max_seq_len * ddp_world_size). This is needed for the gradient accumulation steps to be calculated correctly.
        if self.config.training.total_batch_size % (micro_batch_size * self.config.model.max_seq_len * ddp_world_size) != 0:
            raise ValueError('total_batch_size must be divisible by (micro_batch_size * max_seq_len * ddp_world_size)')

        # Gradient accumulation steps
        grad_accum_steps = self.config.training.total_batch_size // (micro_batch_size * self.config.model.max_seq_len * ddp_world_size)

        # Final check to validate previous calculations.
        if self.config.training.total_batch_size != (micro_batch_size * self.config.model.max_seq_len * ddp_world_size * grad_accum_steps):
            raise ValueError('total batch size MUST EQUAL (micro_batch_size * max_seq_len * ddp_world_size * grad_accum_steps)')

        return grad_accum_steps

    def build_trainer_context(self):
        self.trainer_ctx = TrainerContext(
            distributed=self.distributed_ctx,
            device=self.device_ctx,
            precision=self.precision_ctx,
            grad_accum_steps=self.compute_grad_accum_steps(self.distributed_ctx.ddp_world_size)
        )

    def build_run_context(self):
        dist_buffer = [None]

        if self.distributed_ctx.is_master_process:
            name, timestamp = generate_name(name=self.config.run.name)
            dist_buffer[0] = {
                'name': name,
                'timestamp': timestamp
            }

        if self.distributed_ctx.ddp and dist.is_initialized():
            dist.broadcast_object_list(dist_buffer, src=0)

        self.run_ctx = RunContext(
            name=dist_buffer[0]['name'],
            timestamp=dist_buffer[0]['timestamp']
        )

    def load_test_generation_prompts(self):
        if not self.can_run_scheduled_action(self.config.generation):
            return
        self.test_generation_prompts = resolve_generation_test_prompts(self.config)

    def can_run_scheduled_action(self, schedule):
        return (
            schedule.every_x_steps > 0 or
            schedule.run_on_first_step or
            schedule.run_on_last_step
        )

    def load_hellaswag_eval_data(self):
        if not self.can_run_scheduled_action(self.config.evals.hellaswag):
            return
        self.hellaswag_data = load_multiple_choice_eval_file(
            filepath=f'{self.config.paths.evals.hellaswag_path}/{self.config.paths.evals.data_filename}',
            ddp=self.distributed_ctx.ddp,
            is_master_process=self.distributed_ctx.is_master_process,
            pad_token_id=self.tokenizer.pad_id,
            size=self.config.evals.hellaswag.number_of_examples
        )

    def load_winogrande_eval_data(self):
        if not self.can_run_scheduled_action(self.config.evals.winogrande):
            return
        self.winogrande_data = load_multiple_choice_eval_file(
            filepath=f'{self.config.paths.evals.winogrande_path}/{self.config.paths.evals.data_filename}',
            ddp=self.distributed_ctx.ddp,
            is_master_process=self.distributed_ctx.is_master_process,
            pad_token_id=self.tokenizer.pad_id,
            size=self.config.evals.winogrande.number_of_examples
        )

    def load_arc_challenge_eval_data(self):
        if not self.can_run_scheduled_action(self.config.evals.arc_challenge):
            return
        self.arc_challenge_data = load_multiple_choice_eval_file(
            filepath=f'{self.config.paths.evals.arc_challenge_path}/{self.config.paths.evals.data_filename}',
            ddp=self.distributed_ctx.ddp,
            is_master_process=self.distributed_ctx.is_master_process,
            pad_token_id=self.tokenizer.pad_id,
            size=self.config.evals.arc_challenge.number_of_examples
        )

    def load_ifeval_no_external_eval_data(self):
        if not (
            self.is_chat_stage() and
            self.can_run_scheduled_action(self.config.evals.ifeval_no_external)
        ):
            return
        self.ifeval_no_external_data = load_ifeval_eval_file(
            filepath=f'{self.config.paths.evals.ifeval_no_external_path}/{self.config.paths.evals.data_filename}',
            ddp=self.distributed_ctx.ddp,
            is_master_process=self.distributed_ctx.is_master_process,
            size=self.config.evals.ifeval_no_external.number_of_examples
        )

    def load_custom_sft_smoke_eval_data(self):
        if not (
            self.is_chat_stage() and
            self.can_run_scheduled_action(self.config.evals.custom_sft_smoke)
        ):
            return
        self.custom_sft_smoke_data = load_custom_sft_smoke_eval_file(
            filepath=f'{self.config.paths.evals.custom_sft_smoke_path}/{self.config.paths.evals.data_filename}',
            ddp=self.distributed_ctx.ddp,
            is_master_process=self.distributed_ctx.is_master_process,
            size=self.config.evals.custom_sft_smoke.number_of_examples
        )
    
    def build_tokenizer(self):
        self.tokenizer = init_tokenizer(
            path=self.config.tokenizer.checkpoint_path,
            system_prompt=self.config.prompts.system_prompt,
            is_huggingface_tokenizer=self.config.tokenizer.huggingface_tokenizer,
            hf_token=self.config.third_party.hf_token if self.config.tokenizer.huggingface_tokenizer else None
        )

    def build_model(self):
        self.model = build_model(
            config=self.config.model,
            pad_token_id=self.tokenizer.pad_id,
            vocab_size=self.tokenizer.vocab_size,
            ignore_index=self.config.tokenizer.ignore_index,
            hf_token=self.config.third_party.hf_token if self.config.tokenizer.huggingface_tokenizer else None
        )

    def is_pretraining(self):
        return self.config.training.stage == TrainingStage.PRETRAINING

    def is_instruct(self):
        return self.config.training.stage == TrainingStage.INSTRUCT

    def is_dpo(self):
        return self.config.training.stage == TrainingStage.DPO

    def is_chat_stage(self):
        return self.is_instruct() or self.is_dpo()

    def build_data_loaders(self):
        self.train_loader, self.val_loader = init_data_loaders(
            batch_size=self.config.training.micro_batch_size,
            sequence_length=self.config.model.max_seq_len,
            is_master_process=self.distributed_ctx.is_master_process,
            ddp_rank=self.distributed_ctx.ddp_rank,
            ddp_world_size=self.distributed_ctx.ddp_world_size,
            data_root=self.config.paths.datasets.training_path,
            pad_id=self.tokenizer.pad_id,
            training_stage=self.config.training.stage,
            number_of_cpu_processes=self.config.runtime.number_of_cpu_processes,
            ignore_index=self.config.tokenizer.ignore_index
        )

    def resolve_checkpoint_request(self):
        if self.args.checkpoint is None:
            return None

        checkpoint_file_path = Path(self.args.checkpoint)

        if not checkpoint_file_path.exists():
            raise FileNotFoundError(f'Checkpoint file does not exist: {checkpoint_file_path}')
        if not checkpoint_file_path.is_file():
            raise FileNotFoundError(f'Checkpoint path is not a file: {checkpoint_file_path}')

        return str(checkpoint_file_path)

    def load_checkpoint_data(self, checkpoint_file_path):
        args = self.args

        checkpoint_data = load_checkpoint(file_path=checkpoint_file_path)

        training_stage_changed = (
            checkpoint_data.metadata.get('training_stage', None) != self.config.training.stage.value
        )
        if training_stage_changed:
            logger.warning('Training stage has changed')
            if checkpoint_data.resume_step:
                logger.warning('ignoring stored resume step...')
                checkpoint_data.resume_step = 0

        ddp_world_size_changed = (
            checkpoint_data.metadata.get('ddp_world_size', None) != self.distributed_ctx.ddp_world_size
        )
        if ddp_world_size_changed:
            logger.warning('DDP world size has changed')

        lora_mode_changed = (
            self.config.lora.enabled and
            checkpoint_data is not None and
            not checkpoint_data.is_lora_checkpoint
        )
        if lora_mode_changed:
            logger.warning('LoRA enabled for non LoRA checkpoint')

        if args.reset_optimizers:
            logger.warning('Reset optimizers flag was set')

        if args.reset_dataloaders:
            logger.warning('Reset dataloaders flag was set')

        if ddp_world_size_changed or training_stage_changed or args.reset_dataloaders:
            if checkpoint_data.train_loader_state is not None and checkpoint_data.val_loader_state is not None:
                logger.warning('ignoring stored metadata for dataloaders...')
                checkpoint_data.train_loader_state = None
                checkpoint_data.val_loader_state = None

        reset_optimizer_state = training_stage_changed or args.reset_optimizers or lora_mode_changed
        if reset_optimizer_state:
            if checkpoint_data.optimizers_state is not None:
                logger.warning('ignoring stored state of optimizer(s)...')
                checkpoint_data.optimizers_state = None

        reset_validation_history = training_stage_changed or lora_mode_changed
        if reset_validation_history:
            if checkpoint_data.last_val_loss is not None or checkpoint_data.best_val_loss is not None:
                logger.warning('ignoring stored last val loss and best val loss...')
                checkpoint_data.last_val_loss = float('inf')
                checkpoint_data.best_val_loss = float('inf')
        
        self.checkpoint_data = checkpoint_data

    def apply_lora_modification(self):
        config = self.config

        supported = self.model.supported_lora_target_modules()
        if not supported:
            raise ValueError(f'Model architecture {self.config.model.architecture} does not expose LoRA target modules.')

        logger.section('LoRA Configuration')
        if self.config.lora.target_modules is None:
            target_modules = supported
            logger.warning(f'LoRA "target_modules" was not specified in the config. Using all supported: {supported}')
        elif len(self.config.lora.target_modules) == 0:
            raise ValueError('"lora.target_modules" cannot be empty.')
        else:
            requested = set(self.config.lora.target_modules)
            invalid = requested - supported
            if invalid:
                raise ValueError(
                    f'The provided LoRA target modules for {self.config.model.architecture} are invalid: {sorted(invalid)}. '
                    f'Supported target modules are: {sorted(supported)}'
                )
            target_modules = requested

        apply_lora(
            model=self.model,
            target_modules=target_modules,
            rank=config.lora.rank,
            alpha=config.lora.alpha,
            dropout=config.lora.dropout
        )
        # by default we freeze the other parameters
        freeze_non_lora_parameters(self.model)

        logger.info(f'- rank: {config.lora.rank}')
        logger.info(f'- alpha: {config.lora.alpha}')
        logger.info(f'- dropout: {config.lora.dropout}')
        logger.info(f'- target modules: {target_modules}')

    def apply_lora_for_checkpoint(self):
        if self.checkpoint_data.is_lora_checkpoint:
            if not self.config.lora.enabled:
                raise ValueError('"lora_enabled" must be set to True when loading checkpoint that includes LoRA')
            self.apply_lora_modification()

    def resolve_apply_lora(self):
        if (
            self.config.lora.enabled and
            (
                (not self.checkpoint_data) or
                (self.checkpoint_data and not self.checkpoint_data.is_lora_checkpoint)
            )
        ):
            self.apply_lora_modification()

    def restore_model_state(self):
        load_model_state(self.model, self.checkpoint_data.model_state)
        logger.section('Model loading')
        logger.info('Model checkpoint loaded and ready')

    def restore_data_loaders_state(self):
        checkpoint_data = self.checkpoint_data
        if checkpoint_data.train_loader_state is not None and checkpoint_data.val_loader_state is not None:
            self.train_loader.load_state_dict(checkpoint_data.train_loader_state)
            self.val_loader.load_state_dict(checkpoint_data.val_loader_state)

    def compile_model(self):
        if self.config.runtime.use_torch_compile:
            self.model.compile()

    def prepare_model_for_distributed_context(self):
        device = self.device_ctx.device
        ddp_local_rank = self.distributed_ctx.ddp_local_rank
        fsdp_mp = self.precision_ctx.fsdp_mp
        model_dtype = self.precision_ctx.model_dtype

        if self.config.runtime.use_fsdp:
            if not dist.is_initialized():
                raise ValueError('dist must be initialized if "config.runtime.use_fsdp" flag is set. Run with `torchrun` to force `dist` to initialize.')
            if self.config.runtime.use_torch_compile:
                raise ValueError('Currently not supporting torch compile for FSDP. Please set "config.runtime.use_torch_compile" flag to False.')
            logger.section('FSDP')
            logger.info('Wrapping the model in preparation for FSDP')
            # for FSDP no need to move explicitly to device here as that would actually cost more VRAM, instead let FSDP initialization alocate the shard to the device id (ddp_local_rank).
            self.model = prepare_model_for_fsdp(self.model, ddp_local_rank, fsdp_mp)
        else:
            # move to gpu
            self.model.to(device=device, dtype=model_dtype)
            if dist.is_initialized():
                logger.section('DDP')
                logger.info('Wrapping the model in preparation for DDP')
                self.model = prepare_model_for_ddp(self.model, ddp_local_rank)
            self.compile_model()

    def move_task_assets_to_device(self):
        self.task_assets = self.task.move_assets_to_device(self.task_assets)

    def build_optimizer_plan(self):
        parameter_buckets = classify_trainable_parameters(get_model(self.model))
        self.optimizer_plan = build_optimizer_plan(self.config, parameter_buckets)

    def build_optimizers(self):
        self.optimizers = build_optimizers(self.config, self.optimizer_plan)

    def resolve_optimizers_checkpoint(self):
        if not self.checkpoint_data or not self.checkpoint_data.optimizers_state:
            return
        if self.optimizers.adamw and self.checkpoint_data.optimizers_state['adamw']:
            load_optimizer_state(self.optimizers.adamw, get_model(self.model), self.checkpoint_data.optimizers_state['adamw'])
            move_optimizer_state_to_param_device(self.optimizers.adamw)
            logger.info('AdamW optimizer state loaded and ready')
        if self.optimizers.muon and self.checkpoint_data.optimizers_state['muon']:
            load_optimizer_state(self.optimizers.muon, get_model(self.model), self.checkpoint_data.optimizers_state['muon'])
            move_optimizer_state_to_param_device(self.optimizers.muon)
            logger.info('Muon optimizer state loaded and ready')

    def prepare_runtime(self):
        self.trainer_state.max_steps = self.config.training.max_steps
        if self.trainer_state.max_steps <= 0:
            self.trainer_state.max_steps = math.ceil(self.train_loader.calculate_max_tokens() / self.config.training.total_batch_size)
        if self.checkpoint_data:
            self.trainer_state.start_step = self.checkpoint_data.resume_step if self.args.start_step is None else self.args.start_step
            self.trainer_state.current_step = self.checkpoint_data.resume_step if self.args.start_step is None else self.args.start_step
            self.trainer_state.last_val_loss = self.checkpoint_data.last_val_loss
            self.trainer_state.best_val_loss = self.checkpoint_data.best_val_loss
        else:
            self.trainer_state.start_step = 0 if self.args.start_step is None else self.args.start_step
            self.trainer_state.current_step = 0 if self.args.start_step is None else self.args.start_step

    def prepare_workload_summary_json(self):
        train_loader_max_tokens = self.train_loader.calculate_max_tokens() # This is distributed
        if self.distributed_ctx.is_master_process:
            self.workload_summary = prepare_workload_summary(
                config=self.config,
                checkpoint_data=self.checkpoint_data,
                trainer_ctx=self.trainer_ctx,
                optimizer_plan=self.optimizer_plan,
                trainer_state=self.trainer_state,
                model_params_count=get_model(self.model).get_total_parameters_count(),
                model_trainable_params_count=get_model(self.model).get_trainable_parameters_count(),
                total_tokens=train_loader_max_tokens,
                test_generation_prompts=self.test_generation_prompts
            )

    def log_workload_summary(self):
        if self.distributed_ctx.is_master_process:
            logger.section(f'Workload summary for stage "{self.config.training.stage.value}"')
            logger.info(self.workload_summary, is_json=True)
            logger.separator()

    def save_run_snapshot(self):
        if self.distributed_ctx.is_master_process:
            create_run_snapshot(
                run_ctx=self.run_ctx,
                args=self.args,
                workload_summary=self.workload_summary,
                save_dir_path=self.get_snapshots_dir_path()
            )

    def setup_wandb(self):
        self.wandb = WandbWrapper(
            enabled=self.config.wandb.enabled,
            is_master_process=self.distributed_ctx.is_master_process,
            wandb_api_key=self.config.third_party.wandb_api_key
        )
        self.wandb.init(
            self.config.wandb.project_name,
            job_name=self.config.wandb.run_name if self.config.wandb.run_name else self.run_ctx.name,
            config=self.workload_summary,
            output_path=self.get_run_output_dir_path()
        )

    def setup_torch_profiler(self):
        self.torch_profiler_context = init_torch_profiler_context(
            self.config,
            self.distributed_ctx
        )

    def check_all_devices_ready(self):
        if self.distributed_ctx.ddp and dist.is_initialized():
            dist.barrier()
        logger.info(f'\nDevice: {self.distributed_ctx.ddp_local_rank} is ready.', force=True)

    def log_step_metrics(
        self,
        *,
        step_metrics,
        aggregated_metrics=None,
        model_specific_metrics=None,
        memory_usage_metrics=None,
        console_logs=None,
        pbar=None
    ):
        if not self.trainer_ctx.distributed.is_master_process:
            return
        if step_metrics.step_type == StepType.TRAIN:
            console_logs, wanb_log = prepare_train_step_log(
                step_metrics=step_metrics,
                trainer_state=self.trainer_state,
                aggregated_metrics=aggregated_metrics,
                memory_usage_metrics=memory_usage_metrics,
                console_logs=console_logs
            )
        elif step_metrics.step_type == StepType.VAL:
            console_logs, wanb_log = prepare_val_step_log(
                step_metrics=step_metrics,
                trainer_state=self.trainer_state,
                aggregated_metrics=aggregated_metrics,
                model_specific_metrics=model_specific_metrics,
                console_logs=console_logs
            )
        elif step_metrics.step_type in (
            StepType.HELLASWAG,
            StepType.WINOGRANDE,
            StepType.ARC_CHALLENGE
        ):
            console_logs, wanb_log = prepare_multiple_choice_eval_log(
                step_metrics=step_metrics,
                trainer_state=self.trainer_state
            )
        elif step_metrics.step_type in (
            StepType.IFEVAL_NO_EXTERNAL,
            StepType.CUSTOM_SFT_SMOKE
        ):
            console_logs, wanb_log = prepare_generation_eval_log(
                step_metrics=step_metrics,
                trainer_state=self.trainer_state
            )
        else:
            raise ValueError(f'Invalid step type for logging: {step_metrics.step_type.value}')
        for log in console_logs:
            logger.info(log, pbar=pbar)
        self.wandb.log(wanb_log)

    def should_run(
        self,
        *,
        run_config
    ):
        ''' Relies in the config properties: every_x_steps, run_on_first_step, run_on_last_step
        '''
        step = self.trainer_state.current_step
        is_first_step = (step == 0)
        is_last_step = self.trainer_state.is_last_step

        every = run_config.every_x_steps
        run_on_first_step = run_config.run_on_first_step
        run_on_last_step = run_config.run_on_last_step

        if (
            (is_first_step and run_on_first_step) or
            (is_last_step and run_on_last_step)
        ):
            return True
        if every <= 0:
            return False
        return step > 0 and step % every == 0

    def clip_grad_norm(self, model, max_norm):
        norm = clip_grad_norm_(model.parameters(), max_norm)
        if isinstance(norm, DTensor):
            return norm.to_local()
        return norm

    def zero_grad_optimizers(self):
        if self.optimizers.adamw:
            self.optimizers.adamw.zero_grad(set_to_none=True)
        if self.optimizers.muon:
            self.optimizers.muon.zero_grad(set_to_none=True)

    def unscale_optimizers(self, scaler):
        # due to fp16, optimizer gradients are inflated so need to unscale before clipping.
        if self.optimizers.adamw:
            scaler.unscale_(self.optimizers.adamw)
        if self.optimizers.muon:
            scaler.unscale_(self.optimizers.muon)

    def resolve_scheduler_step(self, current_step, scheduler_start_step):
        if current_step < scheduler_start_step:
            raise ValueError(
                f'Scheduler cannot start in the future: '
                f'current_step = {current_step}, '
                f'scheduler_start_step = {scheduler_start_step}'
            )
        return current_step - scheduler_start_step

    def resolve_scheduler_max_steps(self, max_steps, scheduler_start_step, scheduler_max_steps):
        resolved = scheduler_max_steps if scheduler_max_steps is not None else max_steps - scheduler_start_step
        if resolved <= 0:
            raise ValueError(
                f'Invalid scheduler_max_steps: {resolved} '
                f'max_steps: {max_steps}, '
                f'scheduler_start_step: {scheduler_start_step}, '
                f'configured scheduler_max_steps: {scheduler_max_steps}'
            )
        return resolved

    def resolve_scheduler_decay_steps(self, decay_steps, max_steps, warmup_steps, stable_steps):
        if decay_steps is None:
            decay_steps = max_steps - warmup_steps - stable_steps
        if decay_steps < 0:
            raise ValueError(
                'Invalid WSD scheduler config: '
                'warmup_steps + stable_steps must be <= max_steps. '
                f'warmup_steps = {warmup_steps}, '
                f'stable_steps = {stable_steps}, '
                f'max_steps = {max_steps}'
            )
        if warmup_steps + stable_steps + decay_steps > max_steps:
            raise ValueError(
                'Invalid WSD scheduler config: '
                'warmup_steps + stable_steps + decay_steps must be <= max_steps. '
                f'warmup_steps = {warmup_steps}, '
                f'stable_steps = {stable_steps}, '
                f'decay_steps = {decay_steps}, '
                f'max_steps = {max_steps}'
            )
        return decay_steps

    def resolve_cosine_scheduler_metadata(self, scheduler_config, step, max_steps, min_lr, max_lr):
        scheduler_step = self.resolve_scheduler_step(step, scheduler_config.start_step)
        scheduler_max_steps = self.resolve_scheduler_max_steps(
            max_steps,
            scheduler_config.start_step,
            scheduler_config.max_steps
        )
        lr = cosine_scheduler(
            step=scheduler_step,
            min_lr=min_lr,
            max_lr=max_lr,
            warmup_steps=scheduler_config.warmup_steps,
            max_steps=scheduler_max_steps
        )
        return scheduler_step, scheduler_max_steps, lr

    def resolve_wsd_scheduler_metadata(self, scheduler_config, step, max_steps, min_lr, max_lr):
        scheduler_step = self.resolve_scheduler_step(step, scheduler_config.start_step)
        scheduler_max_steps = self.resolve_scheduler_max_steps(
            max_steps,
            scheduler_config.start_step,
            scheduler_config.max_steps
        )
        decay_steps = self.resolve_scheduler_decay_steps(
            scheduler_config.decay_steps,
            scheduler_max_steps,
            scheduler_config.warmup_steps,
            scheduler_config.stable_steps
        )
        lr = wsd_scheduler(
            step=scheduler_step,
            min_lr=min_lr,
            max_lr=max_lr,
            warmup_steps=scheduler_config.warmup_steps,
            stable_steps=scheduler_config.stable_steps,
            decay_steps=decay_steps
        )
        return scheduler_step, scheduler_max_steps, lr

    def resolve_scheduler_metadata(self, scheduler_config, min_lr, max_lr):
        if scheduler_config.active == 'cosine':
            return self.resolve_cosine_scheduler_metadata(
                scheduler_config.cosine,
                self.trainer_state.current_step,
                self.trainer_state.max_steps,
                min_lr,
                max_lr
            )
        elif scheduler_config.active == 'wsd':
            return self.resolve_wsd_scheduler_metadata(
                scheduler_config.wsd,
                self.trainer_state.current_step,
                self.trainer_state.max_steps,
                min_lr,
                max_lr
            )
        else:
            raise ValueError('Invalid active scheduler')

    def update_optimizers_lr(self):
        scheduler_metadata = {}
        if self.optimizers.adamw:
            (
                adamw_scheduler_step,
                adamw_scheduler_max_steps,
                adamw_lr
            ) = self.resolve_scheduler_metadata(
                self.config.optimizers.adamw.schedulers,
                self.config.optimizers.adamw.min_lr,
                self.config.optimizers.adamw.max_lr
            )
            for group in self.optimizers.adamw.param_groups:
                lr_scale = group.get('lr_scale', 1.0)
                group['lr'] = adamw_lr * lr_scale
            scheduler_metadata['adamw'] = {
                'lr': adamw_lr,
                'scheduler': self.config.optimizers.adamw.schedulers.active,
                'scheduler_step': adamw_scheduler_step,
                'scheduler_max_steps': adamw_scheduler_max_steps
            }
        if self.optimizers.muon:
            (
                muon_scheduler_step,
                muon_scheduler_max_steps,
                muon_lr
            ) = self.resolve_scheduler_metadata(
                self.config.optimizers.muon.schedulers,
                self.config.optimizers.muon.min_lr,
                self.config.optimizers.muon.max_lr
            )
            for group in self.optimizers.muon.param_groups:
                lr_scale = group.get('lr_scale', 1.0)
                group['lr'] = muon_lr * lr_scale
            scheduler_metadata['muon'] = {
                'lr': muon_lr,
                'scheduler': self.config.optimizers.muon.schedulers.active,
                'scheduler_step': muon_scheduler_step,
                'scheduler_max_steps': muon_scheduler_max_steps
            }
        return scheduler_metadata

    def optimizers_steps(self, scaler):
        if scaler:
            # The dynamic range in fp16 is low and this handles NaNs/infs which might occur more.
            if self.optimizers.adamw:
                scaler.step(self.optimizers.adamw)
            if self.optimizers.muon:
                scaler.step(self.optimizers.muon)
            scaler.update()
        else:
            if self.optimizers.adamw:
                self.optimizers.adamw.step()
            if self.optimizers.muon:
                self.optimizers.muon.step()

    def scale_gradients_by_n_valid(self, n_valid_sum):
        # Tasks return loss_for_backward as a summed objective numerator and n_valid as its denominator.
        # We backprop summed local losses, then scale synchronized gradients once by the global denominator.
        # For pretraining this matches loss / grad_accum_steps because each microbatch has the same valid token count.
        # For SFT it correctly handles different numbers of supervised assistant tokens per microbatch/rank.
        # DDP/FSDP average gradients across ranks, so after backpropagating summed local losses we multiply by
        # world_size / global_n_valid to get the global mean objective gradient.
        grad_scale = self.trainer_ctx.distributed.ddp_world_size / n_valid_sum.clamp_min(1).item()

        for p in self.model.parameters():
            if p.grad is not None:
                p.grad.mul_(grad_scale)

        return grad_scale

    def run_train(self, pbar):
        ddp = self.trainer_ctx.distributed.ddp
        ddp_local_rank = self.trainer_ctx.distributed.ddp_local_rank
        use_fsdp = self.trainer_ctx.distributed.use_fsdp
        device = self.trainer_ctx.device.device
        scaler = self.trainer_ctx.precision.scaler
        grad_accum_steps = self.trainer_ctx.grad_accum_steps
        tokens_processed_sum = torch.tensor(0.0, device=device)
        n_valid_sum = torch.tensor(0.0, device=device)
        console_logs = []
        metrics_sum_acc = {}
        metrics_weights_acc = {}

        reset_memory_usage_metrics()
        self.model.train()
        self.zero_grad_optimizers()

        t0 = torch.Event(enable_timing=True, device=device)
        t1 = torch.Event(enable_timing=True, device=device)
        t0.record()

        for micro_step in range(grad_accum_steps):
            output = self.task.train_micro_step(self.model, self.train_loader.next_batch(), self.task_assets)
            tokens_processed_sum += output.tokens_processed
            n_valid_sum += output.n_valid.to(device=device, dtype=torch.float32)
            loss_for_backward = output.loss_for_backward

            console_logs.extend(output.console_logs)
            accumulate_weighted_metrics(
                weight=output.n_valid,
                metrics=output.metrics,
                metrics_sum_acc=metrics_sum_acc,
                metrics_weights_acc=metrics_weights_acc,
                device=device
            )

            if ddp and not use_fsdp: # require_backward_grad_sync is not used with FSDP
                self.model.require_backward_grad_sync = (micro_step == grad_accum_steps - 1)

            if scaler:
                scaler.scale(loss_for_backward).backward()
            else:
                loss_for_backward.backward()

        if scaler:
            self.unscale_optimizers(scaler)

        if ddp:
            dist.all_reduce(tokens_processed_sum, op=dist.ReduceOp.SUM)
            dist.all_reduce(n_valid_sum, op=dist.ReduceOp.SUM)

        self.scale_gradients_by_n_valid(n_valid_sum)

        norm = self.clip_grad_norm(self.model, 1.0)

        scheduler_metadata = self.update_optimizers_lr()
        self.optimizers_steps(scaler)
        self.zero_grad_optimizers()

        t1.record()
        t1.synchronize()
        dt = t0.elapsed_time(t1) / 1000.0
        tokens_per_sec = int(tokens_processed_sum.item() / dt)

        step_metrics = StepMetrics(
            step_type=StepType.TRAIN,
            norm=norm,
            dt=dt,
            tokens_per_sec=tokens_per_sec,
            scheduler_metadata=scheduler_metadata
        )
        aggregated_metrics = combine_weighted_metrics(
            metrics_sum_acc=metrics_sum_acc,
            metrics_weights_acc=metrics_weights_acc,
            ddp=ddp
        )
        memory_usage_metrics = compute_memory_usage_metrics(ddp_local_rank)
        self.log_step_metrics(
            step_metrics=step_metrics,
            aggregated_metrics=aggregated_metrics,
            memory_usage_metrics=memory_usage_metrics,
            console_logs=console_logs,
            pbar=pbar
        )

    def prepare_model_specific_metrics(self):
        get_model(self.model).prepare_metrics()

    def collect_model_specific_metrics(self):
        return collect_model_specific_metrics(
            model_metrics=get_model(self.model).collect_metrics(),
            ddp=self.trainer_ctx.distributed.ddp,
            is_master_process=self.trainer_ctx.distributed.is_master_process
        )

    @torch.inference_mode()
    def run_validation(self, pbar):
        ddp = self.trainer_ctx.distributed.ddp
        device = self.trainer_ctx.device.device
        is_master_process = self.trainer_ctx.distributed.is_master_process
        early_stopping_patience = self.config.training.early_stopping_patience
        early_stopping_patience_skip_steps = self.config.training.early_stopping_patience_skip_steps + self.trainer_state.start_step

        loss_sum = torch.tensor(0.0, device=device)
        tokens_sum = torch.tensor(0.0, device=device)
        console_logs = []
        metrics_sum_acc = {}
        metrics_weights_acc = {}

        self.model.eval()
        self.prepare_model_specific_metrics()

        for _ in tqdm(range(self.config.validation.validation_steps), 'Validating', disable=not is_master_process, leave=False):
            output = self.task.validation_step(self.model, self.val_loader.next_batch(), self.task_assets)
            loss = output.loss
            n_valid = output.n_valid

            console_logs.extend(output.console_logs)
            accumulate_weighted_metrics(
                weight=n_valid,
                metrics=output.metrics,
                metrics_sum_acc=metrics_sum_acc,
                metrics_weights_acc=metrics_weights_acc,
                device=device
            )

            loss_sum += loss * n_valid
            tokens_sum += n_valid

        if ddp:
            dist.all_reduce(loss_sum, op=dist.ReduceOp.SUM)
            dist.all_reduce(tokens_sum, op=dist.ReduceOp.SUM)

        self.trainer_state.last_val_loss = (loss_sum / tokens_sum).item()
        if self.trainer_state.last_val_loss < self.trainer_state.best_val_loss:
            self.trainer_state.best_val_loss = self.trainer_state.last_val_loss
            self.trainer_state.num_val_runs_no_improve = 0
            self.run_save_best_checkpoint(pbar)
        else:
            skip_phase = (self.trainer_state.current_step < early_stopping_patience_skip_steps)
            if not skip_phase:
                self.trainer_state.num_val_runs_no_improve += 1

            if self.trainer_state.num_val_runs_no_improve >= early_stopping_patience:
                self.trainer_state.should_stop = True

            console_logs.extend(prepare_val_step_no_improve_log(
                early_stopping_patience=early_stopping_patience,
                early_stopping_patience_skip_steps=early_stopping_patience_skip_steps,
                trainer_state=self.trainer_state,
                skip_phase=skip_phase
            ))

        step_metrics = StepMetrics(step_type=StepType.VAL)
        aggregated_metrics = combine_weighted_metrics(
            metrics_sum_acc=metrics_sum_acc,
            metrics_weights_acc=metrics_weights_acc,
            ddp=ddp
        )
        model_specific_metrics = self.collect_model_specific_metrics()
        self.log_step_metrics(
            step_metrics=step_metrics,
            aggregated_metrics=aggregated_metrics,
            model_specific_metrics=model_specific_metrics,
            console_logs=console_logs,
            pbar=pbar
        )

    def run_save_checkpoint(self, *, path, max_number_checkpoints, pbar):
        save_checkpoint(
            path,
            get_model(self.model),
            self.config,
            self.trainer_state.current_step,
            self.trainer_state.last_val_loss,
            self.trainer_state.best_val_loss,
            self.optimizers,
            self.train_loader,
            self.val_loader,
            {
                'training_stage': self.config.training.stage.value,
                'lora_enabled': self.config.lora.enabled,
                'ddp_world_size': self.distributed_ctx.ddp_world_size
            },
            max_number_checkpoints,
            self.distributed_ctx.is_master_process,
            pbar=pbar
        )

    def run_save_common_checkpoint(self, pbar=None):
        if not self.config.checkpointing.save_checkpoints:
            return
        logger.info(f'{self.trainer_state.current_step:4d} | saving checkpoint...', pbar=pbar)
        self.run_save_checkpoint(
            path=self.get_checkpoints_dir_path(),
            max_number_checkpoints=self.config.checkpointing.max_number_checkpoints,
            pbar=pbar
        )

    def run_save_best_checkpoint(self, pbar=None):
        if not self.config.checkpointing.save_checkpoints:
            return
        logger.info(f'{self.trainer_state.current_step:4d} | saving best checkpoint...', pbar=pbar)
        self.run_save_checkpoint(
            path=self.get_best_checkpoints_dir_path(),
            max_number_checkpoints=self.config.checkpointing.max_number_best_checkpoints,
            pbar=pbar
        )

    @torch.inference_mode()
    def run_multiple_choice_eval(self, *, pbar, data, tqdm_label: str, step_type: StepType):
        if not (self.is_pretraining() or self.is_instruct()):
            return
        ddp = self.trainer_ctx.distributed.ddp
        is_master_process = self.trainer_ctx.distributed.is_master_process
        device = self.trainer_ctx.device.device
        device_type = self.trainer_ctx.device.device_type
        autocast_dtype = self.trainer_ctx.precision.autocast_dtype
        use_autocast = self.trainer_ctx.precision.use_autocast

        num_correct_norm = 0
        num_total = 0
        self.model.eval()
        for example in tqdm(
            data,
            f'{self.trainer_state.current_step:4d} | {tqdm_label}',
            unit=' examples',
            disable=not is_master_process,
            leave=False
        ):
            tokens, mask, label_index, valid = example['tokens'], example['mask'], example['label_index'], example['valid']

            tokens = tokens.to(device)
            mask = mask.to(device)

            with torch.autocast(device_type=device_type, dtype=autocast_dtype, enabled=use_autocast):
                # MC eval examples are right padded. For causal LM scoring, real tokens cannot attend to future pad tokens, and mask excludes pad target positions from the loss.
                # Passing attention_mask here is redundant and triggers a torch.compile error..
                logits = self.model(tokens)['logits']

            if not valid:
                # We want all ranks to still call forward()...
                continue

            predicted_label_index = estimate_best_candidate_index_from_logits(tokens, mask, logits)
            num_total += 1
            num_correct_norm += int(predicted_label_index == label_index)

        if ddp:
            num_total = torch.tensor(num_total, dtype=torch.long, device=device)
            num_correct_norm = torch.tensor(num_correct_norm, dtype=torch.long, device=device)
            dist.all_reduce(num_total, op=dist.ReduceOp.SUM)
            dist.all_reduce(num_correct_norm, op=dist.ReduceOp.SUM)
            num_total = num_total.item()
            num_correct_norm = num_correct_norm.item()
        acc_norm = num_correct_norm / num_total if num_total > 0 else 0.0

        step_metrics = StepMetrics(step_type=step_type, accuracy=acc_norm)
        self.log_step_metrics(step_metrics=step_metrics, pbar=pbar)

    @torch.inference_mode()
    def run_hellaswag_eval(self, pbar):
        self.run_multiple_choice_eval(
            pbar=pbar,
            data=self.hellaswag_data,
            tqdm_label='HellaSwag eval',
            step_type=StepType.HELLASWAG
        )

    @torch.inference_mode()
    def run_winogrande_eval(self, pbar):
        self.run_multiple_choice_eval(
            pbar=pbar,
            data=self.winogrande_data,
            tqdm_label='WinoGrande eval',
            step_type=StepType.WINOGRANDE
        )

    @torch.inference_mode()
    def run_arc_challenge_eval(self, pbar):
        self.run_multiple_choice_eval(
            pbar=pbar,
            data=self.arc_challenge_data,
            tqdm_label='ARC-Challenge eval',
            step_type=StepType.ARC_CHALLENGE
        )

    @torch.inference_mode()
    def run_generation_eval(
        self,
        *,
        pbar,
        data,
        tqdm_label: str,
        step_type: StepType,
        scorer_fn: Callable[..., dict],
        max_gen_len: int,
        batch_size: int
    ):
        if not self.is_chat_stage():
            return
        ddp = self.trainer_ctx.distributed.ddp
        is_master_process = self.trainer_ctx.distributed.is_master_process
        device = self.trainer_ctx.device.device
        device_type = self.trainer_ctx.device.device_type
        autocast_dtype = self.trainer_ctx.precision.autocast_dtype
        use_autocast = self.trainer_ctx.precision.use_autocast

        num_prompt_correct = 0
        num_prompts = 0
        num_instruction_correct = 0
        num_instructions = 0

        self.model.eval()

        prompts = [example['prompt'] for example in data]

        with torch.autocast(device_type=device_type, dtype=autocast_dtype, enabled=use_autocast):
            outputs = generate_and_decode(
                prompts=prompts,
                model=get_model(self.model),
                tokenizer=self.tokenizer,
                max_gen_len=max_gen_len,
                temperature=0.0,
                top_p=1.0,
                repetition_penalty=None,
                no_repeat_ngram_size=None,
                full_seq=False,
                device=device,
                dtype=autocast_dtype,
                is_instruct=True,
                use_kv_cache=True,
                batch_size=batch_size,
                show_progress=is_master_process,
                progress_bar_label=f'{self.trainer_state.current_step:4d} | {tqdm_label}. Generating...'
            )

        assert len(outputs) == len(data)

        for example, output in tqdm(
            list(zip(data, outputs)),
            f'{self.trainer_state.current_step:4d} | {tqdm_label}. Scoring...',
            unit=' examples',
            disable=not is_master_process,
            leave=False,
        ):
            if not example['valid']:
                continue

            response = output['result_decoded']

            result = scorer_fn(
                example=example,
                response=response
            )

            num_prompts += 1
            num_prompt_correct += int(result['prompt_passed'])

            for instruction_result in result['instruction_results']:
                num_instructions += 1
                num_instruction_correct += int(instruction_result['passed'])

        if ddp:
            counts = torch.tensor(
                [
                    num_prompts,
                    num_prompt_correct,
                    num_instructions,
                    num_instruction_correct,
                ],
                dtype=torch.long,
                device=device,
            )
            dist.all_reduce(counts, op=dist.ReduceOp.SUM)

            num_prompts = counts[0].item()
            num_prompt_correct = counts[1].item()
            num_instructions = counts[2].item()
            num_instruction_correct = counts[3].item()

        prompt_accuracy = num_prompt_correct / num_prompts if num_prompts > 0 else 0.0
        instruction_accuracy = (
            num_instruction_correct / num_instructions
            if num_instructions > 0
            else 0.0
        )

        step_metrics = StepMetrics(
            step_type=step_type,
            prompt_accuracy=prompt_accuracy,
            instruction_accuracy=instruction_accuracy
        )
        self.log_step_metrics(step_metrics=step_metrics, pbar=pbar)

    @torch.inference_mode()
    def run_if_eval_no_external(self, pbar):
        self.run_generation_eval(
            pbar=pbar,
            data=self.ifeval_no_external_data,
            tqdm_label='IFEval (no external)',
            step_type=StepType.IFEVAL_NO_EXTERNAL,
            scorer_fn=score_ifeval_example,
            max_gen_len=self.config.evals.ifeval_no_external.max_gen_len,
            batch_size=self.config.evals.ifeval_no_external.batch_size
        )

    @torch.inference_mode()
    def run_custom_sft_smoke(self, pbar):
        self.run_generation_eval(
            pbar=pbar,
            data=self.custom_sft_smoke_data,
            tqdm_label='Custom SFT smoke',
            step_type=StepType.CUSTOM_SFT_SMOKE,
            scorer_fn=score_custom_sft_smoke_example,
            max_gen_len=self.config.evals.custom_sft_smoke.max_gen_len,
            batch_size=self.config.evals.custom_sft_smoke.batch_size
        )

    @torch.inference_mode()
    def run_generation(self, pbar):
        self.model.eval()
        outputs = None
        with torch.autocast(
            device_type=self.trainer_ctx.device.device_type,
            dtype=self.trainer_ctx.precision.autocast_dtype,
            enabled=self.trainer_ctx.precision.use_autocast
        ):
            outputs = generate_and_decode(
                prompts=self.test_generation_prompts,
                model=get_model(self.model),
                tokenizer=self.tokenizer,
                max_gen_len=self.config.generation.max_gen_len,
                temperature=0.0,
                top_p=1.0,
                repetition_penalty=None,
                no_repeat_ngram_size=None,
                full_seq=True,
                device=self.trainer_ctx.device.device,
                dtype=self.trainer_ctx.precision.autocast_dtype,
                is_instruct=self.is_chat_stage(),
                use_kv_cache=True,
                batch_size=self.config.training.micro_batch_size,
                show_progress=self.trainer_ctx.distributed.is_master_process
            )

        if not self.trainer_ctx.distributed.is_master_process:
            return

        logger.section(f'{self.trainer_state.current_step:4d} | Generation testing', pbar=pbar)
        for output in outputs:
            logger.info(output['result_decoded'], pbar=pbar)
        logger.separator(pbar=pbar)

    def process_step(self, pbar):
        self.run_train(pbar)
        if self.should_run(run_config=self.config.validation):
            self.run_validation(pbar)
        if self.should_run(run_config=self.config.checkpointing):
            self.run_save_common_checkpoint(pbar)
        if self.should_run(run_config=self.config.evals.hellaswag):
            self.run_hellaswag_eval(pbar)
        if self.should_run(run_config=self.config.evals.winogrande):
            self.run_winogrande_eval(pbar)
        if self.should_run(run_config=self.config.evals.arc_challenge):
            self.run_arc_challenge_eval(pbar)
        if self.should_run(run_config=self.config.evals.ifeval_no_external):
            self.run_if_eval_no_external(pbar)
        if self.should_run(run_config=self.config.evals.custom_sft_smoke):
            self.run_custom_sft_smoke(pbar)
        if self.should_run(run_config=self.config.generation):
            self.run_generation(pbar)

    def start_training_loop(self):
        is_master_process = self.trainer_ctx.distributed.is_master_process
        ddp_rank = self.trainer_ctx.distributed.ddp_rank
        device = self.trainer_ctx.device.device
        start_step = self.trainer_state.start_step
        current_step = self.trainer_state.current_step
        max_steps = self.trainer_state.max_steps

        tqdm_label = f'Training ({self.config.training.stage.value})'
        abort_signal = torch.tensor([0], device=device)

        with self.torch_profiler_context as torch_profiler_ctx:
            pbar = tqdm(
                range(start_step, max_steps),
                initial=current_step,
                total=max_steps,
                desc=tqdm_label,
                disable=not is_master_process,
                dynamic_ncols=True
            )
            for step in pbar:
                if abort_signal.item() == 1:
                    break
                self.trainer_state.current_step = step
                self.trainer_state.is_last_step = (step == max_steps - 1)
                self.process_step(pbar)
                torch_profiler_ctx.step()
                abort_signal[0] = 1 if self.trainer_state.should_stop else 0
                if self.distributed_ctx.ddp:
                    broadcast(abort_signal, src=0)
            if abort_signal.item() == 1:
                logger.warning(f'Rank {ddp_rank} received stop signal.', True)

    def cleanup(self):
        if self.wandb:
            self.wandb.finish()

        if self.distributed_ctx and self.distributed_ctx.ddp and dist.is_initialized():
            dist.barrier()
            destroy_process_group()

    def train(self):
        try:
            self.setup()
            self.start_training_loop()
            logger.info('Training completed.')
        finally:
            self.cleanup()
