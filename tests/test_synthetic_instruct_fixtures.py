import itertools
import random
import pytest

from datasets_preparation.synthetic.common import make_fixture_dataset_generator
from datasets_preparation.synthetic.instruct.common import (
    instruct_dedupe_key,
    render_fixture_example,
    resolve_example_answer,
)
from datasets_preparation.synthetic.instruct.fixtures.basic_arithmetic import BASIC_ARITHMETIC_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.common_sense_qa import COMMON_SENSE_QA_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.exact_word_count import EXACT_WORD_COUNT_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.extraction import EXTRACTION_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.factual_qa import FACTUAL_QA_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.grammar import GRAMMAR_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.identity import IDENTITY_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.lists import LIST_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.non_repetition import NON_REPETITION_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.one_sentence import ONE_SENTENCE_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.polite_refusals import POLITE_REFUSAL_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.procedures import PROCEDURE_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.rewrites import REWRITE_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.rhymes import RHYME_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.sentence_transforms import SENTENCE_TRANSFORM_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.simple_explanations import SIMPLE_EXPLANATION_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.social_replies import SOCIAL_REPLY_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.summaries import SUMMARY_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.text_classification import TEXT_CLASSIFICATION_FIXTURES
from datasets_preparation.synthetic.instruct.fixtures.yes_no import YES_NO_FIXTURES


ALL_FIXTURE_SETS = {
    'identity': IDENTITY_FIXTURES,
    'factual_qa': FACTUAL_QA_FIXTURES,
    'common_sense_qa': COMMON_SENSE_QA_FIXTURES,
    'yes_no': YES_NO_FIXTURES,
    'social_replies': SOCIAL_REPLY_FIXTURES,
    'polite_refusals': POLITE_REFUSAL_FIXTURES,
    'procedures': PROCEDURE_FIXTURES,
    'grammar': GRAMMAR_FIXTURES,
    'rewrites': REWRITE_FIXTURES,
    'sentence_transforms': SENTENCE_TRANSFORM_FIXTURES,
    'summaries': SUMMARY_FIXTURES,
    'simple_explanations': SIMPLE_EXPLANATION_FIXTURES,
    'one_sentence': ONE_SENTENCE_FIXTURES,
    'lists': LIST_FIXTURES,
    'exact_word_count': EXACT_WORD_COUNT_FIXTURES,
    'non_repetition': NON_REPETITION_FIXTURES,
    'text_classification': TEXT_CLASSIFICATION_FIXTURES,
    'extraction': EXTRACTION_FIXTURES,
    'basic_arithmetic': BASIC_ARITHMETIC_FIXTURES,
    'rhymes': RHYME_FIXTURES,
}

TEMPLATE_VARIABLES = {
    'model_name': 'Tendril',
    'identity_message': 'I am Tendril, a helpful AI assistant.',
}

def iter_answer_variants(example):
    """Render every configured answer alternative, not just one random choice."""
    if 'answers' not in example:
        yield dict(example)
        return

    for answer in example['answers']:
        variant = dict(example)
        variant.pop('answers')
        variant['answer'] = answer
        yield variant


def iter_message_variants(messages):
    """Render every message-content alternative in a conversation template."""
    content_options = []

    for message in messages:
        content = message['content']
        options = content if isinstance(content, list) else [content]

        if not options:
            raise AssertionError('Message content alternatives cannot be empty.')

        content_options.append(options)

    for selected_contents in itertools.product(*content_options):
        yield [
            {
                **message,
                'content': selected_content,
            }
            for message, selected_content in zip(
                messages,
                selected_contents,
                strict=True,
            )
        ]

def test_all_fixture_examples_and_template_variants_render():
    rendered_count = 0

    for fixture_set_name, fixtures in ALL_FIXTURE_SETS.items():
        for group_name, fixture in fixtures.items():
            for example_index, source_example in enumerate(
                fixture['examples']
            ):
                for example in iter_answer_variants(source_example):
                    message_templates = (
                        example['messages']
                        if 'messages' in example
                        else fixture['messages']
                    )

                    for messages in iter_message_variants(message_templates):
                        isolated_example = dict(example)
                        isolated_example.pop('messages', None)

                        isolated_fixtures = {
                            group_name: {
                                'messages': messages,
                                'examples': [isolated_example],
                            },
                        }

                        try:
                            result = render_fixture_example(
                                isolated_fixtures,
                                group_name,
                                rng=random.Random(42),
                                variables=TEMPLATE_VARIABLES,
                            )
                        except Exception as exc:
                            pytest.fail(
                                f'Failed to render '
                                f'{fixture_set_name}.{group_name}'
                                f'[{example_index}]: {exc!r}'
                            )

                        assert result['messages']
                        assert all(
                            message['content'].strip()
                            for message in result['messages']
                        )

                        rendered_count += 1

    assert rendered_count > 0

def test_multiturn_conversation_renders_all_messages():
    fixtures = {
        'clarification': {
            'messages': [
                {
                    'role': 'user',
                    'content': 'What foods should I try?',
                },
                {
                    'role': 'assistant',
                    'content': 'Which city are you visiting?',
                },
                {
                    'role': 'user',
                    'content': 'I am visiting {city}.',
                },
                {
                    'role': 'assistant',
                    'content': '{answer}',
                },
            ],
            'examples': [
                {
                    'city': 'Lisbon',
                    'answer': 'Try pastéis de nata.',
                },
            ],
        },
    }

    result = render_fixture_example(
        fixtures,
        'clarification',
        rng=random.Random(42),
    )

    assert result == {
        'messages': [
            {
                'role': 'user',
                'content': 'What foods should I try?',
            },
            {
                'role': 'assistant',
                'content': 'Which city are you visiting?',
            },
            {
                'role': 'user',
                'content': 'I am visiting Lisbon.',
            },
            {
                'role': 'assistant',
                'content': 'Try pastéis de nata.',
            },
        ],
    }

def test_custom_identity_message_is_rendered_exactly():
    result = render_fixture_example(
        IDENTITY_FIXTURES,
        'self_identification',
        rng=random.Random(42),
        variables={
            'model_name': 'Tendril',
            'identity_message': 'I am the custom Tendril assistant.',
        },
    )

    assert result['messages'][-1] == {
        'role': 'assistant',
        'content': 'I am the custom Tendril assistant.',
    }

def test_fixture_generator_forwards_template_variables():
    fixtures = {
        'identity': {
            'messages': [
                {
                    'role': 'user',
                    'content': 'What is your name?',
                },
                {
                    'role': 'assistant',
                    'content': '{model_name}',
                },
            ],
            'examples': [{}],
        },
    }

    generator = make_fixture_dataset_generator(
        fixtures=fixtures,
        rng=random.Random(42),
        render_example=render_fixture_example,
        variables={
            'model_name': 'Tendril',
        },
    )

    assert generator() == {
        'messages': [
            {
                'role': 'user',
                'content': 'What is your name?',
            },
            {
                'role': 'assistant',
                'content': 'Tendril',
            },
        ],
    }

def test_structured_steps_are_numbered():
    answer = resolve_example_answer(
        {
            'steps': [
                'Boil water.',
                'Add the ingredient.',
                'Turn off the heat.',
            ],
        },
        random.Random(42),
    )

    assert answer == (
        '1. Boil water.\n'
        '2. Add the ingredient.\n'
        '3. Turn off the heat.'
    )

def test_structured_items_use_fixture_count_and_separator():
    answer = resolve_example_answer(
        {
            'items': ['red', 'green', 'blue'],
            'count': 3,
            'separator': ' | ',
        },
        random.Random(42),
    )

    assert set(answer.split(' | ')) == {
        'red',
        'green',
        'blue',
    }
    assert answer.count(' | ') == 2

def test_system_message_after_dialogue_is_rejected():
    fixtures = {
        'invalid': {
            'messages': [
                {
                    'role': 'user',
                    'content': 'Hello.',
                },
                {
                    'role': 'system',
                    'content': 'This system message is too late.',
                },
                {
                    'role': 'assistant',
                    'content': 'Hello.',
                },
            ],
            'examples': [{}],
        },
    }

    with pytest.raises(
        ValueError,
        match='System messages must appear before the dialogue',
    ):
        render_fixture_example(
            fixtures,
            'invalid',
            rng=random.Random(42),
        )

def test_example_messages_override_fixture_messages():
    fixtures = {
        'override': {
            'messages': [
                {
                    'role': 'user',
                    'content': 'Fixture-level question.',
                },
                {
                    'role': 'assistant',
                    'content': 'Fixture-level answer.',
                },
            ],
            'examples': [
                {
                    'messages': [
                        {
                            'role': 'user',
                            'content': 'Example-level question.',
                        },
                        {
                            'role': 'assistant',
                            'content': 'Example-level answer.',
                        },
                    ],
                },
            ],
        },
    }

    result = render_fixture_example(
        fixtures,
        'override',
        rng=random.Random(42),
    )

    assert result == {
        'messages': [
            {
                'role': 'user',
                'content': 'Example-level question.',
            },
            {
                'role': 'assistant',
                'content': 'Example-level answer.',
            },
        ],
    }

def test_dedupe_key_includes_every_turn():
    first = {
        'messages': [
            {'role': 'user', 'content': 'Question'},
            {'role': 'assistant', 'content': 'First answer'},
            {'role': 'user', 'content': 'Follow-up'},
            {'role': 'assistant', 'content': 'Final answer'},
        ],
    }
    second = {
        'messages': [
            {'role': 'user', 'content': 'Question'},
            {'role': 'assistant', 'content': 'First answer'},
            {'role': 'user', 'content': 'Different follow-up'},
            {'role': 'assistant', 'content': 'Final answer'},
        ],
    }

    assert instruct_dedupe_key(first) != instruct_dedupe_key(second)
