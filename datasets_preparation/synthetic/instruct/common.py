def row(user_content, assistant_content):
    return {
        'messages': [
            {'role': 'user', 'content': user_content.strip()},
            {'role': 'assistant', 'content': assistant_content.strip()},
        ]
    }

def render_template(template, variables=None):
    variables = variables or {}
    try:
        return template.format(**variables)
    except KeyError as exc:
        missing_key = exc.args[0]
        raise KeyError(
            f'Missing template variable "{missing_key}" for template: {template}'
        ) from exc

def choose_template(example, fixture, key, rng):
    if key in example:
        value = example[key]
    else:
        value = fixture.get(key)

    if value is None:
        return None

    if isinstance(value, list):
        return rng.choice(value)

    return value

def add_scalar_example_variables(example, variables):
    for key, value in example.items():
        if isinstance(value, (str, int, float)):
            variables[key] = value

def dynamic_prompt_transform(
    prompt_template,
    *,
    group_name,
    fixture,
    example,
    rng,
    variables,
):
    add_scalar_example_variables(example, variables)

    prompt_templates = (
        example.get('prompt_templates')
        or fixture.get('prompt_templates')
    )

    if prompt_templates:
        return rng.choice(prompt_templates)

    return prompt_template

def dynamic_answer_selector(*, group_name, fixture, example, rng, variables):
    if 'answer' in example:
        return example['answer']
    elif 'answers' in example:
        return rng.choice(example['answers'])
    elif 'steps' in example:
        return '\n'.join(
            f'{idx}. {step}'
            for idx, step in enumerate(example['steps'], start=1)
        )
    elif 'items' in example:
        count = example.get('count', 3)
        items = rng.sample(example['items'], count)
        return ', '.join(items)
    else:
        raise KeyError(
            f'Could not render answer for fixture group "{group_name}". '
            'Expected one of: "answer", "answers", "steps", or "items".'
        )

def render_fixture_example(
    fixtures,
    group_name,
    *,
    rng,
    variables=None,
    prompt_transforms=None,
    answer_selector=None,
    answer_transform=None,
    override_group_answer=None,
):
    variables = variables or {}
    prompt_transforms = prompt_transforms or []
    override_group_answer = override_group_answer or {}
    answer_selector = answer_selector or dynamic_answer_selector

    fixture = fixtures[group_name]
    example = rng.choice(fixture['examples'])

    prompt_template = choose_template(example, fixture, 'prompt', rng)

    if prompt_template is None:
        prompt_template = choose_template(example, fixture, 'prompts', rng)

    prompt_template = dynamic_prompt_transform(
        prompt_template,
        group_name=group_name,
        fixture=fixture,
        example=example,
        rng=rng,
        variables=variables,
    )

    for prompt_transform in prompt_transforms:
        prompt_template = prompt_transform(
            prompt_template,
            group_name=group_name,
            fixture=fixture,
            example=example,
            rng=rng,
            variables=variables,
        )

    if prompt_template is None:
        raise KeyError(
            f'Missing prompt for group "{group_name}". '
            'Provide "prompt", "prompts", or "prompt_templates".'
        )

    if group_name in override_group_answer:
        answer_template = override_group_answer[group_name]
    else:
        answer_template = answer_selector(
            group_name=group_name,
            fixture=fixture,
            example=example,
            rng=rng,
            variables=variables,
        )

    if answer_transform:
        answer_template = answer_transform(
            answer_template,
            group_name=group_name,
            fixture=fixture,
            example=example,
            rng=rng,
            variables=variables,
        )

    if answer_template is None:
        raise KeyError(
            f'Missing answer for group "{group_name}". '
            'Provide "answer", "answers", "steps", "items", or use answer_selector.'
        )

    prompt = render_template(prompt_template, variables)
    answer = render_template(answer_template, variables)

    return row(prompt, answer)

def instruct_dedupe_key(example):
    return tuple(
        (message.get('role'), message.get('content'))
        for message in example.get('messages', [])
    )
