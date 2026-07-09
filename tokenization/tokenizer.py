from tokenization.hf_tokenizer import HFTokenizer
from config import TokenizerPromptFormat


def init_tokenizer(
    *,
    path,
    system_prompt,
    is_huggingface_tokenizer=True,
    hf_token=None,
    prompt_format=TokenizerPromptFormat.GRADIENT_GARDEN
):
    if is_huggingface_tokenizer is True:
        return HFTokenizer(path, system_prompt, hf_token, prompt_format)
    raise ValueError('Currently only HF tokenizer is supported.')
