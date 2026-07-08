import torch

from transformers import AutoConfig, AutoModelForCausalLM
from config import ModelConfig
from models.base import BaseModel
from logger import logger


class HFModelWrapper(BaseModel):
    def __init__(
        self,
        *,
        config: ModelConfig,
        pad_token_id: int,
        vocab_size: int,
        ignore_index: int,
        hf_token: str
    ):
        super().__init__(
            config=config,
            pad_token_id=pad_token_id,
            vocab_size=vocab_size,
            ignore_index=ignore_index,
        )

        self.validate_config(config)

        if config.hf_config.random_init:
            logger.warning('"random_init" flag set. The weights will be randomly initialized.')
            self.inner = AutoModelForCausalLM.from_config(AutoConfig.from_pretrained(config.hf_config.model_name, token=hf_token), token=hf_token)
        else:
            self.inner = AutoModelForCausalLM.from_pretrained(config.hf_config.model_name, token=hf_token)
        if self.inner.config.vocab_size != vocab_size:
            raise ValueError(
                f'Tokenizer vocab_size={vocab_size} != HF model vocab_size={self.inner.config.vocab_size}. '
                'You must pick a compatible tokenizer.'
            )

        self.hf_config = self.inner.config

        self.hf_config.pad_token_id = pad_token_id
        if getattr(self.inner, 'generation_config', None) is not None:
            self.inner.generation_config.pad_token_id = pad_token_id

        self.max_seq_len = getattr(self.hf_config, 'max_position_embeddings', config.max_seq_len)
        self.n_layers = getattr(self.hf_config, 'num_hidden_layers', None)
        self.n_heads = getattr(self.hf_config, 'num_attention_heads', None)
        self.dim = getattr(self.hf_config, 'hidden_size', None)
        self.n_kv_heads = getattr(self.hf_config, 'num_key_value_heads', self.n_heads)

    @classmethod
    def validate_config(cls, config: ModelConfig):
        if config.hf_config is None:
            raise ValueError('Cannot use hf_wrapper architecture without model.hf_config.')
        if config.hf_config.model_name is None:
            raise ValueError('Cannot use hf_wrapper architecture without model.hf_config.model_name.')

    def get_input_embeddings(self):
        return self.inner.get_input_embeddings()

    def get_output_embeddings(self):
        return self.inner.get_output_embeddings()

    def forward(self, input_ids, labels=None, attention_mask=None, **kwargs):
        if attention_mask is None:
            attention_mask = (input_ids != self.pad_token_id).long()

        if labels is not None:
            # Our labels are shifted by default... So we need to unshift because HF expects unshifted.
            # Unshift: original = [-100] + shifted[:, :-1]
            original_labels = torch.full_like(labels, self.ignore_index)
            original_labels[:, 1:] = labels[:, :-1]
            labels = original_labels

        out = self.inner(input_ids=input_ids, labels=labels, attention_mask=attention_mask, **kwargs)
        return {
            'logits': out.logits,
            'loss': out.loss,
        }
