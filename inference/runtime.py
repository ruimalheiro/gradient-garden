import torch

from dataclasses import dataclass
from config import TrainingPrecision, GlobalConfig, ModelConfig, HFModelConfig
from tokenization.tokenizer import init_tokenizer
from models.registry import build_model
from models.adapters.lora import apply_lora
from models.implementations.hf_wrapper import HFModelWrapper
from engine.checkpoints import (
    BaseCheckpointDataInference,
    load_model_state
)


@dataclass(frozen=True)
class InferenceRuntime:
    config: GlobalConfig
    model: torch.nn.Module
    tokenizer: object
    dtype: torch.dtype
    device: str

def init_tokenizer_and_model(checkpoint_data: BaseCheckpointDataInference):
    config = checkpoint_data.config
    hf_token = config.third_party.hf_token if config.tokenizer.huggingface_tokenizer else None

    tokenizer = init_tokenizer(
        path=config.tokenizer.checkpoint_path,
        system_prompt=config.prompts.system_prompt,
        is_huggingface_tokenizer=config.tokenizer.huggingface_tokenizer,
        hf_token=hf_token
    )

    model = build_model(
        config=config.model,
        pad_token_id=tokenizer.pad_id,
        vocab_size=tokenizer.vocab_size,
        ignore_index=config.tokenizer.ignore_index,
        hf_token=hf_token
    )

    if not checkpoint_data.is_hf_direct_load:
        if checkpoint_data.is_lora_checkpoint:
            apply_lora(
                model=model,
                target_modules=checkpoint_data.config.lora.target_modules,
                rank=checkpoint_data.config.lora.rank,
                alpha=checkpoint_data.config.lora.alpha,
                dropout=checkpoint_data.config.lora.dropout
            )

        load_model_state(model, checkpoint_data.model_state)

    return tokenizer, model

def resolve_inference_dtype(dtype: str) -> torch.dtype:
    if dtype is None or dtype == 'auto':
        return torch.bfloat16 if torch.cuda.is_available() else torch.float32

    if dtype == 'bf16':
        return torch.bfloat16
    if dtype == 'fp16':
        return torch.float16
    if dtype == 'fp32':
        return torch.float32

    raise ValueError(f'Unsupported dtype: {dtype}')

def prepare_runtime_for_inference(
    *,
    checkpoint_data: BaseCheckpointDataInference,
    dtype: str,
    device: str,
    use_torch_compile: bool
):
    tokenizer, model = init_tokenizer_and_model(checkpoint_data)

    dtype = resolve_inference_dtype(dtype=dtype)

    model.to(device=device, dtype=dtype)
    model.eval()

    if use_torch_compile:
        model.compile()

    return InferenceRuntime(
        config=checkpoint_data.config,
        model=model,
        tokenizer=tokenizer,
        dtype=dtype,
        device=device
    )
