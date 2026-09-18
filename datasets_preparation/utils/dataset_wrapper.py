from datasets import load_dataset
from huggingface_hub import HfApi, HfFileSystem
from datasets_preparation.utils.parquet_search import (
    load_dataset_with_search_parquet,
    advance_parquet_cursor
)
from datasets_preparation.utils.state import PreparationState
from datasets_preparation.utils.common import stable_hash
from logger import logger


class DatasetSourceWrapper:
    def __init__(
        self,
        *,
        ds_id,
        name,
        source_key,
        split,
        resolved_revision,
        start_document,
        token,
        state: PreparationState,
        max_datapoints=None,
        search_parquet=False,
        num_proc=None
    ):
        self.ds_id = ds_id
        self.name = name
        self.source_key = source_key
        self.split = split
        self.resolved_revision = resolved_revision
        self.start_document = start_document
        self.max_datapoints = max_datapoints
        self.search_parquet = search_parquet

        self.documents_seen = 0

        self.hf_api = None
        self.hf_file_system = None
        self.parquet_row_count_cache = None
        self.parquet_files = None
        self.parquet_cursor = None

        # Loading state
        source_state = state.source_states.get(source_key)
        if source_state is not None:
            self.load_state_dict(source_state)

        hf_name = None if name == 'default' else name

        if search_parquet is True:
            logger.info(f'The "search_parquet" flag is set. Using parquet loader...')

            self.hf_api = HfApi(token=token)
            self.hf_file_system = HfFileSystem(token=token)
            self.parquet_row_count_cache = {}

            resume_document = self.start_document + self.documents_seen

            self.dataset, self.parquet_files, self.parquet_cursor = load_dataset_with_search_parquet(
                ds_id=ds_id,
                split=split,
                streaming=True,
                revision=resolved_revision,
                start_document=resume_document,
                token=token,
                hf_api=self.hf_api,
                hf_file_system=self.hf_file_system,
                num_proc=num_proc,
                cursor=self.parquet_cursor
            )
        else:
            self.dataset = load_dataset(
                ds_id,
                name=hf_name,
                split=split,
                streaming=True,
                revision=resolved_revision,
                token=token
            )

            offset = self.start_document + self.documents_seen

            if offset > 0:
                logger.info(f'Skipping {offset:,} documents for {source_key} (start={self.start_document:,}, committed={self.documents_seen:,})')
                self.dataset = self.dataset.skip(offset)

        if max_datapoints is not None:
            max_datapoints = int(max_datapoints)
            assert max_datapoints > 0

            remaining_datapoints = max_datapoints - self.documents_seen
            self.dataset = self.dataset.take(max(0, remaining_datapoints))

        state.source_states[source_key] = self.state_dict()

    @property
    def metadata(self):
        return {
            'dataset_id': self.ds_id,
            'name': self.name,
            'split': self.split,
            'revision': self.resolved_revision,
            'start_document': self.start_document,
            'search_parquet': self.search_parquet
        }

    def __iter__(self):
        yield from self.dataset

    def commit(self, n_documents=1):
        if n_documents < 0:
            raise ValueError('n_documents must be >= 0')

        if self.parquet_cursor is not None:
            if self.hf_file_system is None:
                raise ValueError('hf file system was not initialized...')

            self.parquet_cursor = advance_parquet_cursor(
                ds_id=self.ds_id,
                revision=self.resolved_revision,
                files=self.parquet_files,
                cursor=self.parquet_cursor,
                n_documents=n_documents,
                hf_file_system=self.hf_file_system,
                row_count_cache=self.parquet_row_count_cache
            )

        self.documents_seen += n_documents

    def state_dict(self):
        return {
            'source_key': self.source_key,
            'documents_seen': self.documents_seen
        }

    def load_state_dict(self, state):
        if self.source_key != state['source_key']:
            raise ValueError(f'Source mismatch: expected {self.source_key!r}, got {state["source_key"]!r}')
        if state['documents_seen'] < 0:
            raise ValueError('documents_seen must be >= 0')
        self.documents_seen = state['documents_seen']

    @property
    def column_names(self):
        return self.dataset.column_names

    def map(self, *args, **kwargs):
        self.dataset = self.dataset.map(*args, **kwargs)
        return self

class DatasetWrapper:
    def __init__(
        self,
        sources: list[DatasetSourceWrapper],
        probabilities,
        seed,
        stopping_strategy,
        documents_seen=0
    ):
        if stopping_strategy != 'first_exhausted':
            raise ValueError(f'Pretraining custom interleave currently only supports "first_exhausted", got {stopping_strategy!r}')

        logger.info(f'Using interleaving strategy: {stopping_strategy}')

        self.sources = { source.source_key: source for source in sources }
        self.source_keys = list(self.sources.keys())
        self.probabilities = probabilities
        self.seed = seed
        self.stopping_strategy = stopping_strategy
        self.documents_seen = documents_seen

    def _select_source(self, logical_index):
        # Deterministic weighted source selection from the global logical index. This avoids persisting mutable RNG state.
        x = stable_hash(str(logical_index), seed=self.seed) / (1 << 64)

        acc = 0.0
        for source_key, probability in zip(self.source_keys, self.probabilities):
            acc += probability
            if x < acc:
                return source_key

        return self.source_keys[-1]

    def __iter__(self):
        iterators = { source_key: iter(source) for source_key, source in self.sources.items() }

        logical_index = self.documents_seen

        while True:
            source_key = self._select_source(logical_index)

            try:
                doc = next(iterators[source_key])
            except StopIteration:
                return

            yield doc
            logical_index += 1

    def commit(self, source_key, n_documents=1):
        self.sources[source_key].commit(n_documents)
        self.documents_seen += n_documents

    def state_dict(self):
        return { source_key: source.state_dict() for source_key, source in self.sources.items() }
