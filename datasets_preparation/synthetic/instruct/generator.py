
from datasets_preparation.synthetic.common import (
    make_fixture_dataset_generator,
    generate_dataset
)
from datasets_preparation.synthetic.group_utils import generate_weighted_group_examples
from datasets_preparation.synthetic.instruct.common import (
    render_fixture_example,
    instruct_dedupe_key
)
from datasets_preparation.synthetic.instruct.fixtures.identity import IDENTITY_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.factual_qa import FACTUAL_QA_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.common_sense_qa import COMMON_SENSE_QA_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.yes_no import YES_NO_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.social_replies import SOCIAL_REPLY_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.polite_refusals import POLITE_REFUSAL_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.procedures import PROCEDURE_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.grammar import GRAMMAR_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.rewrites import REWRITE_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.sentence_transforms import SENTENCE_TRANSFORM_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.summaries import SUMMARY_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.simple_explanations import SIMPLE_EXPLANATION_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.one_sentence import ONE_SENTENCE_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.lists import LIST_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.exact_word_count import EXACT_WORD_COUNT_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.non_repetition import NON_REPETITION_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.text_classification import TEXT_CLASSIFICATION_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.extraction import EXTRACTION_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.basic_arithmetic import BASIC_ARITHMETIC_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.rhymes import RHYME_FIXTURES


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
            0.021,
            default_weights={
                'self_identification': 0.32,
                'human_yes_no': 0.12,
                'human_or_ai': 0.08,
                'role': 0.18,
                'name_brief': 0.10,
                'name_only': 0.10,
                'other_assistant': 0.10,
            },
            variables={
                'model_name': model_name,
                'identity_message': identity_message,
            },
            override_group_answer=override_group_answer,
        ),
        make_generator(
            'factual_qa',
            FACTUAL_QA_FIXTURES,
            0.073,
            default_weights={
                'capital': 0.16,
                'science': 0.15,
                'solar_system': 0.10,
                'counts': 0.08,
                'authors_art': 0.12,
                'animals': 0.08,
                'geography': 0.08,
                'objects_body_plants': 0.08,
                'opposites': 0.06,
                'one_word_factual': 0.06,
                'health_safety': 0.03
            }
        ),
        make_generator('common_sense_qa', COMMON_SENSE_QA_FIXTURES, 0.034),
        make_generator('yes_no', YES_NO_FIXTURES, 0.030),
        make_generator(
            'social_replies',
            SOCIAL_REPLY_FIXTURES,
            0.094,
            default_weights={
                'affirmative_scheduling': 0.22,
                'thanks': 0.12,
                'apology_ack': 0.12,
                'celebration': 0.17,
                'supportive_nervous': 0.15,
                'cancellation_ack': 0.10,
                'request_ack': 0.12,
            },
        ),
        make_generator('polite_refusals', POLITE_REFUSAL_FIXTURES, 0.021),
        make_generator(
            'procedures',
            PROCEDURE_FIXTURES,
            0.056,
            default_weights={
                'three_step': 0.70,
                'strict_eval_tasks': 0.30
            }
        ),
        make_generator('grammar', GRAMMAR_FIXTURES, 0.038),
        make_generator(
            'rewrites',
            REWRITE_FIXTURES,
            0.081,
            default_weights={
                'redundancy_removal': 0.20,
                'concise_rewrite': 0.22,
                'natural_paraphrase': 0.22,
                'high_edit_distance': 0.20,
                'bad_because_not_good': 0.16,
            },
        ),
        make_generator(
            'sentence_transforms',
            SENTENCE_TRANSFORM_FIXTURES,
            0.060,
            default_weights={
                'question_statement': 0.24,
                'statement_question': 0.12,
                'tense': 0.11,
                'present_tense': 0.08,
                'number': 0.09,
                'singular': 0.07,
                'polarity': 0.09,
                'positive': 0.06,
                'style': 0.05,
                'casual_style': 0.04,
                'combine_split': 0.03,
                'split': 0.02
            }
        ),
        make_generator(
            'summaries',
            SUMMARY_FIXTURES,
            0.060,
            default_weights={
                'one_sentence': 0.26,
                'short_summary': 0.24,
                'five_words_or_fewer': 0.18,
                'headline': 0.12,
                'key_point': 0.12,
                'two_sentence_summary': 0.08,
            },
        ),
        make_generator(
            'simple_explanations',
            SIMPLE_EXPLANATION_FIXTURES,
            0.030,
            default_weights={
                'technology': 0.50,
                'general_science': 0.30,
                'everyday_concepts': 0.20,
            },
        ),
        make_generator(
            'one_sentence',
            ONE_SENTENCE_FIXTURES,
            0.056,
            default_weights={
                'topics': 0.75,
                'must_include_words': 0.25
            }
        ),
        make_generator(
            'lists',
            LIST_FIXTURES,
            0.038,
            default_weights={
                'dedup': 0.40,
                'sampled_categories': 0.60,
            },
        ),
        make_generator(
            'exact_word_count',
            EXACT_WORD_COUNT_FIXTURES,
            0.047,
            default_weights={
                'one_word': 0.25,
                'two_words': 0.12,
                'three_words': 0.13,
                'four_words': 0.13,
                'five_words': 0.17,
                'six_words': 0.10,
                'seven_words': 0.10
            }
        ),
        make_generator(
            'non_repetition',
            NON_REPETITION_FIXTURES,
            0.051,
            default_weights={
                'numbered_two_reasons': 0.18,
                'numbered_three_reasons': 0.18,
                'bullet_points': 0.18,
                'comma_lists_four': 0.18,
                'comma_lists_five': 0.12,
                'comma_examples_three': 0.16
            }
        ),
        make_generator(
            'text_classification',
            TEXT_CLASSIFICATION_FIXTURES,
            0.056,
            default_weights={
                'sentiment': 0.60,
                'topic': 0.25,
                'yes_no_question_type': 0.15
            }
        ),
        make_generator(
            'extraction',
            EXTRACTION_FIXTURES,
            0.056,
            default_weights={
                'name': 0.16,
                'city': 0.16,
                'date': 0.09,
                'number': 0.10,
                'email': 0.07,
                'color': 0.08,
                'animal': 0.08,
                'food': 0.08,
                'country': 0.08,
                'month': 0.05,
                'time': 0.05
            }
        ),
        make_generator(
            'basic_arithmetic',
            BASIC_ARITHMETIC_FIXTURES,
            0.051,
            default_weights={
                'addition': 0.24,
                'subtraction': 0.16,
                'multiplication': 0.14,
                'division': 0.10,
                'comparison': 0.12,
                'smaller_comparison': 0.10,
                'symbolic_answer_only': 0.14
            }
        ),
        make_generator(
            'rhymes',
            RHYME_FIXTURES,
            0.047,
            default_weights={
                'exactly_four_unique': 0.40,
                'exactly_three_unique': 0.12,
                'exactly_five_unique': 0.12,
                'no_repeats_explicit': 0.26,
                'comma_format_only': 0.10,
            },
        ),
    ]

    return generate_weighted_group_examples(
        groups=dict(groups),
        transforms=transforms,
        count=count,
        dedupe_key_fn=instruct_dedupe_key,
        rng=rng
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
