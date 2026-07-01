import pytest

from evals.ifeval.checkers import (
    CHECKERS,
    check_end_checker,
    check_english_capital,
    check_english_lowercase,
    check_forbidden_words,
    check_json_format,
    check_keyword_frequency,
    check_keywords_existence,
    check_letter_frequency,
    check_no_comma,
    check_number_bullet_lists,
    check_number_highlighted_sections,
    check_number_paragraphs,
    check_number_placeholders,
    check_number_words,
    check_postscript,
    check_quotation,
    check_repeat_prompt,
    check_title,
    check_two_responses,
    compare_count,
    count_keyword_occurrences,
)


@pytest.mark.parametrize(
    ('value', 'relation', 'target', 'expected'),
    [
        (3, None, 3, True),
        (3, None, 4, False),
        (3, 'exactly', 3, True),
        (3, 'exactly', 2, False),
        (3, 'at least', 2, True),
        (3, 'at least', 4, False),
        (3, 'at most', 3, True),
        (3, 'at most', 2, False),
        (3, 'less than', 4, True),
        (3, 'less than', 3, False),
        (3, 'more than', 2, True),
        (3, 'more than', 3, False),
    ],
)
def test_compare_count(value, relation, target, expected):
    assert compare_count(value=value, relation=relation, target=target) is expected

def test_compare_count_invalid_relation_raises():
    with pytest.raises(ValueError, match='Unsupported relation'):
        compare_count(value=3, relation='around', target=3)

@pytest.mark.parametrize(
    ('response', 'expected'),
    [
        ('This has no comma', True),
        ('This has one, comma', False),
        ('', True),
    ],
)
def test_check_no_comma(response, expected):
    assert check_no_comma(response) is expected

def test_check_number_placeholders_at_least_default():
    response = '[name]\n[address]\n[email]'
    assert check_number_placeholders(response, num_placeholders=3) is True
    assert check_number_placeholders(response, num_placeholders=4) is False

def test_check_number_placeholders_exactly():
    response = '[name] [address] [email]'
    assert check_number_placeholders(response, num_placeholders=3, relation='exactly') is True
    assert check_number_placeholders(response, num_placeholders=2, relation='exactly') is False

def test_check_number_placeholders_ignores_empty_and_multiline_brackets():
    response = '[] [valid] [not\nvalid]'
    assert check_number_placeholders(response, num_placeholders=1, relation='exactly') is True

def test_check_number_bullet_lists_exact_default():
    response = '* First\n* Second\n* Third'
    assert check_number_bullet_lists(response, num_bullets=3) is True
    assert check_number_bullet_lists(response, num_bullets=2) is False

def test_check_number_bullet_lists_allows_leading_whitespace():
    response = '  * First\n    * Second\n* Third'
    assert check_number_bullet_lists(response, num_bullets=3) is True

def test_check_number_bullet_lists_requires_star_space_format():
    response = '- First\n- Second\n- Third'
    assert check_number_bullet_lists(response, num_bullets=3) is False

def test_check_title_double_angle_brackets():
    assert check_title('<<Resignation Notice>>\nDear manager,') is True
    assert check_title('<Resignation Notice>\nDear manager,') is False
    assert check_title('Resignation Notice\nDear manager,') is False

def test_check_title_does_not_match_multiline_title():
    assert check_title('<<Bad\nTitle>>') is False

def test_check_repeat_prompt_strict_prefix():
    prompt_to_repeat = 'Write an email to my boss telling him that I am quitting.'

    assert (
        check_repeat_prompt(
            'Write an email to my boss telling him that I am quitting.\n\n<<Title>>',
            prompt_to_repeat=prompt_to_repeat,
        )
        is True
    )

    assert (
        check_repeat_prompt(
            'Sure. Write an email to my boss telling him that I am quitting.\n\n<<Title>>',
            prompt_to_repeat=prompt_to_repeat,
        )
        is False
    )

@pytest.mark.parametrize(
    ('response', 'expected'),
    [
        ('what are the boys doing?', True),
        ('what are the boys doing? 123!', True),
        ('What are the boys doing?', False),
        ('WHAT ARE THE BOYS DOING?', False),
        ('123 !!!', False),
    ],
)
def test_check_english_lowercase(response, expected):
    assert check_english_lowercase(response) is expected

@pytest.mark.parametrize(
    ('response', 'expected'),
    [
        ('THIS IS ALL CAPS!', True),
        ('THIS IS ALL CAPS 123!', True),
        ('This Is Mixed Case', False),
        ('this is lowercase', False),
        ('123 !!!', False),
    ],
)
def test_check_english_capital(response, expected):
    assert check_english_capital(response) is expected

def test_check_keywords_existence_case_insensitive():
    response = 'The story mentions a river and a castle.'
    assert check_keywords_existence(response, keywords=['story', 'RIVER']) is True
    assert check_keywords_existence(response, keywords=['story', 'mountain']) is False

def test_check_forbidden_words_with_forbidden_words():
    response = 'The answer uses safe words only.'
    assert check_forbidden_words(response, forbidden_words=['banana', 'orange']) is True
    assert check_forbidden_words(response, forbidden_words=['safe']) is False

def test_check_forbidden_words_with_keywords_fallback():
    response = 'The answer uses safe words only.'
    assert check_forbidden_words(response, keywords=['banana']) is True
    assert check_forbidden_words(response, keywords=['answer']) is False

def test_check_forbidden_words_empty_list_passes():
    assert check_forbidden_words('anything') is True

def test_check_end_checker_strips_outer_whitespace():
    assert check_end_checker('Hello world.\n', end_phrase='world.') is True
    assert check_end_checker('Hello world!', end_phrase='world.') is False

@pytest.mark.parametrize(
    ('response', 'expected'),
    [
        ('"A quoted response."', True),
        (' "A quoted response." ', True),
        ('A quoted response.', False),
        ("'single quotes are not enough'", False),
        ('"missing end quote', False),
    ],
)
def test_check_quotation(response, expected):
    assert check_quotation(response) is expected

def test_check_number_words_exact_default():
    assert check_number_words('one two three', num_words=3) is True
    assert check_number_words('one two three', num_words=2) is False

def test_check_number_words_with_relation():
    assert check_number_words('one two three four', num_words=3, relation='at least') is True
    assert check_number_words('one two', num_words=3, relation='at least') is False
    assert check_number_words('one two', num_words=3, relation='less than') is True

def test_check_number_words_counts_hyphen_and_apostrophe_words():
    response = "don't stop the well-made plan"
    assert check_number_words(response, num_words=5) is True

def test_check_json_format_plain_json_object():
    assert check_json_format('{"answer": 42}') is True

def test_check_json_format_plain_json_array():
    assert check_json_format('[1, 2, 3]') is True

def test_check_json_format_fenced_json():
    response = """```json
{"answer": 42}
```"""
    assert check_json_format(response) is True

def test_check_json_format_fenced_without_language():
    response = """```
{"answer": 42}
```"""
    assert check_json_format(response) is True

def test_check_json_format_invalid_json():
    assert check_json_format("{answer: 42}") is False

def test_check_two_responses_requires_exactly_two_nonempty_parts():
    assert check_two_responses('First response ****** Second response') is True
    assert check_two_responses('First response******Second response') is True
    assert check_two_responses('First response') is False
    assert check_two_responses('First ****** Second ****** Third') is False
    assert check_two_responses('First ****** ') is False

def test_check_postscript_default_marker():
    assert check_postscript('Main text\n\nP.S. One more thing.') is True
    assert check_postscript('Main text\n\np.s. One more thing.') is True
    assert check_postscript('Main text only.') is False

def test_check_postscript_custom_marker():
    assert check_postscript('Main text\n\nPS: One more thing.', postscript_marker='PS:') is True
    assert check_postscript('Main text\n\nP.S. One more thing.', postscript_marker='PS:') is False

def test_check_number_highlighted_sections_at_least_default():
    response = '*One*\nSome text\n*Two*\nSome text\n*Three*'
    assert check_number_highlighted_sections(response, num_highlights=3) is True
    assert check_number_highlighted_sections(response, num_highlights=4) is False

def test_check_number_highlighted_sections_counts_bold():
    response = '**One**\n**Two**'
    assert check_number_highlighted_sections(response, num_highlights=2) is True

def test_check_number_highlighted_sections_exactly():
    response = '*One*\n*Two*\n*Three*'
    assert (
        check_number_highlighted_sections(
            response,
            num_highlights=3,
            relation='exactly',
        )
        is True
    )
    assert (
        check_number_highlighted_sections(
            response,
            num_highlights=2,
            relation='exactly',
        )
        is False
    )

def test_count_keyword_occurrences_word_keyword_uses_word_boundaries():
    response = 'story Story storybook backstory story'
    assert count_keyword_occurrences(response, 'story') == 3

def test_count_keyword_occurrences_symbol_keyword_uses_substring_count():
    response = 'Wow!!! Really!!'
    assert count_keyword_occurrences(response, "!") == 5

def test_check_keyword_frequency_with_keyword():
    response = 'The story is a short story about another story.'
    assert check_keyword_frequency(response, keyword='story', frequency=3) is True
    assert check_keyword_frequency(response, keyword='story', frequency=2) is False

def test_check_keyword_frequency_with_keywords_fallback():
    response = 'The story is a short story.'
    assert check_keyword_frequency(response, keywords=['story'], frequency=2) is True

def test_check_keyword_frequency_with_relation():
    response = 'story story story'
    assert check_keyword_frequency(response, keyword='story', frequency=2, relation='at least') is True
    assert check_keyword_frequency(response, keyword='story', frequency=4, relation='less than') is True

def test_check_keyword_frequency_missing_keyword_raises():
    with pytest.raises(ValueError, match='Missing keyword/keywords'):
        check_keyword_frequency('response', frequency=1)

def test_check_letter_frequency_alpha_case_insensitive():
    response = 'Taco Truck'
    assert check_letter_frequency(response, letter='t', let_frequency=2) is True

def test_check_letter_frequency_symbol_case_sensitive_not_relevant():
    response = 'Wow!!! Really!!'
    assert check_letter_frequency(response, letter='!', let_frequency=5) is True

def test_check_letter_frequency_with_relation():
    response = 'banana'
    assert check_letter_frequency(response, letter='a', let_frequency=3, let_relation='exactly') is True
    assert check_letter_frequency(response, letter='a', let_frequency=2, let_relation='more than') is True
    assert check_letter_frequency(response, letter='z', let_frequency=1, let_relation='less than') is True

def test_check_letter_frequency_rejects_multi_character_letter():
    with pytest.raises(ValueError, match='Expected a single character'):
        check_letter_frequency('hello', letter='ll', let_frequency=1)

def test_check_number_paragraphs_blank_line_default():
    response = 'Paragraph one.\n\nParagraph two.\n\nParagraph three.'
    assert check_number_paragraphs(response, num_paragraphs=3) is True
    assert check_number_paragraphs(response, num_paragraphs=2) is False

def test_check_number_paragraphs_with_section_spliter():
    response = 'Paragraph one.***Paragraph two.***Paragraph three.'
    assert (
        check_number_paragraphs(
            response,
            num_paragraphs=3,
            section_spliter='***',
        )
        is True
    )

def test_check_number_paragraphs_ignores_empty_parts_with_splitter():
    response = 'Paragraph one.***   ***Paragraph two.'
    assert (
        check_number_paragraphs(
            response,
            num_paragraphs=2,
            section_spliter='***',
        )
        is True
    )

def test_check_number_paragraphs_empty_response():
    assert check_number_paragraphs('', num_paragraphs=0) is True
    assert check_number_paragraphs('', num_paragraphs=1) is False

def test_checkers_registry_contains_expected_supported_ids():
    expected = {
        'punctuation:no_comma',
        'detectable_content:number_placeholders',
        'detectable_format:number_bullet_lists',
        'detectable_format:title',
        'combination:repeat_prompt',
        'change_case:english_lowercase',
        'keywords:existence',
        'keywords:forbidden_words',
        'startend:end_checker',
        'startend:quotation',
        'length_constraints:number_words',
        'detectable_format:json_format',
        'combination:two_responses',
        'change_case:english_capital',
        'detectable_content:postscript',
        'detectable_format:number_highlighted_sections',
        'keywords:frequency',
        'keywords:letter_frequency',
        'length_constraints:number_paragraphs',
    }

    assert set(CHECKERS) == expected
    assert all(callable(fn) for fn in CHECKERS.values())
