import torch

from inference.generation import generate


def test_generate_kv_cache_matches_no_cache_greedy(model, tokenizer, device):
    model.eval()
    torch.manual_seed(0)

    # token ids must be within vocab and not pad/stop ideally
    prompts = [
        [10, 20, 30, 40],
        [11, 22],
        [7, 8, 9]
    ]

    kwargs = dict(
        model=model,
        tokenizer=tokenizer,
        prompt_tokens=prompts,
        max_gen_len=16,
        temperature=0.0,
        top_p=1.0,
        repetition_penalty=None,
        no_repeat_ngram_size=None,
        device=device,
        dtype=torch.float32
    )

    out_no_cache = generate(**kwargs, use_kv_cache=False)
    out_cache = generate(**kwargs, use_kv_cache=True)

    assert out_no_cache == out_cache

def test_generate_batched_variable_lengths_smoke(model, tokenizer, device):
    model.eval()
    torch.manual_seed(0)

    prompts = [
        [10, 11, 12, 13, 14],
        [21, 22],
        [31, 32, 33, 34],
    ]

    max_gen_len = 12

    out = generate(
        model=model,
        tokenizer=tokenizer,
        prompt_tokens=prompts,
        max_gen_len=max_gen_len,
        temperature=0.0,
        top_p=1.0,
        repetition_penalty=None,
        no_repeat_ngram_size=None,
        device=device,
        dtype=torch.float32,
        use_kv_cache=True,
    )

    assert isinstance(out, list)
    assert len(out) == len(prompts)

    for r in out:
        gen_tokens = r['result']
        assert isinstance(gen_tokens, list)
        assert len(gen_tokens) <= max_gen_len

def test_generate_empty_prompt_raises(model, tokenizer, device):
    with torch.no_grad():
        try:
            generate(
                model=model,
                tokenizer=tokenizer,
                prompt_tokens=[[1, 2, 3], []], # one empty prompt
                max_gen_len=8,
                temperature=0.0,
                top_p=1.0,
                repetition_penalty=None,
                no_repeat_ngram_size=None,
                device=device,
                dtype=torch.float32,
                use_kv_cache=True
            )
            assert False, 'Expected ValueError for empty prompt'
        except ValueError as e:
            assert 'Prompt cannot be of length 0' in str(e)
