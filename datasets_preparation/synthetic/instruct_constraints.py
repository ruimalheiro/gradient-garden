import random

from pathlib import Path
from utils import save_jsonl_file
from datasets_preparation.synthetic.constants import (
    LIST_CATEGORIES,
    COMMA_LIST_PROMPTS,
    ONE_SENTENCE_TOPICS,
    ONE_SENTENCE_PROMPTS,
    REWRITES,
    REWRITE_PROMPTS,
    GRAMMAR_CORRECTIONS,
    GRAMMAR_PROMPTS,
    PROCEDURES,
    PROCEDURE_PROMPTS
)
from logger import logger


def build_constraints_dataset(*, config, ds_id, seed, count, transforms):
    logger.info(f'Generating synthetic constraints dataset...')

    current_dir = Path(__file__).resolve().parent.parent.parent

    target_dir = current_dir / ds_id
    target_dir.mkdir(parents=True, exist_ok=True)
    data_filename = target_dir / 'constraints.jsonl'

    if data_filename.exists():
        logger.warning(f'Synthetic constraints dataset raw source already exists: {data_filename} \nDelete this file manually to regenerate it.')
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

    def generate_comma_list_with_three_items():
        category = rng.choice(list(LIST_CATEGORIES.keys()))
        items = rng.sample(LIST_CATEGORIES[category], 3)

        user_content = rng.choice(COMMA_LIST_PROMPTS['three']).format(category=category)
        assistant_content = ', '.join(items)

        return row(user_content, assistant_content)

    def generate_one_sentence_answer():
        topic = rng.choice(list(ONE_SENTENCE_TOPICS.keys()))
        answer = rng.choice(ONE_SENTENCE_TOPICS[topic])

        user_content = rng.choice(ONE_SENTENCE_PROMPTS).format(topic=topic)
        assistant_content = answer

        return row(user_content, assistant_content)

    def generate_rewrite():
        bad, good = rng.choice(REWRITES)

        user_content = rng.choice(REWRITE_PROMPTS).format(bad=bad)
        assistant_content = good

        return row(user_content, assistant_content)

    def generate_grammar_correction():
        bad, good = rng.choice(GRAMMAR_CORRECTIONS)

        user_content = rng.choice(GRAMMAR_PROMPTS).format(bad=bad)
        assistant_content = good

        return row(user_content, assistant_content)

    def generate_three_step_procedure():
        task, steps = rng.choice(PROCEDURES)

        user_content = rng.choice(PROCEDURE_PROMPTS).format(task=task)
        assistant_content = '\n'.join(
            f'{i + 1}. {step}' for i, step in enumerate(steps)
        )

        return row(user_content, assistant_content)

    groups = [
        (generate_comma_list_with_three_items, 0.20),
        (generate_one_sentence_answer, 0.20),
        (generate_rewrite, 0.20),
        (generate_grammar_correction, 0.20),
        (generate_three_step_procedure, 0.20)
    ]

    remaining = count

    for group_idx, (generator_fn, weight) in enumerate(groups):
        if group_idx == len(groups) - 1:
            group_count = remaining
        else:
            group_count = round(count * weight)
            remaining -= group_count

        for _ in range(group_count):
            examples.append(generator_fn())

    rng.shuffle(examples)

    save_jsonl_file(data_filename, examples)
    logger.info(f'Synthetic constraints dataset completed and stored at: {data_filename}')
