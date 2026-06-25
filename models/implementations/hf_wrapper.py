from transformers import AutoModelForCausalLM
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
    ):
        super().__init__(
            config=config,
            pad_token_id=pad_token_id,
            vocab_size=vocab_size,
            ignore_index=ignore_index,
        )

        self.inner = AutoModelForCausalLM.from_pretrained(config.model_name)

        if self.inner.config.vocab_size != vocab_size:
            logger.warning(
                f'Tokenizer vocab_size={vocab_size} does not match HF model '
                f'vocab_size={self.inner.config.vocab_size}. It is recommended to use the matching tokenizer. '
                'Automatically resizing for compatibility... '
            )
            self.inner.resize_token_embeddings(vocab_size)

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
        if config.model_name is None:
            raise ValueError('Cannot use hf_wrapper architecture without model.model_name.')

    def get_input_embeddings(self):
        return self.inner.get_input_embeddings()

    def get_output_embeddings(self):
        return self.inner.get_output_embeddings()

    def forward(self, input_ids, labels=None, **kwargs):
        if 'attention_mask' not in kwargs:
            attention_mask = (input_ids != self.pad_token_id).long()
            kwargs['attention_mask'] = attention_mask
        out = self.inner(input_ids=input_ids, labels=labels, **kwargs)
        return {
            'logits': out.logits,
            'loss': out.loss,
        }
