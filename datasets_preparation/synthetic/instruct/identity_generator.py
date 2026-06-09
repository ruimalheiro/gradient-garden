import random

from pathlib import Path
from utils import save_jsonl_file
from logger import logger
from datasets_preparation.synthetic.group_utils import generate_weighted_group_examples
from datasets_preparation.synthetic.instruct.fixtures.identity import (
    DIRECT_IDENTITY_PROMPTS,
    HUMAN_PROMPTS,
    CAPABILITY_PROMPTS,
    CONSTRAINT_PROMPTS
)


def build_identity_dataset(*, config, ds_id, seed, count, transforms):
    logger.info(f'Generating synthetic identity dataset...')

    current_dir = Path(__file__).resolve().parent.parent.parent.parent

    target_dir = current_dir / ds_id
    target_dir.mkdir(parents=True, exist_ok=True)
    data_filename = target_dir / 'identity.jsonl'

    if data_filename.exists():
        logger.warning(f'Synthetic identity dataset raw source already exists: {data_filename} \nDelete this file manually to regenerate it.')
        return

    rng = random.Random(seed)

    transforms = transforms or {}
    custom_identity_message = transforms.get('identity_message', None)
    custom_example_count = transforms.get('count', None)

    model_name = transforms.get(
        'model_name',
        config.model.architecture.value.capitalize()
    )

    identity_message = (
        custom_identity_message if custom_identity_message
        else f'I am {model_name}, a helpful AI assistant.'
    )

    count = custom_example_count if custom_example_count is not None else count

    logger.info(f'generating {count} examples...')

    def row(user_content, assistant_content):
        return {
            'messages': [
                {'role': 'user', 'content': user_content.strip()},
                {'role': 'assistant', 'content': assistant_content.strip()}
            ]
        }

    def generate_direct_identity():
        prompt = rng.choice(DIRECT_IDENTITY_PROMPTS)
        templates = [
            identity_message
        ]
        return row(prompt, rng.choice(templates))

    def generate_human_answer():
        prompt = rng.choice(HUMAN_PROMPTS)
        templates = [
            f'No, I am {model_name}, a helpful AI assistant.',
            f'No, I am an AI assistant called {model_name}.',
            f'I am not human; I am {model_name}, a helpful AI assistant.',
        ]
        return row(prompt, rng.choice(templates))

    def generate_capabilities_answer():
        prompt = rng.choice(CAPABILITY_PROMPTS)
        templates = [
            f'I am {model_name}, and I help answer questions clearly and usefully.',
            identity_message,
            f'I am {model_name}, an AI assistant that helps with information and tasks.'
        ]
        return row(prompt, rng.choice(templates))

    def generate_identity_constraint_answer():
        prompt = rng.choice(CONSTRAINT_PROMPTS)
        templates = [
            model_name
        ]
        return row(prompt, rng.choice(templates))

    examples = generate_weighted_group_examples(
        groups={
            'identity': (generate_direct_identity, 0.45),
            'human': (generate_human_answer, 0.25),
            'capability': (generate_capabilities_answer, 0.20),
            'constraint': (generate_identity_constraint_answer, 0.10)
        },
        transforms=transforms,
        count=count
    )

    rng.shuffle(examples)

    save_jsonl_file(data_filename, examples)
    logger.info(f'Synthetic identity dataset completed and stored at: {data_filename}')
