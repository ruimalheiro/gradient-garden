from datasets_preparation.synthetic.common import generate_dataset
from datasets_preparation.synthetic.instruct.common import row
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


def generator_fn(*, config, rng, count, transforms):
    def make_fixture_generator(fixtures):
        def generate_fixture_example():
            user_content, assistant_content = rng.choice(fixtures)
            return row(user_content, assistant_content)
        return generate_fixture_example

    return generate_weighted_group_examples(
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

def build_general_tasks_dataset(*, config, ds_id, seed, count, transforms):
    return generate_dataset(
        config=config,
        ds_id=ds_id,
        seed=seed,
        count=count,
        transforms=transforms,
        label='General Tasks',
        file_name='general_tasks',
        generator_fn=generator_fn
    )
