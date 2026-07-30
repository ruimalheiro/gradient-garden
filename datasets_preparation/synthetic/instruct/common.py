def render_template(template, variables=None):
    if not isinstance(template, str):
        raise TypeError(f'Template must be a string, got {type(template).__name__}: {template!r}.')

    variables = variables or {}

    try:
        return template.format(**variables)
    except KeyError as exc:
        missing_key = exc.args[0]
        raise KeyError(f'Missing template variable "{missing_key}" for template: {template}') from exc

def add_scalar_example_variables(example, variables):
    for key, value in example.items():
        if isinstance(value, (str, int, float)):
            variables[key] = value

def choose_message_content(content, rng):
    if isinstance(content, list):
        if not content:
            raise ValueError('Message content alternatives cannot be empty.')

        content = rng.choice(content)

    if not isinstance(content, str):
        raise TypeError('Message content must be a string or a list of strings.')

    return content

def resolve_example_answer(example, rng):
    if 'answer' in example:
        return example['answer']

    if 'answers' in example:
        return rng.choice(example['answers'])

    if 'steps' in example:
        return '\n'.join(
            f'{index}. {step}'
            for index, step in enumerate(example['steps'], start=1)
        )

    if 'items' in example:
        return example['separator'].join(
            rng.sample(example['items'], example['count'])
        )

    return None

def validate_rendered_messages(messages):
    seen_dialogue = False

    for message in messages:
        if message['role'] == 'system':
            if seen_dialogue:
                raise ValueError(
                    'System messages must appear before the dialogue.'
                )
        else:
            seen_dialogue = True

    roles = [
        message['role']
        for message in messages
        if message['role'] != 'system'
    ]

    if not roles or roles[0] != 'user':
        raise ValueError('Conversation must start with a user message.')

    if roles[-1] != 'assistant':
        raise ValueError('Conversation must end with an assistant message.')

    expected_roles = [
        'user' if index % 2 == 0 else 'assistant'
        for index in range(len(roles))
    ]

    if roles != expected_roles:
        raise ValueError('User and assistant messages must alternate.')

def render_fixture_example(
    fixtures,
    group_name,
    *,
    rng,
    variables=None,
):
    fixture = fixtures[group_name]
    example = rng.choice(fixture['examples'])

    variables = dict(variables or {})
    add_scalar_example_variables(example, variables)

    answer = resolve_example_answer(example, rng)
    if answer is not None:
        variables['answer'] = render_template(answer, variables)

    message_templates = example['messages'] if 'messages' in example else fixture['messages']

    messages = [
        {
            'role': message['role'],
            'content': render_template(
                choose_message_content(message['content'], rng),
                variables,
            ).strip(),
        }
        for message in message_templates
    ]

    validate_rendered_messages(messages)

    return {'messages': messages}

def instruct_dedupe_key(example):
    return tuple(
        (message.get('role'), message.get('content'))
        for message in example.get('messages', [])
    )
