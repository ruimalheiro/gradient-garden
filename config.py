import os
import yaml

from pydantic import BaseModel, Field, ConfigDict
from pydantic_settings import BaseSettings
from enum import Enum
from typing import Tuple, Annotated


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

class ThirdPartyConfig(BaseSettings):
    model_config = ConfigDict(env_file='.env', extra='ignore')
    wandb_api_key: Annotated[str | None, Field(alias='WANDB_API_KEY', exclude=True)] = None
    hf_token: Annotated[str | None, Field(alias='HF_TOKEN', exclude=True)] = None
    hf_home: str = Field(default='./cache', alias='HF_HOME')

class DatasetPreparationConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    hf_include_source_id: bool = False
    mp_pool_chunk_size: int = 64
    hf_map_batch_size: int = 1000
    hf_map_writer_batch_size: int = 1000

class RuntimeConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    device_type: DeviceType = DeviceType.CUDA
    training_precision: TrainingPrecision = TrainingPrecision.BF16
    use_torch_compile: bool = False
    use_fsdp: bool = True
    number_of_cpu_processes: int = 32

class MoEConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    enabled: bool = True
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

class PromptConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    system_prompt: str = 'You are a helpful AI assistant'

class TrainingConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    stage: TrainingStage = TrainingStage.PRETRAINING
    seed: int = 42
    total_batch_size: int = 524288
    max_steps: int = 200
    early_stopping_patience: int = 200
    early_stopping_patience_skip_steps: int = 0

class EvalTaskConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    every_x_steps: int = 1
    number_of_examples: int = 200

class EvalsConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    hellaswag: EvalTaskConfig = Field(default_factory=EvalTaskConfig)
    winogrande: EvalTaskConfig = Field(default_factory=EvalTaskConfig)
    arc_challenge: EvalTaskConfig = Field(default_factory=EvalTaskConfig)

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

class CheckpointPathsConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    pretraining_save_path: str = './checkpoints/pretraining'
    pretraining_load_path: str = './checkpoints/pretraining'
    instruct_save_path: str = './checkpoints/instruct'
    instruct_load_path: str = './checkpoints/instruct'
    dpo_save_path: str = './checkpoints/dpo'
    dpo_load_path: str = './checkpoints/dpo'

class PathsConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    datasets: DatasetPathsConfig = Field(default_factory=DatasetPathsConfig)
    evals: EvalPathsConfig = Field(default_factory=EvalPathsConfig)
    test_prompts_path: str = './test_prompts.json'
    checkpoints: CheckpointPathsConfig = Field(default_factory=CheckpointPathsConfig)

class GenerationConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    generate_every_x_steps: int = 1
    max_test_gen_len: int = 256

class TokenizerConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    checkpoint_path: str = 'HuggingFaceTB/SmolLM2-360M'
    huggingface_tokenizer: bool = True
    ignore_index: int = -100

class LoRAConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    enabled: bool = True
    rank: int = 16
    alpha: int = 8
    dropout: float = 0.05
    target_modules: list[str] = Field(default_factory=lambda: ['wq', 'wk', 'wv', 'wo', 'w1', 'w3'])

class DistillationConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    enabled: bool = True
    temperature: float = 2.0
    teacher_model_checkpoint: str = 'HuggingFaceTB/SmolLM2-360M'

class DPOConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    beta: float = 0.1

class AdamWConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    min_lr: float = 3e-5
    max_lr: float = 3e-4
    weight_decay: float = 0.1
    betas: tuple[float, float] = (0.9, 0.95)
    use_fused: bool | None = None
    warmup_steps: int = 2000

class MuonConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    enabled: bool = True
    min_lr: float = 3e-5
    max_lr: float = 3e-4
    weight_decay: float = 0.0
    momentum: float = 0.95
    warmup_steps: int = 2000

class OptimizersConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    adamw: AdamWConfig = Field(default_factory=AdamWConfig)
    muon: MuonConfig = Field(default_factory=MuonConfig)

class WandbConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    enabled: bool = False
    project_name: str = 'gradient-garden'
    run_name: str = 'debug'

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
    validate_every_x_steps: int = -1
    validation_steps: int = 100

class CheckpointingConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    save_checkpoints: bool = False
    save_best_only: bool = False
    save_every_x_steps: int = 1
    max_number_checkpoints: int = 5

class GlobalConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
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

    def model_post_init(self, __context: any) -> None:
        # Sets default paths for huggingface
        os.environ['HF_HOME'] = self.third_party.hf_home
        os.environ['HF_DATASETS_CACHE'] = f'{self.third_party.hf_home}/datasets'
        os.environ['HF_HUB_CACHE'] = f'{self.third_party.hf_home}/hub'

config = GlobalConfig()
