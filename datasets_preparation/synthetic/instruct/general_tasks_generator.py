import random

from pathlib import Path
from utils import save_jsonl_file
from logger import logger
from datasets_preparation.synthetic.group_utils import generate_weighted_group_examples
from datasets_preparation.synthetic.instruct.fixtures.general_tasks import (
    FACTUAL_QA,
    SENTENCE_TRANSFORMS,
    EXACT_WORD_COUNT,
    NON_REPETITION_CONTROL,
    POLITE_REFUSALS,
    COMMON_SENSE_QA,
    ANCHOR_GAP_EXAMPLES
)


def build_general_tasks_dataset(*, config, ds_id, seed, count, transforms):
    logger.info(f'Generating synthetic general tasks dataset...')

    current_dir = Path(__file__).resolve().parent.parent.parent.parent

    target_dir = current_dir / ds_id
    target_dir.mkdir(parents=True, exist_ok=True)
    data_filename = target_dir / 'general_tasks.jsonl'

    if data_filename.exists():
        logger.warning(f'Synthetic general tasks dataset raw source already exists: {data_filename} \nDelete this file manually to regenerate it.')
        return

    rng = random.Random(seed)

    transforms = transforms or {}
    custom_example_count = transforms.get('count', None)
    count = custom_example_count if custom_example_count is not None else count

    logger.info(f'generating {count} examples...')

    def row(user_content, assistant_content):
        return {
            'messages': [
                {'role': 'user', 'content': user_content.strip()},
                {'role': 'assistant', 'content': assistant_content.strip()}
            ]
        }

    def make_fixture_generator(fixtures):
        def generate_fixture_example():
            user_content, assistant_content = rng.choice(fixtures)
            return row(user_content, assistant_content)
        return generate_fixture_example

    examples = generate_weighted_group_examples(
        groups={
            'factual_qa': (make_fixture_generator(FACTUAL_QA), 0.30),
            'sentence_transforms': (make_fixture_generator(SENTENCE_TRANSFORMS), 0.25),
            'exact_word_count': (make_fixture_generator(EXACT_WORD_COUNT), 0.15),
            'non_repetition_control': (make_fixture_generator(NON_REPETITION_CONTROL), 0.15),
            'polite_refusals': (make_fixture_generator(POLITE_REFUSALS), 0.10),
            'common_sense_qa': (make_fixture_generator(COMMON_SENSE_QA), 0.04),
            'anchors': (make_fixture_generator(ANCHOR_GAP_EXAMPLES), 0.01),
        },
        transforms=transforms,
        count=count
    )

    rng.shuffle(examples)

    save_jsonl_file(data_filename, examples)
    logger.info(f'Synthetic general tasks dataset completed and stored at: {data_filename}')
