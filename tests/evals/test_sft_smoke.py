import pytest

from evals.custom_sft_smoke.checkers import (
    CHECKERS,
    check_exact_match,
    check_non_empty,
    check_no_role_leak,
    check_comma_list_count,
    check_numbered_list_count,
    check_contains_all,
    check_max_words,
    check_not_near_copy
)


@pytest.mark.parametrize(
    ('response', 'target', 'normalize', 'expected'),
    [
        ('Yes.', ['yes'], ['strip', 'lower', 'strip_punct'], True),
        ('He does not like carrots.', ["He doesn't like carrots.", 'He does not like carrots.'], ['strip'], True),
        ('yes, it is', ['yes'], ['strip', 'lower', 'strip_punct'], False),
    ],
)
def test_check_exact_match(response, target, normalize, expected):
    assert check_exact_match(response, target, normalize) is expected

@pytest.mark.parametrize(
    ('response', 'expected'),
    [
        ('hello', True),
        ('  hello  ', True),
        ('', False),
        ('   \n\t', False)
    ],
)
def test_check_non_empty(response, expected):
    assert check_non_empty(response) is expected

@pytest.mark.parametrize(
    ('response', 'expected'),
    [
        ('Assistant: Sure, here is the answer.', False),
        (' user: hello', False),
        ('<|assistant|> yes', False),
        ('Hi there', True)
    ],
)
def test_check_no_role_leak(response, expected):
    assert check_no_role_leak(response) is expected

@pytest.mark.parametrize(
    ('response', 'n', 'expected'),
    [
        ('apple, banana, orange', 3, True),
        ('red, blue, green, yellow', 4, True),
        ('apple, banana, orange, grape', 4, True),
        ('apple, banana', 3, False),
        ('apple, banana, orange, grape', 3, False),
        ('Here are three fruits: apple, banana, orange', 3, False)
    ],
)
def test_check_comma_list_count(response, n, expected):
    assert check_comma_list_count(response, n) is expected

@pytest.mark.parametrize(
    ('response', 'n', 'expected'),
    [
        ('1. Brush your teeth\n2. Rinse your mouth\n3. Smile', 3, True),
        ('1) Boil water\n2) Add tea\n3) Wait\n4) Serve', 4, True),
        ('- Brush your teeth\n- Rinse your mouth\n- Smile', 3, False),
        ('Here are the steps:\n1. Brush\n2. Rinse\n3. Smile', 3, False)
    ],
)
def test_check_numbered_list_count(response, n, expected):
    assert check_numbered_list_count(response, n) is expected

@pytest.mark.parametrize(
    ('response', 'must_contain', 'case_sensitive', 'expected'),
    [
        ('Mia missed one train but caught another train later.', ['Mia', 'Train'], False, True),
        ('Mia missed one train but caught another train later.', ['Mia', 'Train'], True, False),
        ('The bakery sold out of bread before noon..', ['bakery', 'bread'], True, True),
        ('Mia packed her bag and left.', ['Mia', 'train'], False, False),
    ],
)
def test_check_contains_all(response, must_contain, case_sensitive, expected):
    assert check_contains_all(response, must_contain, case_sensitive) is expected

@pytest.mark.parametrize(
    ('response', 'max_words', 'expected'),
    [
        ('hello,world', 2, True),
        ('one.two.three', 3, True),
        ("don't stop", 2, True),
        ('well-written text', 2, True),
        ('     ', 0, True),
        ('Mia caught the train.', 4, True),
        ('Mia caught the train.', 3, False),
        ('Mia packed her bag and caught the next train later.', 10, True),
        ('Mia packed her bag and caught the next train later.', 5, False),
    ],
)
def test_check_max_words(response, max_words, expected):
    assert check_max_words(response, max_words) is expected

@pytest.mark.parametrize(
    ('response', 'source', 'max_similarity', 'min_words', 'expected'),
    [
        ('The thing was kind of bad because the parts did not work together well.', 'The thing was kind of bad because the parts did not work together well.', 0.85, 3, False),
        ('The parts worked poorly together, which made the result ineffective.', 'The thing was kind of bad because the parts did not work together well.', 0.85, 3, True),
        ('OK', 'The thing was kind of bad because the parts did not work together well.', 0.85, 3, False),
        ('OK, the components did not work well together which made the result less effective', 'The thing was kind of bad because the parts did not work together well.', 0.85, 3, True),
    ],
)
def test_check_not_near_copy(response, source, max_similarity, min_words, expected):
    assert check_not_near_copy(response, source, max_similarity, min_words) is expected

def test_checkers_registry_contains_expected_supported_ids():
    expected = {
        'exact_match',
        'non_empty',
        'no_role_leak',
        'comma_list_count',
        'numbered_list_count',
        'contains_all',
        'max_words',
        'not_near_copy'
    }

    assert set(CHECKERS) == expected
    assert all(callable(fn) for fn in CHECKERS.values())
