from datasets_preparation.synthetic.common import generate_dataset
from datasets_preparation.synthetic.instruct.common import row
from datasets_preparation.synthetic.group_utils import generate_weighted_group_examples
from datasets_preparation.synthetic.instruct.fixtures.constraints import (
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


def generator_fn(*, config, rng, count, transforms):
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

    anchor_idx = 0 # cycle anchors to improve coverage deterministically...
    def generate_anchor_constraint():
        nonlocal anchor_idx

        user_content, assistant_content = ANCHOR_CONSTRAINT_EXAMPLES[
            anchor_idx % len(ANCHOR_CONSTRAINT_EXAMPLES)
        ]
        anchor_idx += 1

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

    return generate_weighted_group_examples(
        groups={
            'lists': (generate_comma_list_with_three_items, 0.10),
            'one_sentence_answers': (generate_one_sentence_answer, 0.10),
            'rewrites': (generate_rewrite, 0.30),
            'grammar': (generate_grammar_correction, 0.125),
            'procedures': (generate_three_step_procedure, 0.19),
            'anchors': (generate_anchor_constraint, 0.01),
            'friendly_replies': (generate_friendly_reply, 0.075),
            'one_sentence_summaries': (generate_one_sentence_summary, 0.05),
            'simple_explanations': (generate_simple_explanation, 0.05)
        },
        transforms=transforms,
        count=count
    )

def build_constraints_dataset(*, config, ds_id, seed, count, transforms):
    return generate_dataset(
        config=config,
        ds_id=ds_id,
        seed=seed,
        count=count,
        transforms=transforms,
        label='Constraints',
        file_name='constraints',
        generator_fn=generator_fn
    )
