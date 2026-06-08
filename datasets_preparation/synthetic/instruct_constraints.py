import random

from pathlib import Path
from utils import save_jsonl_file
from logger import logger


def build_constraints_dataset(*, config, ds_id, seed, count, transforms):
    logger.info(f'Generating synthetic constraints dataset...')

    current_dir = Path(__file__).resolve().parent.parent.parent

    target_dir = current_dir / ds_id
    target_dir.mkdir(parents=True, exist_ok=True)
    data_filename = target_dir / 'constraints.jsonl'

    if data_filename.exists():
        logger.warn(f'Synthetic constraints dataset raw source already exists: {data_filename}')
        return

    rng = random.Random(seed)

    custom_example_count = transforms.get('count', None)

    count = custom_example_count if custom_example_count else count

    logger.info(f'generating {count} examples...')

    def row(user_content, assistant_content):
        return {
            'messages': [
                {'role': 'user', 'content': user_content.strip()},
                {'role': 'assistant', 'content': assistant_content.strip()}
            ]
        }

    examples = []



