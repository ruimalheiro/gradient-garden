from dataclasses import dataclass


@dataclass
class PreparationState:
    path: str
    status: str
    documents_seen: int
    mix_position: int
    source_metadata: dict
    source_states: dict
    source_doc_counts: dict
    source_token_counts: dict
    source_train_token_counts: dict
    split_doc_counts: dict
    split_token_counts: dict
    train_writer_state: dict
    train_writer_buffer_file_path: str
    val_writer_state: dict
    val_writer_buffer_file_path: str
