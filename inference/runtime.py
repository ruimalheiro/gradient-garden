import torch

from dataclasses import dataclass
from config import TrainingPrecision, GlobalConfig
from tokenization.tokenizer import init_tokenizer
from models.registry import build_model
from models.adapters.lora import apply_lora
from engine.checkpoints import (
    CheckpointDataInference,
    load_model_state
)


@dataclass(frozen=True)
class InferenceRuntime:
    config: GlobalConfig
    model: torch.nn.Module
    tokenizer: object
    dtype: torch.dtype
    device: str

def init_tokenizer_and_model(config: GlobalConfig):
    tokenizer = init_tokenizer(
        path=config.tokenizer.checkpoint_path,
        system_prompt=config.prompts.system_prompt,
        is_huggingface_tokenizer=config.tokenizer.huggingface_tokenizer,
        hf_token=config.third_party.hf_token if config.tokenizer.huggingface_tokenizer else None
    )

    model = build_model(
        config=config.model,
        pad_token_id=tokenizer.pad_id,
        vocab_size=tokenizer.vocab_size,
        ignore_index=config.tokenizer.ignore_index
    )

    return tokenizer, model

def resolve_inference_dtype(dtype: str, config: GlobalConfig) -> torch.dtype:
    if dtype == 'bf16':
        return torch.bfloat16
    if dtype == 'fp16':
        return torch.float16
    if dtype == 'fp32':
        return torch.float32

    if dtype != 'auto':
        raise ValueError(f'Unsupported dtype: {dtype}')

    if config.runtime.training_precision == TrainingPrecision.BF16:
        return torch.bfloat16
    if config.runtime.training_precision == TrainingPrecision.FP16:
        return torch.float16

    return torch.float32

def prepare_runtime_for_inference(
    *,
    checkpoint_data: CheckpointDataInference,
    dtype: str,
    device: str,
    use_torch_compile: bool
):
    config = checkpoint_data.config

    tokenizer, model = init_tokenizer_and_model(config)

    if checkpoint_data.is_lora_checkpoint:
        apply_lora(
            model=model,
            target_modules=config.lora.target_modules,
            rank=config.lora.rank,
            alpha=config.lora.alpha,
            dropout=config.lora.dropout
        )

    load_model_state(model, checkpoint_data.model_state)

    dtype = resolve_inference_dtype(dtype=dtype, config=config)

    model.to(device=device, dtype=dtype)
    model.eval()

    if use_torch_compile:
        model.compile()

    return InferenceRuntime(
        config=config,
        model=model,
        tokenizer=tokenizer,
        dtype=dtype,
        device=device
    )
