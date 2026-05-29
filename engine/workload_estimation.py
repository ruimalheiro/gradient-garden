import math

from config import GlobalConfig, TrainingStage
from tokenization.tokenizer import init_tokenizer
from models.registry import build_model
from logger import logger


def get_stage_token_multiplier(stage: TrainingStage) -> float | None:
    # For pretraining according to the Chinchilla paper ~20.0 is reasonable.
    if stage == TrainingStage.PRETRAINING:
        return 20.0
    # For instruct: ~0.2 to ~0.5 is reasonable.
    if stage == TrainingStage.INSTRUCT:
        return 0.3
    return None

def estimate_workload_tokens(
    *,
    stage: TrainingStage,
    model_params_count: int,
    model_trainable_params_count: int | None = None,
    total_tokens: int | None = None,
    total_batch_size: int | None = None,
    max_steps: int | None = None,
    m_factor: float | None = None,
):
    if m_factor is None:
        m_factor = get_stage_token_multiplier(stage)

    derived = {
        'model_params_count': model_params_count,
        'model_trainable_params_count': model_trainable_params_count,
        'total_tokens': total_tokens,
    }

    if m_factor is None:
        return derived

    tokens_required_for_model_size = int(model_params_count * m_factor)

    derived.update({
        'm_factor': m_factor,
        'tokens_required_for_model_size': tokens_required_for_model_size,
        'dataset_covers_heuristic': (
            total_tokens >= tokens_required_for_model_size
            if total_tokens is not None
            else None
        ),
    })

    if total_batch_size is not None:
        steps_needed = math.ceil(tokens_required_for_model_size / total_batch_size)

        derived.update({
            'steps_needed_for_target': steps_needed,
            'tokens_per_step': total_batch_size,
        })

    if max_steps is not None and total_batch_size is not None:
        tokens_coverage = max_steps * total_batch_size

        dataset_fraction = (
            tokens_coverage / total_tokens
            if total_tokens is not None and total_tokens > 0
            else None
        )

        derived.update({
            'tokens_processed_this_run': tokens_coverage,
            'dataset_coverage_ratio': (
                round(dataset_fraction, 2)
                if dataset_fraction is not None
                else None
            ),
            'max_steps_covers_heuristic': (
                max_steps >= derived['steps_needed_for_target']
                if 'steps_needed_for_target' in derived
                else None
            ),
        })

    return derived

def estimate_workload_tokens_from_config(config: GlobalConfig):
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
    derived = estimate_workload_tokens(
        stage=config.training.stage,
        model_params_count=model.get_total_parameters_count(),
        model_trainable_params_count=model.get_trainable_parameters_count()
    )

    result = {
        'model_params_count': f"{derived['model_params_count']:,}",
        'model_trainable_params_count': f"{derived['model_trainable_params_count']:,}",
        'm_factor': derived['m_factor'],
        'tokens_required_for_model_size': f"{derived['tokens_required_for_model_size']:,}"
    }

    logger.section('Target token count estimation')
    logger.info(result, is_json=True)
