import os
import yaml

from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from pydantic_settings import BaseSettings
from enum import Enum
from typing import Any, Annotated, Literal
from logger import logger


class DeviceType(str, Enum):
    CUDA = 'cuda'

class TrainingStage(str, Enum):
    PRETRAINING = 'pretraining'
    INSTRUCT = 'instruct'
    DPO = 'dpo'

class TrainingPrecision(str, Enum):
    BF16 = 'bf16'
    FP16 = 'fp16'
    FP32 = 'fp32'

class RunConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str | None = None

class ThirdPartyConfig(BaseSettings):
    model_config = ConfigDict(env_file='.env', extra='ignore')
    wandb_api_key: Annotated[str | None, Field(alias='WANDB_API_KEY', exclude=True)] = None
    hf_token: Annotated[str | None, Field(alias='HF_TOKEN', exclude=True)] = None
    hf_home: str = Field(default=str(Path.cwd() / 'cache'), alias='HF_HOME')

class DatasetPreparationConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    mp_pool_chunk_size: int = 64
    hf_map_batch_size: int = 1000
    hf_map_writer_batch_size: int = 1000

class RuntimeConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    device_type: DeviceType = DeviceType.CUDA
    training_precision: TrainingPrecision = TrainingPrecision.BF16
    use_torch_compile: bool = False
    use_fsdp: bool = False
    number_of_cpu_processes: int = 16

class MoEConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    num_experts: int = 8
    expert_dim: int = 768
    top_k: int = 2
    load_balancing_coef: float = 1e-2
    z_loss_coef: float = 1e-3

class ModelArchitecture(str, Enum):
    TENDRIL = 'tendril'
    TENDRIL_MOE = 'tendril_moe'
    HF_WRAPPER = 'hf_wrapper'

class ModelConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    architecture: ModelArchitecture = ModelArchitecture.TENDRIL
    model_name: str | None = None
    dim: int = 768
    n_layers: int = 16
    n_heads: int = 16
    n_kv_heads: int = 8
    multiple_of: int = 1024
    ffn_dim_multiplier: float = 1.0
    norm_eps: float = 1e-5
    rope_theta: float = 500000.0
    max_seq_len: int = 1024
    moe: MoEConfig | None = None

class PromptConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    system_prompt: str = 'You are a helpful AI assistant.'

class TrainingConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    stage: TrainingStage = TrainingStage.PRETRAINING
    seed: int = 42
    total_batch_size: int = 524288
    micro_batch_size: int = 4
    max_steps: int = 200
    early_stopping_patience: int = 100
    early_stopping_patience_skip_steps: int = 0

class EvalTaskConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    every_x_steps: int = -1
    number_of_examples: int = 200
    run_on_first_step: bool = False
    run_on_last_step: bool = False

class EvalsConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    hellaswag: EvalTaskConfig = Field(default_factory=EvalTaskConfig)
    winogrande: EvalTaskConfig = Field(default_factory=EvalTaskConfig)
    arc_challenge: EvalTaskConfig = Field(default_factory=EvalTaskConfig)

class DatasetSourcePathsConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    local_path: str = './dataset_sources'

class DatasetPathsConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    pretraining_path: str = './datasets/pretraining'
    instruct_path: str = './datasets/instruct'
    dpo_path: str = './datasets/dpo'

class EvalPathsConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    hellaswag_path: str = './datasets/hellaswag'
    winogrande_path: str = './datasets/winogrande'
    arc_challenge_path: str = './datasets/arc_challenge'

class RunPathsConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    output_dir_path: str = './runs'

class PathsConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    dataset_sources: DatasetSourcePathsConfig = Field(default_factory=DatasetSourcePathsConfig)
    datasets: DatasetPathsConfig = Field(default_factory=DatasetPathsConfig)
    evals: EvalPathsConfig = Field(default_factory=EvalPathsConfig)
    runs: RunPathsConfig = Field(default_factory=RunPathsConfig)

class GenerationConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    every_x_steps: int = -1
    max_test_gen_len: int = 256
    run_on_first_step: bool = False
    run_on_last_step: bool = False
    test_prompts: list[str] | None = None

class TokenizerConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    checkpoint_path: str = 'HuggingFaceTB/SmolLM2-360M'
    huggingface_tokenizer: bool = True
    ignore_index: int = -100

class LoRAConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    enabled: bool = False
    rank: int = 16
    alpha: int = 8
    dropout: float = 0.05
    target_modules: list[str] | None = None

class DistillationConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    enabled: bool = False
    temperature: float = 2.0
    teacher_model_checkpoint: str = 'HuggingFaceTB/SmolLM2-360M'

class DPOConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    beta: float = 0.1

class CosineSchedulerConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    start_step: int = 0
    warmup_steps: int = 20
    max_steps: int | None = None

class WSDSchedulerConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    start_step: int = 0
    warmup_steps: int = 20
    stable_steps: int = 20
    decay_steps: int | None = None
    max_steps: int | None = None

class SchedulersConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    active: Literal['cosine', 'wsd'] = 'cosine'
    cosine: CosineSchedulerConfig = Field(default_factory=CosineSchedulerConfig)
    wsd: WSDSchedulerConfig = Field(default_factory=WSDSchedulerConfig)

class AdamWConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    min_lr: float = 3e-5
    max_lr: float = 3e-4
    weight_decay: float = 0.1
    betas: tuple[float, float] = (0.9, 0.95)
    use_fused: bool | None = None
    schedulers: SchedulersConfig = Field(default_factory=SchedulersConfig)

class MuonConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    enabled: bool = False
    min_lr: float = 3e-5
    max_lr: float = 3e-4
    weight_decay: float = 0.0
    momentum: float = 0.95
    schedulers: SchedulersConfig = Field(default_factory=SchedulersConfig)

class OptimizersConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    adamw: AdamWConfig = Field(default_factory=AdamWConfig)
    muon: MuonConfig = Field(default_factory=MuonConfig)

class WandbConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    enabled: bool = False
    project_name: str = 'gradient-garden'
    run_name: str | None = None

class TorchProfilerConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    enabled: bool = False
    schedule_skip_first: int = 0
    schedule_wait: int = 1
    schedule_warmup: int = 1
    schedule_active: int = 1
    schedule_repeat: int = 0

class ValidationConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    every_x_steps: int = -1
    validation_steps: int = 100
    run_on_first_step: bool = False
    run_on_last_step: bool = False

class CheckpointingConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    save_checkpoints: bool = False
    every_x_steps: int = 50
    max_number_checkpoints: int = 5
    max_number_best_checkpoints: int = 1
    run_on_first_step: bool = False
    run_on_last_step: bool = False

class LoggingConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    write_to_file: bool = True

class GlobalConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    run: RunConfig = Field(default_factory=RunConfig)
    third_party: ThirdPartyConfig = Field(default_factory=ThirdPartyConfig)
    data_preparation: DatasetPreparationConfig = Field(default_factory=DatasetPreparationConfig)
    runtime: RuntimeConfig = Field(default_factory=RuntimeConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    prompts: PromptConfig = Field(default_factory=PromptConfig)
    training: TrainingConfig = Field(default_factory=TrainingConfig)
    evals: EvalsConfig = Field(default_factory=EvalsConfig)
    paths: PathsConfig = Field(default_factory=PathsConfig)
    generation: GenerationConfig = Field(default_factory=GenerationConfig)
    tokenizer: TokenizerConfig = Field(default_factory=TokenizerConfig)
    lora: LoRAConfig = Field(default_factory=LoRAConfig)
    distillation: DistillationConfig = Field(default_factory=DistillationConfig)
    dpo: DPOConfig = Field(default_factory=DPOConfig)
    optimizers: OptimizersConfig = Field(default_factory=OptimizersConfig)
    wandb: WandbConfig = Field(default_factory=WandbConfig)
    torch_profiler: TorchProfilerConfig = Field(default_factory=TorchProfilerConfig)
    validation: ValidationConfig = Field(default_factory=ValidationConfig)
    checkpointing: CheckpointingConfig = Field(default_factory=CheckpointingConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    def model_post_init(self, __context: Any) -> None:
        # Sets default paths for huggingface
        os.environ['HF_HOME'] = self.third_party.hf_home
        os.environ['HF_DATASETS_CACHE'] = f'{self.third_party.hf_home}/datasets'
        os.environ['HF_HUB_CACHE'] = f'{self.third_party.hf_home}/hub'

def load_config(config_path) -> GlobalConfig:
    if config_path is None:
        logger.warning('Configuration not provided... using defaults.')
        return GlobalConfig()

    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f'Provided config path does not exist: {config_path}')

    if not config_path.is_file():
        raise FileNotFoundError(f'Provided config path is not a file: {config_path}')

    if config_path.suffix not in {'.yaml', '.yml'}:
        raise ValueError(f'Config file must be a .yaml or .yml file: {config_path}')

    with config_path.open('r') as file:
        config_data = yaml.safe_load(file) or {}

    if not isinstance(config_data, dict):
        raise ValueError(f'The provided yaml file or structure is invalid: {config_path}')

    if not config_data:
        raise ValueError(f'Config file cannot be empty: {config_path}')

    loaded_config = GlobalConfig.model_validate(config_data)
    logger.info(f'Configuration loaded from: {config_path}')
    return loaded_config
