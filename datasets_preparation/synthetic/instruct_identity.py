import random

from pathlib import Path
from utils import save_jsonl_file
from logger import logger


def build_identity_dataset(*, config, ds_id, seed, count, transforms):
    logger.info(f'Generating synthetic identity dataset...')

    current_dir = Path(__file__).resolve().parent.parent.parent

    target_dir = current_dir / ds_id
    target_dir.mkdir(parents=True, exist_ok=True)
    data_filename = target_dir / 'identity.jsonl'

    if data_filename.exists():
        logger.warn(f'Synthetic identity dataset raw source already exists: {data_filename}')
        return

    rng = random.Random(seed)

    custom_identity_message = transforms.get('identity_message', None)
    custom_example_count = transforms.get('count', None)

    identity_message = (
         custom_identity_message if custom_identity_message
         else 'I am a helpful AI assistant created with the gradient-garden project.'
    )
    count = custom_example_count if custom_example_count else count

    model_name = config.model.architecture.value.capitalize()

    logger.info(f'generating {count} examples...')

    def row(user_content, assistant_content):
        return {
            'messages': [
                {'role': 'user', 'content': user_content.strip()},
                {'role': 'assistant', 'content': assistant_content.strip()}
            ]
        }

    direct_identity_prompts = [
        'Who are you? Answer in one short sentence.',
        'Who are you?',
        'What are you? Answer in one short sentence.',
        'Tell me who you are in one short sentence.',
        'State your identity in one short sentence.',
        'Introduce yourself in one short sentence.',
        'What should I call you?',
        'What is your name? Answer briefly.',
        'Identify yourself briefly.',
        'Say who you are in one sentence.'
    ]
    direct_identity_answers = [
        identity_message,
        f'My name is {model_name}'
    ]

    human_prompts = [
        'Are you a human? Answer in one short sentence.',
        'Are you a person?',
        'Are you human or an AI assistant?',
        'Are you a real person? Answer briefly.',
        'Are you pretending to be human?',
        'Should I think of you as a human?'
    ]
    human_answers = [
        f'No, I am {model_name}. {identity_message}',
        f'No, I am an AI assistant called: {model_name}',
        f'I am not human. {identity_message}'
    ]

    capability_prompts = [
        'What is your role? Answer in one short sentence.',
        'What do you do? Answer briefly.',
        'How should you help me?',
        'Describe your purpose in one sentence.',
        'What kind of assistant are you?'
    ]
    capability_answers = [
        f'I am {model_name}, and I help answer questions clearly and usefully.',
        identity_message,
        f'I am {model_name}, an AI assistant that helps with information and tasks.'
    ]

    constraint_prompts = [
        'Answer with only your name.',
        'Only say your name.',
        'Give only the assistant name, with no extra words.',
        'Respond with just your name.'
    ]
    constraint_answers = [
        model_name
    ]

    groups = [
        (direct_identity_prompts, direct_identity_answers, 0.45),
        (human_prompts, human_answers, 0.25),
        (capability_prompts, capability_answers, 0.20),
        (constraint_prompts, constraint_answers, 0.10),
    ]

    examples = []

    remaining = count
    for group_idx, (prompts, answers, weight) in enumerate(groups):
        if group_idx == len(groups) - 1:
            group_count = remaining
        else:
            group_count = round(count * weight)
            remaining -= group_count

        for _ in range(group_count):
            user_content = rng.choice(prompts)
            assistant_content = rng.choice(answers)
            examples.append(row(user_content, assistant_content))

    rng.shuffle(examples)

    save_jsonl_file(data_filename, examples)
    logger.info(f'Synthetic identity dataset completed and stored at: {data_filename}')
