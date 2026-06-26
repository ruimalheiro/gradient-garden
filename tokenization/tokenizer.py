from tokenization.hf_tokenizer import HFTokenizer


def init_tokenizer(*, path, system_prompt, is_huggingface_tokenizer=True, hf_token=None):
    if is_huggingface_tokenizer is True:
        return HFTokenizer(path, system_prompt, hf_token)
    raise ValueError('Currently we only support HF tokenizer.')
