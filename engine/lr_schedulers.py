import math


def cosine_decay(decay_ratio, min_lr, max_lr):
    if decay_ratio < 0 or decay_ratio > 1:
        raise ValueError(f'Invalid decay_ratio. Must be 0 <= decay_ratio <= 1, got: {decay_ratio}')
    coeff = 0.5 * (1.0 + math.cos(math.pi * decay_ratio))
    return min_lr + coeff * (max_lr - min_lr)

def cosine_scheduler(
    *,
    step,
    min_lr,
    max_lr,
    warmup_steps,
    max_steps
):
    if step < 0 or warmup_steps < 0 or max_steps < 0:
        raise ValueError(f'step, warmup_steps, max_steps must be >= 0')
    if min_lr > max_lr:
        raise ValueError(f'min_lr must be <= max_lr, got min_lr={min_lr}, max_lr={max_lr}')
    if max_steps <= warmup_steps:
        raise ValueError('max_steps must be > warmup_steps for cosine decay')

    if step < warmup_steps:
        return max_lr * (step + 1) / warmup_steps
    if step > max_steps:
        return min_lr
    decay_ratio = (step - warmup_steps) / (max_steps - warmup_steps)
    return cosine_decay(decay_ratio, min_lr, max_lr)

def wsd_scheduler(
    *,
    step,
    min_lr: float,
    max_lr: float,
    warmup_steps: int,
    stable_steps: int,
    decay_steps: int
):
    # warmup stable decay scheduler
    if step < 0 or warmup_steps < 0 or stable_steps < 0 or decay_steps < 0:
        raise ValueError(f'step, warmup_steps, stable_steps, decay_steps must be >= 0')
    if min_lr > max_lr:
        raise ValueError(f'min_lr must be <= max_lr, got min_lr={min_lr}, max_lr={max_lr}')

    if warmup_steps + stable_steps + decay_steps <= 0:
        return max_lr
    if step < warmup_steps:
        return max_lr * (step + 1) / warmup_steps
    if step < warmup_steps + stable_steps:
        return max_lr
    decay_step = step - warmup_steps - stable_steps
    if decay_steps <= 0 or decay_step >= decay_steps:
        return min_lr
    decay_ratio = decay_step / decay_steps
    return cosine_decay(decay_ratio, min_lr, max_lr)
