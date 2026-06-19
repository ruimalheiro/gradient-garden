
from datasets_preparation.synthetic.common import (
    make_fixture_dataset_generator,
    generate_dataset
)
from datasets_preparation.synthetic.group_utils import generate_weighted_group_examples
from datasets_preparation.synthetic.instruct.common import render_fixture_example
from datasets_preparation.synthetic.instruct.fixtures.identity import IDENTITY_FIXTURES

# from datasets_preparation.synthetic.instruct.fixtures.basic_arithmetic import BASIC_ARITHMETIC_FIXTURES
# from datasets_preparation.synthetic.instruct.fixtures.common_sense_qa import COMMON_SENSE_QA_FIXTURES
# from datasets_preparation.synthetic.instruct.fixtures.exact_word_count import EXACT_WORD_COUNT_FIXTURES
# from datasets_preparation.synthetic.instruct.fixtures.extraction import EXTRACTION_FIXTURES
# from datasets_preparation.synthetic.instruct.fixtures.factual_qa import FACTUAL_QA_FIXTURES
# from datasets_preparation.synthetic.instruct.fixtures.grammar import GRAMMAR_FIXTURES
# from datasets_preparation.synthetic.instruct.fixtures.lists import LIST_FIXTURES
# from datasets_preparation.synthetic.instruct.fixtures.non_repetition import NON_REPETITION_FIXTURES
# from datasets_preparation.synthetic.instruct.fixtures.one_sentence import ONE_SENTENCE_FIXTURES
# from datasets_preparation.synthetic.instruct.fixtures.polite_refusals import POLITE_REFUSAL_FIXTURES
# from datasets_preparation.synthetic.instruct.fixtures.procedures import PROCEDURE_FIXTURES
# from datasets_preparation.synthetic.instruct.fixtures.rewrites import REWRITE_FIXTURES
# from datasets_preparation.synthetic.instruct.fixtures.rhymes import RHYME_FIXTURES
# from datasets_preparation.synthetic.instruct.fixtures.sentence_transforms import SENTENCE_TRANSFORM_FIXTURES
# from datasets_preparation.synthetic.instruct.fixtures.simple_explanations import SIMPLE_EXPLANATION_FIXTURES
# from datasets_preparation.synthetic.instruct.fixtures.social_replies import SOCIAL_REPLY_FIXTURES
# from datasets_preparation.synthetic.instruct.fixtures.summaries import SUMMARY_FIXTURES
# from datasets_preparation.synthetic.instruct.fixtures.text_classification import TEXT_CLASSIFICATION_FIXTURES
# from datasets_preparation.synthetic.instruct.fixtures.yes_no import YES_NO_FIXTURES


def generator_fn(*, config, rng, count, transforms):
    def make_generator(group_name, fixtures, weight, *, default_weights=None, variables=None, override_group_answer=None):
        generator = make_fixture_dataset_generator(
            fixtures=fixtures,
            rng=rng,
            render_example=render_fixture_example,
            transforms=transforms.get('groups', {}).get(group_name, {}),
            default_weights=default_weights,
            variables=variables,
            override_group_answer=override_group_answer
        )
        return group_name, (generator, weight)

    custom_identity_message = transforms.get('identity_message')

    model_name = transforms.get(
        'model_name',
        config.model.architecture.value.capitalize(),
    )

    identity_message = custom_identity_message or (
        f'I am {model_name}, a helpful AI assistant.'
    )

    override_group_answer = None
    if custom_identity_message:
        override_group_answer = {
            'self_identification': '{identity_message}',
        }

    groups = [
        make_generator(
            'identity',
            IDENTITY_FIXTURES,
            0.03,
            default_weights={
                'self_identification': 0.40,
                'human': 0.20,
                'role': 0.20,
                'name_only': 0.10,
                'other_assistant': 0.10,
            },
            variables={
                'model_name': model_name,
                'identity_message': identity_message,
            },
            override_group_answer=override_group_answer
        )
    ]

    return generate_weighted_group_examples(
        groups=dict(groups),
        transforms=transforms,
        count=count
    )

def build_instruct_dataset(*, config, ds_id, seed, count, transforms):
    return generate_dataset(
        config=config,
        ds_id=ds_id,
        seed=seed,
        count=count,
        transforms=transforms,
        label='Synthetic instruct',
        file_name='instruct',
        generator_fn=generator_fn,
    )
