import torch
import torch.nn as nn
from transformers import AutoModelForCausalLM
from models.base import BaseModel
from config import ModelConfig


class HFModelWrapper(BaseModel):
    def __init__(self, *, config: ModelConfig, pad_token_id: int, vocab_size: int, ignore_index: int):
        super().__init__(
            config=config,
            pad_token_id=pad_token_id,
            vocab_size=vocab_size,
            ignore_index=ignore_index,
        )

        if config.model_name is None:
            raise ValueError('Cannot use hf_wrapper architecture without providing a model path to load.')

        self.inner = AutoModelForCausalLM.from_pretrained(config.model_name)
        self.inner.resize_token_embeddings(vocab_size)

        self.config = self.inner.config
        self.config.max_seq_len = self.inner.config.max_position_embeddings
        self.config.n_layers = self.inner.config.num_hidden_layers
        self.config.n_heads = self.inner.config.num_attention_heads
        self.config.dim = self.inner.config.hidden_size
        self.config.n_kv_heads = self.inner.config.num_key_value_heads
        self.pad_token_id = self.inner.config.pad_token_id
        self.vocab_size = self.inner.config.vocab_size

    @classmethod
    def validate_config(cls, config: ModelConfig):
        pass

    def get_input_embeddings(self):
        return self.inner.get_input_embeddings()

    def get_output_embeddings(self):
        return self.inner.get_output_embeddings()

    def forward(self, input_ids, labels=None, **kwargs):
        out = self.inner(input_ids=input_ids, labels=labels)
        return {
            'logits': out.logits,
            'loss': out.loss,
        }
