from tokenization.base import BaseTokenizer
from transformers import AutoTokenizer
from config import TokenizerPromptFormat


class HFTokenizer(BaseTokenizer):
    def __init__(self, path: str, system_prompt: str, hf_token: str, prompt_format: TokenizerPromptFormat):
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

        self.prompt_format = prompt_format

    def encode(self, text, add_special_tokens=False):
        return self.model.encode(text, add_special_tokens=add_special_tokens)

    def decode(self, tokens, skip_special_tokens=False):
        return self.model.decode(tokens, skip_special_tokens=skip_special_tokens)

    def encode_instruct_messages_inference(self, messages):
        if self.prompt_format == TokenizerPromptFormat.HF_CHAT_TEMPLATE:
            return self.model.apply_chat_template(
                messages,
                tokenize=True,
                add_generation_prompt=True,
                return_dict=False,
            )

        return super().encode_instruct_messages_inference(messages)
