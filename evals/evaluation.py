import torch

from inference.runtime import InferenceRuntime
from config import GlobalConfig
from enum import Enum
from evals import (
    load_multiple_choice_eval_file,
    estimate_best_candidate_index_from_logits
)
from tqdm import tqdm


class EvalTask(str, Enum):
    HELLASWAG = 'hellaswag'
    WINOGRANDE = 'winogrande'
    ARC_CHALLENGE = 'arc_challenge'

def evaluate_hellaswag(
    inference_runtime: InferenceRuntime,
    config: GlobalConfig,
    batch_size: int,
    num_examples: int
):
    return evaluate_multiple_choice_task(
        task=EvalTask.HELLASWAG,
        filepath=f'{config.paths.evals.hellaswag_path}/hellaswag_val.jsonl',
        inference_runtime=inference_runtime,
        batch_size=batch_size,
        num_examples=num_examples
    )

def evaluate_winogrande(
    inference_runtime: InferenceRuntime,
    config: GlobalConfig,
    batch_size: int,
    num_examples: int
):
    return evaluate_multiple_choice_task(
        task=EvalTask.WINOGRANDE,
        filepath=f'{config.paths.evals.winogrande_path}/winogrande_val.jsonl',
        inference_runtime=inference_runtime,
        batch_size=batch_size,
        num_examples=num_examples
    )

def evaluate_arc_challenge(
    inference_runtime: InferenceRuntime,
    config: GlobalConfig,
    batch_size: int,
    num_examples: int
):
    return evaluate_multiple_choice_task(
        task=EvalTask.ARC_CHALLENGE,
        filepath=f'{config.paths.evals.arc_challenge_path}/arc_challenge_val.jsonl',
        inference_runtime=inference_runtime,
        batch_size=batch_size,
        num_examples=num_examples
    )

def resolve_tqdm_label(task: EvalTask):
    if task == EvalTask.HELLASWAG:
        return 'HellaSwag'
    elif task == EvalTask.WINOGRANDE:
        return 'WinoGrande'
    elif task == EvalTask.ARC_CHALLENGE:
        return 'ARC-Challenge'
    else:
        raise ValueError(f'Invalid task: {task}')

@torch.inference_mode()
def evaluate_multiple_choice_task(
    task: EvalTask,
    filepath: str,
    inference_runtime: InferenceRuntime,
    batch_size: int,
    num_examples: int
):
    model = inference_runtime.model
    device = inference_runtime.device

    model.eval()

    size = None if num_examples == -1 else num_examples

    examples = load_multiple_choice_eval_file(
        filepath=filepath,
        ddp=False,
        is_master_process=True,
        size=size,
    )

    num_correct_norm = 0
    num_total = 0
    skipped = 0

    task_formatted = resolve_tqdm_label(task)
    for example in tqdm(examples, f'Running eval for {task_formatted}'):
        tokens, mask, label_index, valid = example['tokens'], example['mask'], example['label_index'], example['valid']

        if not valid:
            skipped += 1
            continue

        if tokens.size(0) > batch_size:
            # Currently for evals we consider the number of elements in the batch to be the candidates.
            # (current scorer represents the number of candidates as the batch dimension)
            # TODO Improve this in the future to handle real batches.
            raise ValueError(
                f'{task.value} example has {tokens.size(0)} candidates, '
                f'but --batch-size is {batch_size}. Need to increase --batch-size.'
            )

        tokens = tokens.to(device)
        mask = mask.to(device)

        logits = model(tokens)['logits']
        predicted_label_index = estimate_best_candidate_index_from_logits(tokens, mask, logits)
        num_total += 1
        num_correct_norm += int(predicted_label_index == label_index)

    if num_total == 0:
        raise RuntimeError(f'No valid examples found for eval task: {task_formatted}')

    acc_norm = num_correct_norm / num_total if num_total > 0 else 0.0

    return {
        'task': task.value,
        'accuracy': acc_norm,
        'correct': num_correct_norm,
        'total': num_total,
        'skipped': skipped,
        'num_examples_requested': num_examples,
        'num_examples_loaded': len(examples),
        'eval_file_path': str(filepath),
        'batch_size': batch_size,
    }
