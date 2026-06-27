from tokenization.base import BaseTokenizer
from transformers import AutoTokenizer


class HFTokenizer(BaseTokenizer):
    def __init__(self, path, system_prompt, hf_token):
        self.model = AutoTokenizer.from_pretrained(path, token=hf_token)
        self.model.model_max_length = int(1e30)
        self.system_prompt = system_prompt

        if self.model.pad_token_id is None:
            self.model.pad_token = self.model.eos_token

        self.pad_id = self.model.pad_token_id
        self.pad_token = self.model.pad_token

        self.vocab_size = len(self.model)

        self.bos_id = self.model.bos_token_id
        self.bos_token = self.model.bos_token
        self.eos_id = self.model.eos_token_id
        self.eos_token = self.model.eos_token

        self.stop_tokens = {self.eos_id}

    def encode(self, text, add_special_tokens=False):
        return self.model.encode(text, add_special_tokens=add_special_tokens)

    def decode(self, tokens, skip_special_tokens=False):
        return self.model.decode(tokens, skip_special_tokens=skip_special_tokens)
