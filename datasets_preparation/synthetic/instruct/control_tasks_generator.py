from datasets_preparation.synthetic.common import generate_dataset
from datasets_preparation.synthetic.instruct.common import row
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


def generator_fn(*, config, rng, count, transforms):
    def make_fixture_generator(fixtures):
        def generate_fixture_example():
            user_content, assistant_content = rng.choice(fixtures)
            return row(user_content, assistant_content)
        return generate_fixture_example

    return generate_weighted_group_examples(
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

def build_control_tasks_dataset(*, config, ds_id, seed, count, transforms):
    return generate_dataset(
        config=config,
        ds_id=ds_id,
        seed=seed,
        count=count,
        transforms=transforms,
        label='Control Tasks',
        file_name='control_tasks',
        generator_fn=generator_fn
    )
