from tokenization.base import BaseTokenizer
from transformers import AutoTokenizer


class HFTokenizer(BaseTokenizer):
    def __init__(self, path, system_prompt, hf_token):
        self.num_reserved_special_tokens = 256
        self.model = AutoTokenizer.from_pretrained(
            path,
            token=hf_token
        )
        self.model.model_max_length = int(1e30)
        self.system_prompt = system_prompt

        update_tokens = []
        for token in [
            '<|begin_of_text|>',
            '<|end_of_text|>',
            '<|start_header_id|>',
            '<|end_header_id|>',
            '<|eot_id|>',
            '<|reserved_special_token_0|>'
        ]:
            if token not in self.model.get_vocab():
                update_tokens.append(token)

        if update_tokens:
            self.model.add_special_tokens({'additional_special_tokens': update_tokens})

        self.model.bos_token = '<|begin_of_text|>'
        self.model.bos_token_id = self.model.convert_tokens_to_ids(self.model.bos_token)
        self.model.eos_token = '<|end_of_text|>'
        self.model.eos_token_id = self.model.convert_tokens_to_ids(self.model.eos_token)
        self.model.pad_token = '<|reserved_special_token_0|>'
        self.model.pad_token_id = self.model.convert_tokens_to_ids(self.model.pad_token)

        self.vocab_size = len(self.model)

        self.bos_id = self.model.bos_token_id
        self.eos_id = self.model.eos_token_id
        self.sh_id = self.model.convert_tokens_to_ids('<|start_header_id|>')
        self.eh_id = self.model.convert_tokens_to_ids('<|end_header_id|>')
        self.eot_id = self.model.convert_tokens_to_ids('<|eot_id|>')
        self.pad_id = self.model.pad_token_id

        self.stop_tokens = {
            self.eos_id,
            self.eot_id,
        }

    def encode(
        self,
        text,
        *,
        bos=False,
        eos=False,
        **kw
    ):
        tokens = self.model.encode(text, add_special_tokens=False)
        if bos: tokens.insert(0, self.bos_id)
        if eos: tokens.append(self.eos_id)
        return tokens

    def decode(self, tokens):
        return self.model.decode(tokens, skip_special_tokens=False)
