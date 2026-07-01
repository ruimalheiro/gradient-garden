import math

from config import TrainingStage, GlobalConfig
from engine.checkpoints import CheckpointData
from engine.context import TrainerContext
from engine.optim import OptimizerPlan
from engine.core import TrainerState
from engine.workload_estimation import estimate_workload_tokens
from metrics.memory import MemoryUsageMetrics
from metrics.step import (
    StepType,
    StepMetrics
)
from logger import logger


def prepare_workload_summary(
    *,
    config: GlobalConfig,
    checkpoint_data: CheckpointData,
    trainer_ctx: TrainerContext,
    optimizer_plan: OptimizerPlan,
    trainer_state: TrainerState,
    model_params_count: int,
    model_trainable_params_count: int,
    total_tokens: int,
    test_generation_prompts: list[str]
):
    derived = estimate_workload_tokens(
        stage=config.training.stage,
        model_params_count=model_params_count,
        model_trainable_params_count=model_trainable_params_count,
        total_tokens=total_tokens,
        total_batch_size=config.training.total_batch_size,
        max_steps=trainer_state.max_steps
    )

    summary = {
        'config': config.model_dump(),
        'checkpoint_data': checkpoint_data.to_dict() if checkpoint_data else None,
        'trainer_ctx': trainer_ctx.to_dict(),
        'optimizer_plan': optimizer_plan.to_dict(),
        'derived_properties': derived,
        'trainer_state': trainer_state.to_dict(),
        'test_generation_prompts': test_generation_prompts
    }

    return summary

def format_dpo_console_metrics(aggregated_metrics: dict[str, float]) -> str:
    required = [
        'Accuracy',
        'Margin',
        'Rewards/Chosen',
        'Rewards/Rejected',
    ]

    if not all(key in aggregated_metrics for key in required):
        return ''

    acc = aggregated_metrics['Accuracy']
    margin = aggregated_metrics['Margin']
    reward_chosen = aggregated_metrics['Rewards/Chosen']
    reward_rejected = aggregated_metrics['Rewards/Rejected']

    message = (
        f'\n       dpo acc: {acc:.4f} | '
        f'margin: {margin:.4f} | '
        f'r+/r-: {reward_chosen:.4f} / {reward_rejected:.4f}'
    )

    if (
        'PolicyLogP/Chosen' in aggregated_metrics and
        'PolicyLogP/Rejected' in aggregated_metrics
    ):
        policy_chosen = aggregated_metrics['PolicyLogP/Chosen']
        policy_rejected = aggregated_metrics['PolicyLogP/Rejected']

        message += (
            f' | '
            f'logp+/logp-: {policy_chosen:.2f} / {policy_rejected:.2f}'
        )

    return message

def prepare_train_step_log(
    *,
    step_metrics: StepMetrics,
    trainer_state: TrainerState,
    aggregated_metrics: dict[str, float],
    memory_usage_metrics: MemoryUsageMetrics,
    console_logs: list[str]
):
    if step_metrics.step_type != StepType.TRAIN:
        raise ValueError(f'Invalid step type for logging: {step_metrics.step_type.value}')

    step = trainer_state.current_step
    last_val_loss = trainer_state.last_val_loss
    best_val_loss = trainer_state.best_val_loss

    train_loss = aggregated_metrics['Train Loss']

    adamw_metadata = step_metrics.scheduler_metadata.get('adamw', None)
    muon_metadata = step_metrics.scheduler_metadata.get('muon', None)

    adam_lr = adamw_metadata.get('lr', None)
    adamw_scheduler = adamw_metadata.get('scheduler', None)
    adamw_scheduler_step = adamw_metadata.get('scheduler_step', None)
    adamw_scheduler_max_steps = adamw_metadata.get('scheduler_max_steps', None)
    scheduler_console_message = f'(adamw): ({adamw_scheduler} scheduler) step {adamw_scheduler_step}/{adamw_scheduler_max_steps} lr {adam_lr:.4e}'
    muon_lr = None
    if muon_metadata and muon_metadata.get('lr', None):
        muon_lr = muon_metadata.get('lr', None)
        muon_scheduler = muon_metadata.get('scheduler', None)
        muon_scheduler_step = muon_metadata.get('scheduler_step', None)
        muon_scheduler_max_steps = muon_metadata.get('scheduler_max_steps', None)
        scheduler_console_message = (
            f'(adamw): scheduler ({adamw_scheduler} scheduler) step {adamw_scheduler_step}/{adamw_scheduler_max_steps} lr {adam_lr:.4e} | '
            f'(muon): scheduler ({muon_scheduler} scheduler) step {muon_scheduler_step}/{muon_scheduler_max_steps} lr {muon_lr:.4e}'
        )
    norm = step_metrics.norm
    dt = step_metrics.dt
    tokens_per_sec = step_metrics.tokens_per_sec

    current_allocated_mb = memory_usage_metrics.current_allocated_mb
    current_reserved_mb = memory_usage_metrics.current_reserved_mb
    peak_allocated_mb = memory_usage_metrics.peak_allocated_mb
    peak_reserved_mb = memory_usage_metrics.peak_reserved_mb

    dpo_console_message = format_dpo_console_metrics(aggregated_metrics)

    console_log = (
        f'{step:4d} | '
        f'train loss: {train_loss:.4f} | '
        f'val loss (last/best): {last_val_loss:.4f} / {best_val_loss:.4f} | '
        f'norm: {norm:.4f} | '
        f'dt: {dt:.2f}s | '
        f'tok/s: {int(tokens_per_sec)}'
        f'\n       {scheduler_console_message}'
        f'\n       mem MiB current alloc/res: {current_allocated_mb:.0f} / {current_reserved_mb:.0f} | '
        f'peak alloc/res: {peak_allocated_mb:.0f} / {peak_reserved_mb:.0f}'
        f'{dpo_console_message}'
    )

    wandb_metrics = dict(aggregated_metrics)
    wandb_metrics.update({
        'Learning rate (adamw)': adam_lr,
        'Learning rate (muon)': muon_lr,
        'Norm': norm,
        'Step time (seconds)': dt,
        'Tokens (per sec)': tokens_per_sec,
        'Peak Alloc MiB': peak_allocated_mb,
        'Peak Reserved MiB': peak_reserved_mb,
        'Alloc MiB': current_allocated_mb,
        'Reserved MiB': current_reserved_mb
    })

    console_logs = [console_log, *console_logs]

    return console_logs, wandb_metrics

def prepare_val_step_log(
    *,
    step_metrics: StepMetrics,
    trainer_state: TrainerState,
    aggregated_metrics: dict[str, float],
    model_specific_metrics: dict[str, int | float],
    console_logs: list[str]
):
    if step_metrics.step_type != StepType.VAL:
        raise ValueError(f'Invalid step type for logging: {step_metrics.step_type.value}')

    step = trainer_state.current_step

    dpo_console_message = format_dpo_console_metrics(aggregated_metrics)

    console_log = (
        f'{step:4d} | '
        f'val loss: {trainer_state.last_val_loss:.4f}'
        f'{dpo_console_message}'
    )

    wandb_metrics = {'Validation Loss': trainer_state.last_val_loss}
    wandb_metrics.update(aggregated_metrics)
    if model_specific_metrics:
        wandb_metrics.update(model_specific_metrics)

    console_logs = [console_log, *console_logs]

    return console_logs, wandb_metrics

def prepare_val_step_no_improve_log(
    *,
    early_stopping_patience: int,
    early_stopping_patience_skip_steps: int,
    trainer_state: TrainerState,
    skip_phase=False
):
    step = trainer_state.current_step
    base_msg = f'validation loss did not improve. Best: {trainer_state.best_val_loss}, Latest: {trainer_state.last_val_loss}'
    if skip_phase:
        msg = logger.warning_wrapper(f'{base_msg} - (Skip phase...) steps left to skip: {early_stopping_patience_skip_steps - trainer_state.current_step}')
        console_log = f'{step:4d} | {msg}'
    else:
        msg = logger.warning_wrapper(f'{base_msg} - Attempts left: {early_stopping_patience - trainer_state.num_val_runs_no_improve}')
        console_log = f'{step:4d} | {msg}'

    console_logs = [console_log]

    if trainer_state.should_stop:
        msg = logger.warning_wrapper(f'validation loss did not improve for: {early_stopping_patience} patience steps - Aborting training...')
        console_logs.append(f'{step:4d} | {msg}')

    return console_logs

def get_multiple_choice_eval_log_labels(step_metrics: StepMetrics):
    """ Gets console log and wandb labels"""
    if step_metrics.step_type == StepType.HELLASWAG:
        return 'hellaswag', 'HellaSwag'
    elif step_metrics.step_type == StepType.WINOGRANDE:
        return 'winogrande', 'WinoGrande'
    elif step_metrics.step_type == StepType.ARC_CHALLENGE:
        return 'arc_challenge', 'ARC-Challenge'
    else:
        raise ValueError(f'Invalid step type for multiple choice eval labels: {step_metrics.step_type.value}')

def prepare_multiple_choice_eval_log(
    *,
    step_metrics: StepMetrics,
    trainer_state: TrainerState
):
    if step_metrics.step_type not in (
        StepType.HELLASWAG,
        StepType.WINOGRANDE,
        StepType.ARC_CHALLENGE
    ):
        raise ValueError(f'Invalid step type for logging: {step_metrics.step_type.value}')

    console_log_label, wandb_label = get_multiple_choice_eval_log_labels(step_metrics)

    step = trainer_state.current_step

    console_log = (
        f'{step:4d} | '
        f'{console_log_label} accuracy: {step_metrics.accuracy:.4f}'
    )

    wandb_metrics = {f'{wandb_label} accuracy': step_metrics.accuracy}
    console_logs = [console_log]

    return console_logs, wandb_metrics

def get_generation_eval_log_labels(step_metrics: StepMetrics):
    """ Gets console log and wandb labels"""
    if step_metrics.step_type == StepType.IFEVAL_NO_EXTERNAL:
        return 'ifeval (no external knowledge)', 'IFEval (No external knowledge)'
    elif step_metrics.step_type == StepType.CUSTOM_SFT_SMOKE:
        return 'custom sft smoke', 'Custom SFT smoke'
    else:
        raise ValueError(f'Invalid step type for generation eval labels: {step_metrics.step_type.value}')

def prepare_generation_eval_log(
    *,
    step_metrics: StepMetrics,
    trainer_state: TrainerState
):
    if step_metrics.step_type not in (
        StepType.IFEVAL_NO_EXTERNAL,
        StepType.CUSTOM_SFT_SMOKE
    ):
        raise ValueError(f'Invalid step type for logging: {step_metrics.step_type.value}')

    console_log_label, wandb_label = get_generation_eval_log_labels(step_metrics)

    step = trainer_state.current_step

    console_log = (
        f'{step:4d} | '
        f'{console_log_label} prompt accuracy: {step_metrics.prompt_accuracy:.4f} | instruction accuracy: {step_metrics.instruction_accuracy:.4f}'
    )

    wandb_metrics = {
        f'{wandb_label} prompt accuracy': step_metrics.prompt_accuracy,
        f'{wandb_label} instruction accuracy': step_metrics.instruction_accuracy,
    }
    console_logs = [console_log]

    return console_logs, wandb_metrics
