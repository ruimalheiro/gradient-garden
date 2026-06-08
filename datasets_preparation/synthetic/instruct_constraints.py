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
    PROCEDURE_PROMPTS,
    ANCHOR_CONSTRAINT_EXAMPLES,
    FRIENDLY_REPLIES,
    ONE_SENTENCE_SUMMARIES,
    SIMPLE_EXPLANATIONS
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

    def generate_friendly_reply():
        message, reply = rng.choice(FRIENDLY_REPLIES)

        templates = [
            'Write one short friendly reply to this message:\n{message}',
            'Reply briefly and kindly to this message:\n{message}',
            'Write a friendly one-sentence response:\n{message}',
            'Give a short friendly reply:\n{message}',
        ]

        return row(rng.choice(templates).format(message=message), reply)

    def generate_one_sentence_summary():
        text, summary = rng.choice(ONE_SENTENCE_SUMMARIES)

        templates = [
            'Summarize this in one sentence:\n{text}',
            'Write a one-sentence summary of this:\n{text}',
            'Summarize the following text in exactly one sentence:\n{text}',
            'Give a brief one-sentence summary:\n{text}',
        ]

        return row(rng.choice(templates).format(text=text), summary)

    def generate_simple_explanation():
        prompt, answer = rng.choice(SIMPLE_EXPLANATIONS)
        return row(prompt, answer)

    groups = [
        (generate_rewrite, 0.20),
        (generate_grammar_correction, 0.15),
        (generate_three_step_procedure, 0.15),
        (generate_comma_list_with_three_items, 0.125),
        (generate_one_sentence_answer, 0.125),
        (generate_friendly_reply, 0.10),
        (generate_one_sentence_summary, 0.075),
        (generate_simple_explanation, 0.075)
    ]

    for user_content, assistant_content in ANCHOR_CONSTRAINT_EXAMPLES:
        if len(examples) >= count:
            break
        examples.append(row(user_content, assistant_content))

    remaining_to_generate = max(count - len(examples), 0)
    remaining = remaining_to_generate

    for group_idx, (generator_fn, weight) in enumerate(groups):
        if group_idx == len(groups) - 1:
            group_count = remaining
        else:
            group_count = round(remaining_to_generate * weight)
            remaining -= group_count

        for _ in range(group_count):
            examples.append(generator_fn())

    rng.shuffle(examples)

    save_jsonl_file(data_filename, examples)
    logger.info(f'Synthetic constraints dataset completed and stored at: {data_filename}')
