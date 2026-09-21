from itertools import islice
from datasets_preparation.utils.dataset_wrapper import DatasetSourceWrapper, DatasetWrapper
from recipes.config import MixStrategy


class MockDatasetSourceWrapper(DatasetSourceWrapper):
    def __init__(
        self,
        source_key,
        size,
        documents_seen=0
    ):
        self.source_key = source_key
        self.documents_seen = documents_seen
        self.parquet_cursor = None

        items = [
            {
                'source': source_key,
                'id': f'{source_key}-{i}'
            }
            for i in range(size)
        ]

        # Simulate the real DatasetSourceWrapper, where self.dataset is already positioned at the committed resume offset.
        self.dataset = items[documents_seen:]

def make_wrapper(
    *,
    a_seen=0,
    b_seen=0,
    documents_seen=0,
    mix_position=0,
    probabilities=[0.6, 0.4],
    mix_strategy=MixStrategy.LEGACY_INTERLEAVE
):
    sources = [
        MockDatasetSourceWrapper(
            source_key='a',
            size=100,
            documents_seen=a_seen
        ),
        MockDatasetSourceWrapper(
            source_key='b',
            size=100,
            documents_seen=b_seen
        ),
    ]

    return DatasetWrapper(
        sources=sources,
        probabilities=probabilities,
        seed=42,
        mix_strategy=mix_strategy,
        stopping_strategy='first_exhausted',
        documents_seen=documents_seen,
        mix_position=mix_position
    )

def test_dataset_wrapper_resume_matches_uninterrupted_sequence():
    # Generate a reference sequence without interruption.
    full_wrapper = make_wrapper()
    expected = list(islice(full_wrapper, 20))

    # Simulate a run that commits the first 8 documents.
    wrapper = make_wrapper()
    iterator = iter(wrapper)

    prefix = []

    for _ in range(8):
        doc = next(iterator)
        prefix.append(doc)

        wrapper.advance()
        wrapper.commit(doc['source'])

    assert prefix == expected[:8]

    # Capture the state that would be persisted in a checkpoint.
    a_seen = wrapper.sources['a'].documents_seen
    b_seen = wrapper.sources['b'].documents_seen
    documents_seen = wrapper.documents_seen
    mix_position = wrapper.mix_position

    assert a_seen + b_seen == documents_seen
    assert documents_seen == 8

    # Reconstruct the dataset exactly as a resumed preparation would.
    resumed_wrapper = make_wrapper(
        a_seen=a_seen,
        b_seen=b_seen,
        documents_seen=documents_seen,
        mix_position=mix_position
    )

    resumed = list(islice(resumed_wrapper, 12))

    # Resuming must reproduce the exact uninterrupted tail.
    assert resumed == expected[8:20]

def test_dataset_wrapper_resume_uses_committed_not_yielded_position():
    # Reference uninterrupted sequence.
    full_wrapper = make_wrapper()
    expected = list(islice(full_wrapper, 20))

    wrapper = make_wrapper()
    iterator = iter(wrapper)

    # Commit the first 8 documents.
    for _ in range(8):
        doc = next(iterator)
        wrapper.advance()
        wrapper.commit(doc['source'])

    assert wrapper.documents_seen == 8

    # Simulate multiprocessing prefetch. The producer yields another 5 documents, but the parent has not committed them yet.
    prefetched = list(islice(iterator, 5))

    assert len(prefetched) == 5

    # Yielding must not mutate committed state.
    assert wrapper.documents_seen == 8
    assert wrapper.sources['a'].documents_seen + wrapper.sources['b'].documents_seen == 8

    # Recreate from committed state only.
    resumed_wrapper = make_wrapper(
        a_seen=wrapper.sources['a'].documents_seen,
        b_seen=wrapper.sources['b'].documents_seen,
        documents_seen=wrapper.documents_seen,
        mix_position=wrapper.mix_position
    )

    resumed = list(islice(resumed_wrapper, 12))

    # Resume must start from logical position 8, not from the producer's prefetched position 13.
    assert resumed == expected[8:20]

def test_dataset_wrapper_token_budget_uses_round_robin():
    wrapper = make_wrapper(
        probabilities=None,
        mix_strategy=MixStrategy.TOKEN_BUDGET
    )

    docs = list(islice(wrapper, 6))

    assert [doc['source'] for doc in docs] == [
        'a', 'b', 'a', 'b', 'a', 'b'
    ]

def test_dataset_wrapper_resume_matches_uninterrupted_sequence_with_token_budget():
    # Generate a reference sequence without interruption.
    full_wrapper = make_wrapper(
        probabilities=None,
        mix_strategy=MixStrategy.TOKEN_BUDGET
    )
    expected = list(islice(full_wrapper, 20))

    # Simulate a run that commits the first 7 documents.
    wrapper = make_wrapper(
        probabilities=None,
        mix_strategy=MixStrategy.TOKEN_BUDGET
    )
    iterator = iter(wrapper)

    prefix = []

    for _ in range(7):
        doc = next(iterator)
        prefix.append(doc)

        wrapper.advance()
        wrapper.commit(doc['source'])

    assert prefix == expected[:7]

    # Capture the state that would be persisted in a checkpoint.
    a_seen = wrapper.sources['a'].documents_seen
    b_seen = wrapper.sources['b'].documents_seen
    documents_seen = wrapper.documents_seen
    mix_position = wrapper.mix_position

    assert a_seen + b_seen == documents_seen
    assert documents_seen == 7

    # Reconstruct the dataset exactly as a resumed preparation would.
    resumed_wrapper = make_wrapper(
        a_seen=a_seen,
        b_seen=b_seen,
        documents_seen=documents_seen,
        mix_position=mix_position,
        probabilities=None,
        mix_strategy=MixStrategy.TOKEN_BUDGET
    )

    resumed = list(islice(resumed_wrapper, 13))

    # Resuming must reproduce the exact uninterrupted tail.
    assert resumed == expected[7:20]

def test_dataset_wrapper_resume_uses_committed_not_yielded_position_with_token_budget():
    # Reference uninterrupted sequence.
    full_wrapper = make_wrapper(
        probabilities=None,
        mix_strategy=MixStrategy.TOKEN_BUDGET
    )
    expected = list(islice(full_wrapper, 20))

    wrapper = make_wrapper(
        probabilities=None,
        mix_strategy=MixStrategy.TOKEN_BUDGET
    )
    iterator = iter(wrapper)

    # Commit the first 7 documents.
    for _ in range(7):
        doc = next(iterator)
        wrapper.advance()
        wrapper.commit(doc['source'])

    assert wrapper.documents_seen == 7

    # Simulate multiprocessing prefetch. The producer yields another 6 documents, but the parent has not committed them yet.
    prefetched = list(islice(iterator, 6))

    assert len(prefetched) == 6

    # Yielding must not mutate committed state.
    assert wrapper.documents_seen == 7
    assert wrapper.sources['a'].documents_seen + wrapper.sources['b'].documents_seen == 7

    # Recreate from committed state only.
    resumed_wrapper = make_wrapper(
        a_seen=wrapper.sources['a'].documents_seen,
        b_seen=wrapper.sources['b'].documents_seen,
        documents_seen=wrapper.documents_seen,
        mix_position=wrapper.mix_position,
        probabilities=None,
        mix_strategy=MixStrategy.TOKEN_BUDGET
    )

    resumed = list(islice(resumed_wrapper, 13))

    # Resume must start from logical position 7, not from the producer's prefetched position 13.
    assert resumed == expected[7:20]
