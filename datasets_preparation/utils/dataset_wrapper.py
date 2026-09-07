from datasets import load_dataset
from datasets_preparation.utils.parquet_search import load_dataset_with_search_parquet


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
        max_datapoints=None,
        search_parquet=False,
        num_proc=None,
    ):
        self.source_key = source_key
        self.documents_seen = start_document

        self.metadata = {
            'dataset_id': ds_id,
            'name': name,
            'split': split,
            'revision': resolved_revision,
            'start_document': start_document,
            'search_parquet': search_parquet
        }

        hf_name = None if name == 'default' else name

        if search_parquet is True:
            self.dataset = load_dataset_with_search_parquet(
                ds_id=ds_id,
                split=split,
                streaming=True,
                revision=resolved_revision,
                start_document=start_document,
                token=token,
                num_proc=num_proc
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

            if start_document > 0:
                logger.info(f'Skipping {start_document:,} documents for {source_key}')
                ds = ds.skip(start_document)

        if max_datapoints is not None:
            max_datapoints = int(max_datapoints)
            assert max_datapoints > 0
            self.dataset = self.dataset.take(max_datapoints)

    def metadata(self):
        return self.metadata

    def __iter__(self):
        yield from self.dataset

    def commit(self, n_documents=1):
        if n_documents < 0:
            raise ValueError('n_documents must be >= 0')
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
    def __init__(self, sources: list[DatasetSourceWrapper]):
        self.sources = sources

    def __iter__(self):
        yield from self.sources

    def commit(self):
        pass

    def state_dict(self):
        pass
