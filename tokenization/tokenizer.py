from tokenization.hf_tokenizer import HFTokenizer
from tokenization.tik_tokenizer import TikTokenizer


def init_tokenizer(*, path, system_prompt, is_huggingface_tokenizer=True, hf_token=None):
    if is_huggingface_tokenizer:
        return HFTokenizer(path, system_prompt, hf_token)
    return TikTokenizer(path, system_prompt)
