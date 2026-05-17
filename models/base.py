import torch
import torch.nn as nn

from dataclasses import dataclass
from abc import ABC, abstractmethod
from metrics import ModelMetrics


class BaseModel(nn.Module, ABC):
    def __init__(self, *, config, pad_token_id: int, vocab_size: int, ignore_index: int):
        super().__init__()
        self.config = config
        self.pad_token_id = pad_token_id
        self.vocab_size = vocab_size
        self.ignore_index = ignore_index

    @abstractmethod
    def forward(self, *args, **kwargs) -> dict:
        ...

    def get_input_embeddings(self):
        ...

    def get_output_embeddings(self):
        ...

    def get_total_parameters_count(self) -> int:
        return sum(p.numel() for p in self.parameters())

    def get_trainable_parameters_count(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def get_named_trainable_parameters(self):
        return [(n, p) for n, p in self.named_parameters() if p.requires_grad]

    def prepare_metrics(self) -> None:
        pass

    def collect_metrics(self) -> ModelMetrics:
        return ModelMetrics()
