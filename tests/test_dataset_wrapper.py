from itertools import islice
from datasets_preparation.utils.dataset_wrapper import DatasetSourceWrapper, DatasetWrapper
from recipes.config import MixStrategy


class MockDatasetSourceWrapper(DatasetSourceWrapper):
    def __init__(
        self,
        source_key,
        size,
        documents_seen=0,
        start_document=0
    ):
        self.source_key = source_key
        self.documents_seen = documents_seen
        self.start_document = start_document
        self.parquet_cursor = None
        self.yield_count = 0

        items = [
            {
                'source': source_key,
                'id': f'{source_key}-{i}'
            }
            for i in range(size)
        ]

        # Simulate the real DatasetSourceWrapper, where physical position = start_document + committed documents_seen.
        offset = start_document + documents_seen
        self.dataset = items[offset:]

    def __iter__(self):
        for item in self.dataset:
            self.yield_count += 1
            yield item

def make_wrapper(
    *,
    a_seen=0,
    b_seen=0,
    a_start=0,
    b_start=0,
    a_size=100,
    b_size=100,
    documents_seen=0,
    mix_position=0,
    probabilities=[0.6, 0.4],
    mix_strategy=MixStrategy.LEGACY_INTERLEAVE
):
    sources = [
        MockDatasetSourceWrapper(
            source_key='a',
            size=a_size,
            documents_seen=a_seen,
            start_document=a_start
        ),
        MockDatasetSourceWrapper(
            source_key='b',
            size=b_size,
            documents_seen=b_seen,
            start_document=b_start
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
    assert wrapper.mix_position == 8

    # Simulate multiprocessing prefetch. The producer yields another 5 documents, but the parent has not committed them yet.
    prefetched = list(islice(iterator, 5))

    assert len(prefetched) == 5

    # Yielding must not mutate committed state.
    assert wrapper.documents_seen == 8
    assert wrapper.mix_position == 8
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
    assert wrapper.mix_position == 7

    # Simulate multiprocessing prefetch. The producer yields another 6 documents, but the parent has not committed them yet.
    prefetched = list(islice(iterator, 6))

    assert len(prefetched) == 6

    # Yielding must not mutate committed state.
    assert wrapper.documents_seen == 7
    assert wrapper.mix_position == 7
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

def test_dataset_wrapper_token_budget_completed_source_is_not_consumed():
    wrapper = make_wrapper(
        probabilities=None,
        mix_strategy=MixStrategy.TOKEN_BUDGET
    )
    iterator = iter(wrapper)

    # Consume one full round.
    assert next(iterator)['id'] == 'a-0'
    assert next(iterator)['id'] == 'b-0'

    assert wrapper.sources['a'].yield_count == 1
    assert wrapper.sources['b'].yield_count == 1

    # B has now reached its token target.
    wrapper.mark_source_complete('b')

    # Next A slot still consumes a real document.
    assert next(iterator)['id'] == 'a-1'

    # Next B slot becomes a control event and must not consume b-1.
    completed = next(iterator)

    assert completed == {
        'source': 'b',
        'completed': True
    }

    assert wrapper.sources['a'].yield_count == 2
    assert wrapper.sources['b'].yield_count == 1

    # And this remains true on later B slots.
    assert next(iterator)['id'] == 'a-2'
    completed = next(iterator)

    assert completed == {
        'source': 'b',
        'completed': True
    }
    assert wrapper.sources['b'].yield_count == 1

def test_dataset_wrapper_token_budget_source_exhaustion_does_not_stop_other_sources():
    wrapper = make_wrapper(
        a_size=10,
        b_size=1,
        probabilities=None,
        mix_strategy=MixStrategy.TOKEN_BUDGET
    )
    iterator = iter(wrapper)

    assert next(iterator)['id'] == 'a-0'
    assert next(iterator)['id'] == 'b-0'
    assert next(iterator)['id'] == 'a-1'

    exhausted = next(iterator)

    assert exhausted == {
        'source': 'b',
        'exhausted': True
    }

    # A must continue even though B physically exhausted.
    assert next(iterator)['id'] == 'a-2'

    # Future B positions remain exhaustion control slots.
    exhausted = next(iterator)

    assert exhausted == {
        'source': 'b',
        'exhausted': True
    }

    assert next(iterator)['id'] == 'a-3'

def test_dataset_wrapper_token_budget_exhausted_source_is_not_consumed_again():
    wrapper = make_wrapper(
        a_size=10,
        b_size=1,
        probabilities=None,
        mix_strategy=MixStrategy.TOKEN_BUDGET
    )
    iterator = iter(wrapper)

    next(iterator)  # a-0
    next(iterator)  # b-0
    next(iterator)  # a-1

    first_exhausted = next(iterator)

    assert first_exhausted['exhausted'] is True
    assert 'b' in wrapper.exhausted_sources
    assert wrapper.sources['b'].yield_count == 1

    # Go through several more logical positions.
    docs = list(islice(iterator, 6))

    assert wrapper.sources['b'].yield_count == 1

    assert [
        doc.get('exhausted', False)
        for doc in docs
        if doc['source'] == 'b'
    ] == [True, True, True]

def test_dataset_wrapper_token_budget_completed_source_preserves_logical_position_on_resume():
    wrapper = make_wrapper(
        a_seen=2,
        b_seen=2,
        documents_seen=4,
        mix_position=5,
        probabilities=None,
        mix_strategy=MixStrategy.TOKEN_BUDGET
    )

    # Simulate shard_and_tokenize reconstructing completion from persisted source_train_token_counts.
    wrapper.mark_source_complete('b')

    iterator = iter(wrapper)

    # mix_position=5 is B's logical slot.
    completed = next(iterator)

    assert completed == {
        'source': 'b',
        'completed': True
    }

    # Logical position 6 is A again, and physical A resumes from a-2.
    doc = next(iterator)

    assert doc['source'] == 'a'
    assert doc['id'] == 'a-2'

    # B has not been physically consumed after resume.
    assert wrapper.sources['b'].yield_count == 0

def test_dataset_wrapper_supports_independent_source_start_documents():
    wrapper = make_wrapper(
        a_start=5,
        b_start=0,
        probabilities=None,
        mix_strategy=MixStrategy.TOKEN_BUDGET
    )

    docs = list(islice(wrapper, 6))

    assert [doc['id'] for doc in docs] == [
        'a-5',
        'b-0',
        'a-6',
        'b-1',
        'a-7',
        'b-2'
    ]

def test_dataset_wrapper_resume_preserves_independent_start_documents():
    a_start = 5
    b_start = 20

    wrapper = make_wrapper(
        a_start=a_start,
        b_start=b_start,
        probabilities=None,
        mix_strategy=MixStrategy.TOKEN_BUDGET
    )

    iterator = iter(wrapper)

    prefix = []

    for _ in range(6):
        doc = next(iterator)
        prefix.append(doc)

        wrapper.advance()
        wrapper.commit(doc['source'])

    assert [doc['id'] for doc in prefix] == [
        'a-5',
        'b-20',
        'a-6',
        'b-21',
        'a-7',
        'b-22'
    ]

    assert wrapper.sources['a'].documents_seen == 3
    assert wrapper.sources['b'].documents_seen == 3
    assert wrapper.documents_seen == 6
    assert wrapper.mix_position == 6

    resumed_wrapper = make_wrapper(
        a_start=a_start,
        b_start=b_start,
        a_seen=wrapper.sources['a'].documents_seen,
        b_seen=wrapper.sources['b'].documents_seen,
        documents_seen=wrapper.documents_seen,
        mix_position=wrapper.mix_position,
        probabilities=None,
        mix_strategy=MixStrategy.TOKEN_BUDGET
    )

    resumed = list(islice(resumed_wrapper, 4))

    assert [doc['id'] for doc in resumed] == [
        'a-8',
        'b-23',
        'a-9',
        'b-24'
    ]
