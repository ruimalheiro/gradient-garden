class PretrainingSource:
    def __init__(self, *, dataset, source_key, documents_seen=0):
        self.dataset = dataset,
        self.source_key = source_key,
        self.documents_seen = documents_seen

    def __iter__(self):
        for doc in self.dataset:
            yield doc

    def commit(self, n_documents=1):
        self.documents_seen += n_documents

    def state_dict(self):
        return {
            'source_key': self.source_key,
            'documents_seen': self.documents_seen
        }

    def load_state_dict(self, state):
        if self.source_key != state['source_key']:
            raise ValueError(f'Source mismatch: expected {self.source_key!r}, got {state["source_key"]!r}')
        self.documents_seen = state['documents_seen']

class PretrainingDataset:
    pass
