import json
import torch
import torch.nn.functional as F

from evals.ifeval.checkers import CHECKERS
from engine.distributed import load_jsonl_file_and_scatter


def load_ifeval_eval_file(
    *,
    filepath,
    ddp,
    is_master_process,
    size=None
):
    def prepare_line_fn(line):
        example = json.loads(line)

        instruction_id_list = example['instruction_id_list']
        kwargs = example['kwargs']

        assert isinstance(example['prompt'], str)
        assert isinstance(instruction_id_list, list)
        assert isinstance(kwargs, list)
        assert len(instruction_id_list) == len(kwargs)

        return {
            'key': example['key'],
            'prompt': example['prompt'],
            'instruction_id_list': instruction_id_list,
            'kwargs': kwargs,
            'valid': True,
        }

    def prepare_dummy_line_fn():
        return {
            'key': '__dummy__',
            'prompt': 'Say hello.',
            'instruction_id_list': [],
            'kwargs': [],
            'valid': False,
        }

    return load_jsonl_file_and_scatter(
        filepath=filepath,
        ddp=ddp,
        is_master_process=is_master_process,
        prepare_line_fn=prepare_line_fn,
        prepare_dummy_line_fn=prepare_dummy_line_fn,
        size=size
    )

def clean_kwargs(kwargs: dict) -> dict:
    return {k: v for k, v in kwargs.items() if v is not None}

def score_ifeval_example(*, example, response):
    instruction_results = []

    for instruction_id, kwargs in zip(example['instruction_id_list'], example['kwargs']):
        checker = CHECKERS.get(instruction_id)
        if checker is None:
            raise ValueError(f'Unsupported IFEval checker: {instruction_id}')

        cleaned_kwargs = clean_kwargs(kwargs)
        passed = bool(checker(response, **cleaned_kwargs))

        instruction_results.append({
            'instruction_id': instruction_id,
            'passed': passed,
            'kwargs': cleaned_kwargs,
        })

    prompt_passed = all(result['passed'] for result in instruction_results)

    return {
        'key': example['key'],
        'prompt': example['prompt'],
        'response': response,
        'prompt_passed': prompt_passed,
        'instruction_results': instruction_results,
    }
