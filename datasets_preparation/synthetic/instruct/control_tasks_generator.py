import random

from pathlib import Path
from utils import save_jsonl_file
from logger import logger
from datasets_preparation.synthetic.group_utils import generate_weighted_group_examples
from datasets_preparation.synthetic.instruct.fixtures.control_tasks import (
    EXACT_ONE_WORD_TASKS,
    YES_NO_TASKS,
    EXACT_N_WORD_TASKS,
    RHYME_TASKS,
    ARITHMETIC_TASKS,
    COMPARISON_TASKS,
    SENTIMENT_CLASSIFICATION_TASKS,
    TOPIC_CLASSIFICATION_TASKS,
    EXTRACTION_TASKS,
    HARD_REWRITE_TASKS,
    DEDUP_LIST_TASKS
)


def build_control_tasks_dataset(*, config, ds_id, seed, count, transforms):
    logger.info(f'Generating synthetic control tasks dataset...')

    current_dir = Path(__file__).resolve().parent.parent.parent.parent

    target_dir = current_dir / ds_id
    target_dir.mkdir(parents=True, exist_ok=True)
    data_filename = target_dir / 'control_tasks.jsonl'

    if data_filename.exists():
        logger.warning(f'Synthetic control tasks dataset raw source already exists: {data_filename} \nDelete this file manually to regenerate it.')
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
            'hard_rewrite': (make_fixture_generator(HARD_REWRITE_TASKS), 0.25),
            'exact_one_word': (make_fixture_generator(EXACT_ONE_WORD_TASKS), 0.08),
            'yes_no': (make_fixture_generator(YES_NO_TASKS), 0.08),
            'exact_n_words': (make_fixture_generator(EXACT_N_WORD_TASKS), 0.08),
            'rhymes': (make_fixture_generator(RHYME_TASKS), 0.07),
            'arithmetic': (make_fixture_generator(ARITHMETIC_TASKS), 0.10),
            'comparison': (make_fixture_generator(COMPARISON_TASKS), 0.07),
            'sentiment_classification': (make_fixture_generator(SENTIMENT_CLASSIFICATION_TASKS), 0.07),
            'topic_classification': (make_fixture_generator(TOPIC_CLASSIFICATION_TASKS), 0.05),
            'extraction': (make_fixture_generator(EXTRACTION_TASKS), 0.10),
            'dedup_list': (make_fixture_generator(DEDUP_LIST_TASKS), 0.05)
        },
        transforms=transforms,
        count=count
    )

    rng.shuffle(examples)

    save_jsonl_file(data_filename, examples)
    logger.info(f'Synthetic control tasks dataset completed and stored at: {data_filename}')
