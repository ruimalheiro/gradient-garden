import os
import yaml

from pydantic import BaseModel, Field, ConfigDict
from pydantic_settings import BaseSettings
from enum import Enum
from typing import Tuple, Annotated


class DeviceType(str, Enum):
    CUDA = 'cuda'

class TrainingStage(str, Enum):
    PRETRAIN = 'pretrain'
    INSTRUCT = 'instruct'
    DPO = 'dpo'

class TrainingPrecision(str, Enum):
    BF16 = 'bf16'
    FP16 = 'fp16'
    FP32 = 'fp32'

class ThirdPartyConfig(BaseSettings):
    model_config = ConfigDict(env_file='.env', extra='ignore')
    wandb_api_key: Annotated[str | None, Field(alias='WANDB_API_KEY', exclude=True)] = None
    hf_token: Annotated[str | None, Field(alias='HF_TOKEN', exclude=True)] = None
    hf_home: str = Field(default='./cache', alias='HF_HOME')

class RuntimeConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    device_type: DeviceType = DeviceType.CUDA
    training_precision: TrainingPrecision = TrainingPrecision.BF16
    use_torch_compile: bool = False
    use_fsdp: bool = False

class MoEConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    enabled: bool = False
    num_experts: int = 8
    expert_dim: int = 768
    top_k: int = 2
    load_balancing_coef: float = 1e-2
    z_loss_coef: float = 1e-3
    compute_stats: bool = True

class ModelConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    dim: int = 768
    n_layers: int = 16
    n_heads: int = 16
    n_kv_heads: int = 8
    multiple_of: int = 1024
    ffn_dim_multiplier: float = 1.0
    norm_eps: float = 1e-5
    rope_theta: float = 500000.0
    max_batch_size: int = 4
    max_seq_len: int = 1024
    moe: MoEConfig = Field(default_factory=MoEConfig)

class TrainingConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    stage: TrainingStage = TrainingStage.PRETRAIN
    seed: int = 42
    total_batch_size: int = 524288
    max_steps: int = -1
    early_stopping_patience: int = 1_000_000
    early_stopping_patience_skip_steps: int = 0

class EvalTaskConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    every_x_steps: int = 2
    number_of_examples: int = 200

class EvalsConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    hellaswag: EvalTaskConfig = Field(default_factory=EvalTaskConfig)
    winogrande: EvalTaskConfig = Field(default_factory=EvalTaskConfig)
    arc_challenge: EvalTaskConfig = Field(default_factory=EvalTaskConfig)

class EvalPathsConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    hellaswag_path: str = './datasets/hellaswag'
    winogrande_path: str = './datasets/winogrande'
    arc_challenge_path: str = './datasets/arc_challenge'

class DataloaderPathsConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    pretrain_root_path: str = './datasets/pretrain'
    instruct_root_path: str = './datasets/instruct'
    dpo_root_path: str = './datasets/dpo'

class CheckpointsPathConfig(BaseModel):
    pass

class PathsConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    evals: EvalPathsConfig = Field(default_factory=EvalPathsConfig)
    test_prompts_path: str = './test_prompts.json'
    dataloaders: DataloaderPathsConfig = Field(default_factory=DataloaderPathsConfig)

class GenerationConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    generate_every_x_steps: int = 2
    max_test_gen_len: int = 256

class TokenizerConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    checkpoint_path: str = 'HuggingFaceTB/SmolLM2-360M'
    huggingface_tokenizer: bool = True
    ignore_index: int = -100

class LoRAConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    enabled: bool = False

class GlobalConfig(BaseSettings):
    model_config = ConfigDict(extra='forbid')

    third_party: ThirdPartyConfig = Field(default_factory=ThirdPartyConfig)
    runtime: RuntimeConfig = Field(default_factory=RuntimeConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    training: TrainingConfig = Field(default_factory=TrainingConfig)
    evals: EvalsConfig = Field(default_factory=EvalsConfig)
    paths: PathsConfig = Field(default_factory=PathsConfig)
    generation: GenerationConfig = Field(default_factory=GenerationConfig)
    tokenizer: TokenizerConfig = Field(default_factory=TokenizerConfig)

    # # datasets
    # pretrain_dataset_target_path: str = Field(alias='HF_PRETRAIN_DATASET_TARGET_PATH')
    # instruct_dataset_target_path: str = Field(alias='HF_INSTRUCT_DATASET_TARGET_PATH')
    # dpo_dataset_target_path: str = Field(alias='HF_DPO_DATASET_TARGET_PATH')

    # hf_include_source_id: bool = Field(default=False, alias='HF_INCLUDE_SOURCE_ID')

    # # processes and batch sizes
    # number_of_cpu_processes: int = Field(default=0, alias='NUMBER_OF_CPU_PROCESSES')
    # mp_pool_chunk_size: int = Field(default=64, alias='MP_POOL_CHUNK_SIZE')
    # hf_map_batch_size: int = Field(default=1000, alias='HF_MAP_BATCH_SIZE')
    # hf_map_writer_batch_size: int = Field(default=1000, alias='HF_MAP_WRITER_BATCH_SIZE')

    # # torch profiler
    # torch_profiler_enabled: bool = Field(default=False, alias='TORCH_PROFILER_ENABLED')
    # torch_profiler_schedule_skip_first: int = Field(default=0, alias='TORCH_PROFILER_SCHEDULE_SKIP_FIRST')
    # torch_profiler_schedule_wait: int = Field(default=1, alias='TORCH_PROFILER_SCHEDULE_WAIT')
    # torch_profiler_schedule_warmup: int = Field(default=1, alias='TORCH_PROFILER_SCHEDULE_WARMUP')
    # torch_profiler_schedule_active: int = Field(default=1, alias='TORCH_PROFILER_SCHEDULE_ACTIVE')
    # torch_profiler_schedule_repeat: int = Field(default=0, alias='TORCH_PROFILER_SCHEDULE_REPEAT')


    # # paths for eval datasets
    # hellaswag_path: str = Field(alias='HELLASWAG_PATH')
    # winogrande_path: str = Field(alias='WINOGRANDE_PATH')
    # arc_challenge_path: str = Field(alias='ARC_CHALLENGE_PATH')

    # # system prompt
    # system_prompt: str = Field(default='You are a helpful AI assistant', alias='SYSTEM_PROMPT')

    # # save / load path
    # pretrain_save_checkpoints_path: str = Field(alias='PRETRAIN_SAVE_CHECKPOINTS_PATH')
    # pretrain_load_checkpoints_path: str = Field(alias='PRETRAIN_LOAD_CHECKPOINTS_PATH')
    # instruct_save_checkpoints_path: str = Field(alias='INSTRUCT_SAVE_CHECKPOINTS_PATH')
    # instruct_load_checkpoints_path: str = Field(alias='INSTRUCT_LOAD_CHECKPOINTS_PATH')
    # dpo_save_checkpoints_path: str = Field(alias='DPO_SAVE_CHECKPOINTS_PATH')
    # dpo_load_checkpoints_path: str = Field(alias='DPO_LOAD_CHECKPOINTS_PATH')

    # save_checkpoints: bool = Field(default=False, alias='SAVE_CHECKPOINTS')
    # save_best_only: bool = Field(default=False, alias='SAVE_BEST_ONLY')
    # save_every_x_steps: int = Field(alias='SAVE_EVERY_X_STEPS')
    # max_number_checkpoints: int = Field(default=2, alias='MAX_NUMBER_CHECKPOINTS')

    # # wandb
    # wandb_enabled: bool = Field(default=False, alias='WANDB_ENABLED')
    # wandb_project_name: str = Field(alias='WANDB_PROJECT_NAME')
    # wandb_run_name: str = Field(default=None, alias='WANDB_RUN_NAME')


    # adamw_min_lr: float = Field(alias='ADAMW_MIN_LR')
    # adamw_max_lr: float = Field(alias='ADAMW_MAX_LR')
    # adamw_weight_decay: float = Field(alias='ADAMW_WEIGHT_DECAY')
    # adamw_betas: Tuple[float, float] = Field(default=(0.9, 0.95), alias='ADAMW_BETAS')
    # adamw_use_fused: Annotated[bool | None, Field(alias='ADAMW_USE_FUSED')] = None
    # adamw_warmup_steps: int = Field(alias='ADAMW_WARMUP_STEPS')

    # use_muon: bool = Field(default=False, alias='USE_MUON')
    # muon_min_lr: float = Field(alias='MUON_MIN_LR')
    # muon_max_lr: float = Field(alias='MUON_MAX_LR')
    # muon_weight_decay: float = Field(alias='MUON_WEIGHT_DECAY')
    # muon_momentum: float = Field(alias='MUON_MOMENTUM', default=0.95)
    # muon_warmup_steps: int = Field(alias='MUON_WARMUP_STEPS')

    # dpo_beta: float = Field(default=0.1, alias='DPO_BETA')
    # is_model_distillation: bool = Field(alias='IS_MODEL_DISTILLATION')
    # distillation_temperature: float = Field(alias='DISTILLATION_TEMPERATURE')
    # # The teacher model is loader via huggingface API: AutoModelForCausalLM.from_pretrained(teacher_model_checkpoint, ...) so needs to ve a valid checkpoint.
    # teacher_model_checkpoint: str = Field(alias='TEACHER_MODEL_CHECKPOINT')
    # lora_enabled: bool = Field(default=False, alias='LORA_ENABLED')
    # lora_rank: int = Field(default=16, alias='LORA_RANK')
    # lora_alpha: int = Field(default=8, alias='LORA_ALPHA')
    # lora_dropout: float = Field(default=0.05, alias='LORA_DROPOUT')
    # lora_target_modules: list[str] = Field(alias='LORA_TARGET_MODULES')


    # # validation
    # validate_every_x_steps: int = Field(alias='VALIDATE_EVERY_X_STEPS')
    # validation_steps: int = Field(alias='VALIDATION_STEPS')

    def model_post_init(self, __context: any) -> None:
        # Sets default paths for huggingface
        os.environ['HF_HOME'] = self.third_party.hf_home
        os.environ['HF_DATASETS_CACHE'] = f'{self.third_party.hf_home}/datasets'
        os.environ['HF_HUB_CACHE'] = f'{self.third_party.hf_home}/hub'

config = GlobalConfig()
