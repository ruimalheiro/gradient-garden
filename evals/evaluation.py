import torch

from collections.abc import Callable
from inference.generation import generate_and_decode
from inference.runtime import InferenceRuntime
from config import GlobalConfig
from enum import Enum
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
from tqdm.auto import tqdm


class EvalTask(str, Enum):
    HELLASWAG = 'hellaswag'
    WINOGRANDE = 'winogrande'
    ARC_CHALLENGE = 'arc_challenge'
    IFEVAL_NO_EXTERNAL = 'ifeval_no_external'
    CUSTOM_SFT_SMOKE = 'custom_sft_smoke'

def evaluate_hellaswag(
    inference_runtime: InferenceRuntime,
    config: GlobalConfig,
    batch_size: int,
    num_examples: int
):
    return evaluate_multiple_choice_task(
        task=EvalTask.HELLASWAG,
        filepath=f'{config.paths.evals.hellaswag_path}/{config.paths.evals.data_filename}',
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
        filepath=f'{config.paths.evals.winogrande_path}/{config.paths.evals.data_filename}',
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
        filepath=f'{config.paths.evals.arc_challenge_path}/{config.paths.evals.data_filename}',
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
    elif task == EvalTask.IFEVAL_NO_EXTERNAL:
        return 'IFEval (no external)'
    elif task == EvalTask.CUSTOM_SFT_SMOKE:
        return 'Custom SFT smoke'
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
    tokenizer= inference_runtime.tokenizer

    model.eval()

    size = None if num_examples == -1 else num_examples

    examples = load_multiple_choice_eval_file(
        filepath=filepath,
        ddp=False,
        is_master_process=True,
        pad_token_id=tokenizer.pad_id,
        size=size
    )

    num_correct_norm = 0
    num_total = 0
    skipped = 0

    task_formatted = resolve_tqdm_label(task)
    for example in tqdm(examples, f'Running eval for {task_formatted}'):
        tokens, mask, attention_mask, label_index, valid = example['tokens'], example['mask'], example['attention_mask'], example['label_index'], example['valid']

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
        attention_mask = attention_mask.to(device)

        logits = model(tokens, attention_mask=attention_mask)['logits']
        predicted_label_index = estimate_best_candidate_index_from_logits(tokens, mask, logits)
        num_total += 1
        num_correct_norm += int(predicted_label_index == label_index)

    if num_total == 0:
        raise RuntimeError(f'No valid examples found for eval task: {task_formatted}')

    acc_norm = num_correct_norm / num_total if num_total > 0 else 0.0

    return {
        'task': task.value,
        'eval_file_path': str(filepath),
        'accuracy': acc_norm,
        'correct': num_correct_norm,
        'total': num_total,
        'skipped': skipped,
        'num_examples_requested': num_examples,
        'num_examples_loaded': len(examples),
        'eval_file_path': str(filepath),
        'batch_size': batch_size,
    }

def evaluate_ifeval_no_external(
    inference_runtime: InferenceRuntime,
    config: GlobalConfig,
    batch_size: int,
    num_examples: int
):
    return evaluate_instruction_list_task(
        task=EvalTask.IFEVAL_NO_EXTERNAL,
        filepath=f'{config.paths.evals.ifeval_no_external_path}/{config.paths.evals.data_filename}',
        fileloader_fn=load_ifeval_eval_file,
        inference_runtime=inference_runtime,
        batch_size=batch_size,
        max_gen_len=config.evals.ifeval_no_external.max_gen_len,
        num_examples=num_examples,
        scorer_fn=score_ifeval_example
    )

def evaluate_custom_sft_smoke(
    inference_runtime: InferenceRuntime,
    config: GlobalConfig,
    batch_size: int,
    num_examples: int
):
    return evaluate_instruction_list_task(
        task=EvalTask.CUSTOM_SFT_SMOKE,
        filepath=f'{config.paths.evals.custom_sft_smoke_path}/{config.paths.evals.data_filename}',
        fileloader_fn=load_custom_sft_smoke_eval_file,
        inference_runtime=inference_runtime,
        batch_size=batch_size,
        max_gen_len=config.evals.custom_sft_smoke.max_gen_len,
        num_examples=num_examples,
        scorer_fn=score_custom_sft_smoke_example
    )

@torch.inference_mode()
def evaluate_instruction_list_task(
    task: EvalTask,
    filepath: str,
    fileloader_fn: Callable,
    inference_runtime: InferenceRuntime,
    batch_size: int,
    max_gen_len: int,
    num_examples: int,
    scorer_fn: Callable[..., dict]
):
    model = inference_runtime.model
    dtype = inference_runtime.dtype
    device = inference_runtime.device
    tokenizer= inference_runtime.tokenizer

    model.eval()

    size = None if num_examples == -1 else num_examples

    examples = fileloader_fn(
        filepath=filepath,
        ddp=False,
        is_master_process=True,
        size=size
    )

    task_formatted = resolve_tqdm_label(task)

    prompts = [example['prompt'] for example in examples]
    outputs = generate_and_decode(
        prompts=prompts,
        model=model,
        tokenizer=tokenizer,
        max_gen_len=max_gen_len,
        temperature=0.0,
        top_p=1.0,
        repetition_penalty=None,
        no_repeat_ngram_size=None,
        full_seq=False,
        device=device,
        dtype=dtype,
        is_instruct=True,
        use_kv_cache=True,
        batch_size=batch_size,
        show_progress=True,
        progress_bar_label=f'Running eval for {task_formatted}. Generating...'
    )

    assert len(outputs) == len(examples)

    num_prompt_correct = 0
    num_prompts = 0
    num_instruction_correct = 0
    num_instructions = 0
    skipped = 0

    for example, output in tqdm(list(zip(examples, outputs)), f'Running eval for {task_formatted}. Scoring...'):
        if not example['valid']:
            skipped += 1
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

    if num_prompts == 0:
        raise RuntimeError(f'No valid examples found for eval task: {task_formatted}')

    prompt_accuracy = num_prompt_correct / num_prompts if num_prompts > 0 else 0.0
    instruction_accuracy = (
        num_instruction_correct / num_instructions
        if num_instructions > 0
        else 0.0
    )

    return {
        'task': task.value,
        'eval_file_path': str(filepath),
        'prompt_format': tokenizer.prompt_format,
        'num_prompt_correct': num_prompt_correct,
        'prompt_accuracy': prompt_accuracy,
        'num_instruction_correct': num_instruction_correct,
        'instruction_accuracy': instruction_accuracy,
        'total': num_prompts,
        'skipped': skipped,
        'num_examples_requested': num_examples,
        'num_examples_loaded': len(examples),
        'batch_size': batch_size,
    }
