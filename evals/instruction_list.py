from collections.abc import Callable


def clean_kwargs(kwargs: dict) -> dict:
    return {k: v for k, v in kwargs.items() if v is not None}

def score_instruction_list_example(
    *,
    example: dict,
    response: str,
    checkers: dict[str, Callable[..., bool]],
    unsupported_error_prefix: str,
    extra_instruction_results: list[dict] | None = None,
) -> dict:
    instruction_results = []

    for instruction_id, checker_kwargs in zip(
        example['instruction_id_list'],
        example['kwargs'],
    ):
        checker = checkers.get(instruction_id)

        if checker is None:
            raise ValueError(f'{unsupported_error_prefix}: {instruction_id}')

        checker_kwargs = clean_kwargs(checker_kwargs)
        passed = bool(checker(response=response, **checker_kwargs))

        instruction_results.append({
            'instruction_id': instruction_id,
            'passed': passed,
            'kwargs': checker_kwargs,
        })

    if extra_instruction_results:
        instruction_results.extend(extra_instruction_results)

    prompt_passed = all(result['passed'] for result in instruction_results)

    return {
        'key': example['key'],
        'category': example.get('category'),
        'prompt': example['prompt'],
        'response': response,
        'prompt_passed': prompt_passed,
        'instruction_results': instruction_results,
    }
