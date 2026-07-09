import torch
import math

from collections import defaultdict
from inference.kv_cache import KVCache
from utils import batch_generator
from tqdm.auto import tqdm


def sample_top_p(probs, p):
    ''' Top P - Sorts the tokens from highest probabilities to lowest and calculates cumulative probabilities up to the cumulative >= p.
    '''
    probs_sort, probs_idx = torch.sort(probs, dim=-1, descending=True)
    probs_sum = torch.cumsum(probs_sort, dim=-1)
    mask = probs_sum - probs_sort > p
    probs_sort[mask] = 0.0
    
    probs_sort.div_(probs_sort.sum(dim=-1, keepdim=True))

    next_token = torch.multinomial(probs_sort, num_samples=1)

    next_token = torch.gather(probs_idx, -1, next_token)
    return next_token

def temperature_and_top_p_sampling(logits, temperature, top_p):
    ''' Applies temperature and calculates top P. If temperature is 0 we just get the token with highest logit.
        Penalty should be ~[1.05, 1.2]
    '''
    if temperature > 0:
        probs = torch.softmax(logits / temperature, dim=-1)
        next_token = sample_top_p(probs, top_p)
    else:
        next_token = torch.argmax(logits, dim=-1)
    return next_token

def apply_repetition_penalty(current_tokens, logits, penalty):
    ''' Applies the repetition penalty to reduce the probability of the same exact tokens appear multiple times even if they have strong logit.
        Modification is in-place.
    '''
    if penalty is None:
        return

    # (for each batch index) look at all the token logits that already were generated and apply the penalty:
    for batch_index in range(logits.size(0)):
        tokens = current_tokens[batch_index].unique()
        positive_logits = logits[batch_index, tokens] > 0

        # penalty: if logit is positive, we want to reduce it, if it is negative we want to make it more negative
        logits[batch_index, tokens] = torch.where(
            positive_logits,
            logits[batch_index, tokens] / penalty,
            logits[batch_index, tokens] * penalty
        )

def apply_no_repeat_ngram(current_tokens, logits, ngram_size):
    ''' Applies the no_repeat_ngram strategy. Computes the ngrams of size ngram_size accross the token sequence and bans 
    tokens "ngram_size" for the prefix "ngram_size - 1" (Tokens that would complete an ngram).
        Modification is in-place.
    '''
    if ngram_size is None or current_tokens.size(1) < ngram_size - 1:
        return

    for batch_index in range(logits.size(0)):
        banned = defaultdict(set)
        tokens = current_tokens[batch_index].tolist()

        # generate the bans
        for i in range(len(tokens) - ngram_size + 1):
            slide_index = i + ngram_size - 1
            prefix, banned_token = tuple(tokens[i: slide_index]), tokens[slide_index]

            banned[prefix].add(banned_token)

        # get last prefix
        prefix = tuple(tokens[-(ngram_size - 1):])
        for banned_token in banned.get(prefix, ()):
            logits[batch_index, banned_token] = float('-inf')

def build_response(tokens_batch, prompt_tokens, stop_tokens, max_gen_len, eos_id):
    stop_tokens_set = set(stop_tokens)
    result = []
    for i, tokens in enumerate(tokens_batch.tolist()):
        start = len(prompt_tokens[i])
        raw_tokens = tokens[start : start + max_gen_len]

        stop_index = None
        stop_token_id = None
        result_tokens = raw_tokens
        effective_tokens = raw_tokens

        for j, token in enumerate(raw_tokens):
            if token in stop_tokens_set:
                stop_index = j
                stop_token_id = token
                result_tokens = raw_tokens[:stop_index]
                effective_tokens = raw_tokens[:stop_index + 1]
                break

        effective_set = set(effective_tokens)

        metadata = {
            'generated_tokens_before_stop_or_limit': len(effective_tokens),
            'result_tokens': len(result_tokens),
            'last_generated_token_id': effective_tokens[-1] if effective_tokens else None,
            'last_result_token_id': result_tokens[-1] if result_tokens else None,
            'last_10_generated_token_ids': effective_tokens[-10:],
            'contains_eos': eos_id in effective_set,
            'stop_token_id': stop_token_id,
            'stopped_by_stop_token': stop_index is not None,
            'stop_index': stop_index,
        }

        result.append({
            'metadata': metadata,
            'result': result_tokens,
        })
    return result

@torch.no_grad()
def generate(
    *,
    prompt_tokens,
    model,
    tokenizer,
    max_gen_len,
    temperature,
    top_p,
    repetition_penalty,
    no_repeat_ngram_size,
    device,
    dtype,
    use_kv_cache
):
    if hasattr(model, 'inner') and hasattr(model.inner, 'generate'):
        old_padding_side = tokenizer.model.padding_side
        tokenizer.model.padding_side = 'left'
        try:
            batch_encoding = tokenizer.model.pad(
                [{'input_ids': ids} for ids in prompt_tokens],
                padding=True,
                return_attention_mask=True
            )
            padded = torch.tensor(batch_encoding['input_ids'], device=device)
            attn_mask = torch.tensor(batch_encoding['attention_mask'], device=device)

            gen_kwargs = dict(
                max_new_tokens=max_gen_len,
                pad_token_id=tokenizer.pad_id,
                eos_token_id=tokenizer.eos_id,
                do_sample=temperature > 0,
                temperature=temperature if temperature > 0 else 1.0,
                top_p=top_p if temperature > 0 else 1.0,
                repetition_penalty=repetition_penalty,
                no_repeat_ngram_size=no_repeat_ngram_size
            )
            gen_kwargs = {k: v for k, v in gen_kwargs.items() if v is not None}

            outputs = model.inner.generate(
                padded,
                attention_mask=attn_mask,
                **gen_kwargs,
            )

            results = []
            for i in range(len(prompt_tokens)):
                input_len = padded.shape[1]
                gen_ids = outputs[i, input_len:].tolist()

                stop_idx = None
                for j, tid in enumerate(gen_ids):
                    if tid in tokenizer.stop_tokens:
                        stop_idx = j
                        break
                result_ids = gen_ids[:stop_idx] if stop_idx is not None else gen_ids
                effective_ids = gen_ids[:stop_idx+1] if stop_idx is not None else gen_ids
                results.append({
                    'result': result_ids,
                    'metadata': {
                        'generated_tokens_before_stop_or_limit': len(effective_ids),
                        'stopped_by_stop_token': stop_idx is not None,
                    }
                })
            return results
        finally:
            tokenizer.model.padding_side = old_padding_side

    if temperature < 0.0:
        raise ValueError(f'temperature must be >= 0.0, got {temperature}')
    if top_p <= 0.0 or top_p > 1.0:
        raise ValueError(f'top_p must be in (0, 1], got {top_p}')
    if repetition_penalty is not None and repetition_penalty <= 1.0:
        raise ValueError(f'repetition_penalty must be null or > 1.0, got {repetition_penalty}') 
    if no_repeat_ngram_size is not None and no_repeat_ngram_size <= 1:
        raise ValueError(f'no_repeat_ngram_size must be null or >= 2, got {no_repeat_ngram_size}')

    batch_size = len(prompt_tokens)

    pad_token_id = tokenizer.pad_id
    stop_tokens = tokenizer.stop_tokens
    eos_id = tokenizer.eos_id

    # Finding the boundaries / limits.
    min_prompt_len = min(len(t) for t in prompt_tokens)
    if min_prompt_len == 0:
        raise ValueError('Prompt cannot be of length 0')

    max_prompt_len = max(len(t) for t in prompt_tokens)
    if max_prompt_len >= model.config.max_seq_len:
        raise ValueError(
            f'Prompt length {max_prompt_len} exceeds max_seq_len {model.config.max_seq_len}'
        )

    total_len = min(model.config.max_seq_len, max_gen_len + max_prompt_len)

    # Here we assume we receive a batch of multiple tokenized sequences.
    tokens = torch.full((batch_size, total_len), pad_token_id, dtype=torch.long, device=device)

    for batch, tokens_list in enumerate(prompt_tokens):
        tokens[batch, : len(tokens_list)] = torch.tensor(tokens_list, dtype=torch.long, device=device)

    # Define stop conditions, input mask and the stop tokens (extracted from the tokenizer)
    eos_reached = torch.tensor([False] * batch_size, device=device)
    # input_text_mask = tokens != pad_token_id
    input_text_mask = torch.zeros_like(tokens, dtype=torch.bool)
    for i in range(batch_size):
        input_text_mask[i, :len(prompt_tokens[i])] = True
    stop_tokens = torch.tensor(list(stop_tokens), device=device)

    current_position = min_prompt_len

    # KVCache init
    kv_cache = None
    if use_kv_cache:
        kv_cache = KVCache(
            num_layers=model.config.n_layers,
            batch_size=batch_size,
            max_seq_len=total_len,
            n_kv_heads=model.config.n_kv_heads or model.config.n_heads,
            head_dim=model.config.dim // model.config.n_heads,
            device=device,
            dtype=dtype
        )

    out = model(tokens[:, :current_position], start_position=0, kv_cache=kv_cache)

    while current_position < total_len:
        logits = out['logits'][:, -1]

        # Apply repetition penalty
        apply_repetition_penalty(
            tokens[:, :current_position],
            logits,
            penalty=repetition_penalty
        )

        # Apply no repeat ngram
        apply_no_repeat_ngram(
            tokens[:, :current_position],
            logits,
            ngram_size=no_repeat_ngram_size
        )

        # Temperature and sampling.
        next_token = temperature_and_top_p_sampling(logits, temperature, top_p)
        next_token = next_token.reshape(-1)

        # Gets the next token depending on the condition (mask) and appends to tokens.
        next_token = torch.where(input_text_mask[:, current_position], tokens[:, current_position], next_token)

        # Should keep padding if the row already finished in a previous iteration.
        next_token = torch.where(
            eos_reached & (~input_text_mask[:, current_position]),
            torch.full_like(next_token, pad_token_id),
            next_token,
        )

        tokens[:, current_position] = next_token

        # Checks if we reached the eos on all sequences in the batch and updates the current position.
        eos_reached |= (~input_text_mask[:, current_position]) & (torch.isin(next_token, stop_tokens))
        if torch.all(eos_reached):
            break

        current_position += 1

        start_position = current_position - 1 if use_kv_cache else 0
        out = model(tokens[:, start_position : current_position], start_position=start_position, kv_cache=kv_cache)

    return build_response(
        tokens,
        prompt_tokens,
        list(tokenizer.stop_tokens),
        max_gen_len,
        eos_id
    )

@torch.inference_mode()
def generate_and_decode(
        *,
        prompts,
        model,
        tokenizer,
        max_gen_len,
        temperature,
        top_p,
        repetition_penalty,
        no_repeat_ngram_size,
        full_seq,
        device,
        dtype,
        is_instruct,
        use_kv_cache,
        batch_size,
        skip_encoding=False,
        show_progress=False,
        progress_bar_label=None,
        prompts_are_messages=False
    ):
        if full_seq and prompts_are_messages:
            raise ValueError('full_seq=True is not supported with prompts_are_messages=True')
        if not is_instruct and prompts_are_messages:
            raise ValueError('prompts_are_messages=True requires is_instruct=True')

        vocab_size = tokenizer.vocab_size
        pad_token_id = tokenizer.pad_id

        if not isinstance(prompts, list):
            prompts = [prompts]

        if batch_size is None:
            batch_size = len(prompts)

        if not skip_encoding:
            if is_instruct:
                if prompts_are_messages:
                    prompt_tokens = [
                        tokenizer.encode_instruct_messages_inference(prompt)
                        for prompt in prompts
                    ]
                else:
                    prompt_tokens = [
                        tokenizer.encode_instruct_inference(prompt)
                        for prompt in prompts
                    ]
            else:
                prompt_tokens = [tokenizer.encode(prompt) for prompt in prompts]
        else:
            prompt_tokens = prompts

        batches = batch_generator(prompt_tokens, batch_size)
        if show_progress:
            total_batches = math.ceil(len(prompt_tokens) / batch_size)
            batches = tqdm(
                batches,
                total=total_batches,
                desc=progress_bar_label if progress_bar_label is not None else 'Generating...',
                unit=' batch',
                leave=False,
            )
        
        outputs = []
        for prompt_tokens_batches in batches:
            output = generate(
                prompt_tokens=prompt_tokens_batches,
                model=model,
                tokenizer=tokenizer,
                max_gen_len=max_gen_len,
                temperature=temperature,
                top_p=top_p,
                repetition_penalty=repetition_penalty,
                no_repeat_ngram_size=no_repeat_ngram_size,
                device=device,
                dtype=dtype,
                use_kv_cache=use_kv_cache
            )
            outputs.extend(output)

        def validate_token(tokens):
            return [token if token < vocab_size else pad_token_id for token in tokens]

        for prompt, output in zip(prompts, outputs):
            result_decoded = tokenizer.decode(validate_token(output['result']))

            if full_seq:
                output['result_decoded'] = f'{prompt} {result_decoded}' if is_instruct else f'{prompt}{result_decoded}'
            else:
                output['result_decoded'] = result_decoded

        return outputs
