from datasets import Dataset
from datasets_preparation.data_preparation_utils import (
    compute_stats,
    token_budget_dataset_mix,
)


def make_dataset(source, supervised_tokens):
    return Dataset.from_dict({
        'row_id': [
            f'{source}-{i}'
            for i in range(len(supervised_tokens))
        ],
        'source': [source] * len(supervised_tokens),
        'total_tokens': [
            token_count + 5
            for token_count in supervised_tokens
        ],
        'supervised_tokens': supervised_tokens
    })

def test_token_budget_mix_respects_source_targets():
    dataset_a = make_dataset('a', [5] * 100)
    dataset_b = make_dataset('b', [5] * 100)

    mixed = token_budget_dataset_mix(
        datasets=[dataset_a, dataset_b],
        weights=[0.75, 0.25],
        target_tokens=100,
        seed=42
    )

    stats = compute_stats(mixed)

    assert stats['sources']['a']['supervised_tokens'] == 75
    assert stats['sources']['b']['supervised_tokens'] == 25

    assert stats['sources']['a']['examples'] == 15
    assert stats['sources']['b']['examples'] == 5

    assert stats['total_supervised_tokens'] == 100

def test_token_budget_mix_allows_final_example_overshoot():
    dataset = make_dataset(
        'a',
        [10, 20, 30, 40, 50, 60]
    )

    target_tokens = 45

    mixed = token_budget_dataset_mix(
        datasets=[dataset],
        weights=[1.0],
        target_tokens=target_tokens,
        seed=42
    )

    selected_tokens = sum(mixed['supervised_tokens'])

    assert selected_tokens >= target_tokens
    assert selected_tokens < (
        target_tokens + max(dataset['supervised_tokens'])
    )

def test_token_budget_mix_is_deterministic():
    dataset = make_dataset(
        'a',
        [10] * 20
    )

    mixed_a = token_budget_dataset_mix(
        datasets=[dataset],
        weights=[1.0],
        target_tokens=50,
        seed=42
    )

    mixed_b = token_budget_dataset_mix(
        datasets=[dataset],
        weights=[1.0],
        target_tokens=50,
        seed=42
    )

    assert mixed_a['row_id'] == mixed_b['row_id']

def test_token_budget_mix_selects_from_shuffled_dataset():
    dataset = make_dataset(
        'a',
        [10] * 20,
    )

    seed = 42
    target_tokens = 30

    shuffled = dataset.shuffle(seed=seed)

    # All examples contain 10 supervised tokens, so reaching
    # a target of 30 must select exactly the first 3 shuffled rows.
    expected_row_ids = shuffled.select(range(3))['row_id']

    mixed = token_budget_dataset_mix(
        datasets=[dataset],
        weights=[1.0],
        target_tokens=target_tokens,
        seed=seed
    )

    assert mixed['row_id'] == expected_row_ids

def test_token_budget_mix_uses_all_available_data_when_source_exhausts():
    dataset = make_dataset(
        'a',
        [10, 20]
    )

    mixed = token_budget_dataset_mix(
        datasets=[dataset],
        weights=[1.0],
        target_tokens=100,
        seed=42
    )

    assert len(mixed) == 2
    assert sum(mixed['supervised_tokens']) == 30

def test_compute_stats():
    dataset = Dataset.from_dict({
        'source': ['a', 'a', 'b'],
        'total_tokens': [10, 20, 40],
        'supervised_tokens': [5, 10, 20]
    })

    stats = compute_stats(dataset)

    assert stats['total_examples'] == 3
    assert stats['total_tokens'] == 70
    assert stats['total_supervised_tokens'] == 35

    assert stats['sources']['a'] == {
        'examples': 2,
        'total_tokens': 30,
        'supervised_tokens': 15,
        'examples %': '66.67%',
        'tokens %': '42.86%',
        'supervised_tokens %': '42.86%'
    }

    assert stats['sources']['b'] == {
        'examples': 1,
        'total_tokens': 40,
        'supervised_tokens': 20,
        'examples %': '33.33%',
        'tokens %': '57.14%',
        'supervised_tokens %': '57.14%'
    }
