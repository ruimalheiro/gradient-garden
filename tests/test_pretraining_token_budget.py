import numpy as np
import pytest
import datasets_preparation.utils.shard_writer as shard_writer_module

from datasets_preparation.utils.common import stable_hash
from datasets_preparation.utils.dataset_wrapper import DatasetWrapper
from datasets_preparation.utils.shard_writer import shard_and_tokenize
from datasets_preparation.utils.state import PreparationState
from recipes.config import MixStrategy


class MockSource:
    def __init__(self, source_key, docs, target_tokens):
        self.source_key = source_key
        self.dataset = docs
        self.target_tokens = target_tokens
        self.documents_seen = 0

    def __iter__(self):
        yield from self.dataset

    def commit(self, n_documents=1):
        self.documents_seen += n_documents

    def state_dict(self):
        return {
            'source_key': self.source_key,
            'documents_seen': self.documents_seen,
            'parquet_cursor': None
        }

class FakeEvent:
    def __init__(self):
        self._set = False

    def set(self):
        self._set = True

    def is_set(self):
        return self._set

class FakePool:
    def __init__(self, *_args, **_kwargs):
        pass

    def imap(self, func, iterable, chunksize=1):
        for item in iterable:
            yield func(item)

    def close(self):
        pass

    def join(self):
        pass

def make_state(tmp_path):
    state_dir = tmp_path / '.prep_state'
    state_dir.mkdir()

    return PreparationState(
        path=str(state_dir / 'state.json'),
        status='preparing',
        documents_seen=0,
        mix_position=0,
        source_metadata={},
        source_states={},
        source_doc_counts={},
        source_token_counts={},
        source_train_token_counts={},
        split_doc_counts={
            'train': 0,
            'val': 0
        },
        split_token_counts={
            'train': 0,
            'val': 0
        },
        train_writer_state={},
        train_writer_buffer_file_path=str(state_dir / 'train_buffer.npy'),
        val_writer_state={},
        val_writer_buffer_file_path=str(state_dir / 'val_buffer.npy')
    )

def make_dataset(*, a_docs, b_docs, a_target, b_target):
    return DatasetWrapper(
        sources=[
            MockSource(
                source_key='a',
                docs=a_docs,
                target_tokens=a_target
            ),
            MockSource(
                source_key='b',
                docs=b_docs,
                target_tokens=b_target
            )
        ],
        probabilities=None,
        seed=42,
        mix_strategy=MixStrategy.TOKEN_BUDGET,
        stopping_strategy='first_exhausted'
    )

def fake_tokenize(_tokenizer_kwargs, doc):
    return np.asarray(doc['tokens'], dtype=np.uint32)

def find_texts_for_split(
    *,
    seed,
    validation_ratio,
    split,
    count
):
    hash_space = 1 << 64
    threshold = int(validation_ratio * hash_space)

    texts = []

    for i in range(1000):
        text = f'doc-{i}'
        is_val = stable_hash(text, seed=seed, hash_bytes=8) < threshold

        matches_split = (split == 'val' and is_val) or (split == 'train' and not is_val)

        if matches_split:
            texts.append(text)

        if len(texts) == count:
            return texts

    raise RuntimeError(f'Could not find {count} texts for split {split!r}')

def test_token_budget_uses_train_tokens_and_allows_whole_doc_overshoot(
    tmp_path,
    monkeypatch
):
    monkeypatch.setattr(
        shard_writer_module.mp,
        'Pool',
        FakePool
    )
    monkeypatch.setattr(
        shard_writer_module.mp,
        'Event',
        FakeEvent
    )

    seed = 42
    validation_ratio = 0.5

    [val_text] = find_texts_for_split(
        seed=seed,
        validation_ratio=validation_ratio,
        split='val',
        count=1
    )

    train_texts = find_texts_for_split(
        seed=seed,
        validation_ratio=validation_ratio,
        split='train',
        count=4
    )

    dataset = make_dataset(
        a_target=5,
        b_target=7,
        a_docs=[
            {
                'source': 'a',
                'text': val_text,
                'tokens': [1, 2, 3, 4]
            },
            {
                'source': 'a',
                'text': train_texts[0],
                'tokens': [5, 6, 7]
            },
            {
                'source': 'a',
                'text': train_texts[1],
                'tokens': [8, 9, 10, 11]
            }
        ],
        b_docs=[
            {
                'source': 'b',
                'text': train_texts[2],
                'tokens': [12, 13, 14, 15]
            },
            {
                'source': 'b',
                'text': train_texts[3],
                'tokens': [16, 17, 18, 19]
            }
        ]
    )

    state = make_state(tmp_path)

    shard_and_tokenize(
        seed=seed,
        dataset=dataset,
        tokenize_function=fake_tokenize,
        tokenizer_kwargs={},
        train_path=str(tmp_path / 'train'),
        val_path=str(tmp_path / 'val'),
        shard_file_prefix='data',
        shard_size=100,
        train_mix_target_tokens=None,
        validation_ratio=validation_ratio,
        num_proc=1,
        chunksize=1,
        state=state
    )

    assert state.status == 'completed'

    # Source A:
    # - 4 validation tokens, which do not advance its target
    # - 3 + 4 = 7 train tokens against a target of 5
    #
    # Source B:
    # - 4 + 4 = 8 train tokens against a target of 7
    #
    # The final train document is written whole, so both sources overshoot.
    assert state.source_train_token_counts == {
        'a': 7,
        'b': 8
    }

    # source_token_counts includes both train and validation.
    assert state.source_token_counts == {
        'a': 11,
        'b': 8
    }

    assert state.split_token_counts == {
        'train': 15,
        'val': 4
    }

    assert state.split_doc_counts == {
        'train': 4,
        'val': 1
    }

    assert dataset.sources['a'].documents_seen == 3
    assert dataset.sources['b'].documents_seen == 2

    assert 'a' in dataset.completed_sources
    assert 'b' in dataset.completed_sources

def test_token_budget_fails_when_source_exhausts_before_target(
    tmp_path,
    monkeypatch
):
    monkeypatch.setattr(
        shard_writer_module.mp,
        'Pool',
        FakePool
    )
    monkeypatch.setattr(
        shard_writer_module.mp,
        'Event',
        FakeEvent
    )

    dataset = make_dataset(
        a_target=3,
        b_target=10,
        a_docs=[
            {
                'source': 'a',
                'text': 'a-0',
                'tokens': [1, 2, 3, 4]
            }
        ],
        b_docs=[
            {
                'source': 'b',
                'text': 'b-0',
                'tokens': [5, 6, 7, 8]
            }
        ]
    )

    state = make_state(tmp_path)

    with pytest.raises(
        RuntimeError,
        match='b=4/10'
    ):
        shard_and_tokenize(
            seed=42,
            dataset=dataset,
            tokenize_function=fake_tokenize,
            tokenizer_kwargs={},
            train_path=str(tmp_path / 'train'),
            val_path=str(tmp_path / 'val'),
            shard_file_prefix='data',
            shard_size=100,
            train_mix_target_tokens=None,
            validation_ratio=0.0,
            num_proc=1,
            chunksize=1,
            state=state
        )

    assert state.status == 'exhausted_before_target'

    assert state.source_train_token_counts == {
        'a': 4,
        'b': 4
    }

    assert state.source_token_counts == {
        'a': 4,
        'b': 4
    }

    assert dataset.sources['a'].documents_seen == 1
    assert dataset.sources['b'].documents_seen == 1

    # A satisfied its target with whole-document overshoot.
    assert 'a' in dataset.completed_sources

    # B physically exhausted before satisfying its target.
    assert 'b' in dataset.exhausted_sources
    assert 'b' not in dataset.completed_sources
