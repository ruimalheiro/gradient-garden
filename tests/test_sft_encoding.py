import pytest


IGNORE_INDEX = -100

def supervised_ids(labels):
    return [
        int(token_id)
        for token_id in labels
        if int(token_id) != IGNORE_INDEX
    ]

def contains_subsequence(sequence, subsequence):
    if not subsequence:
        return True

    width = len(subsequence)

    return any(sequence[index:index + width] == subsequence for index in range(len(sequence) - width + 1))

def test_sft_supervises_every_assistant_turn_and_eos(tokenizer):
    conversation = [
        {'role': 'user', 'content': 'U1'},
        {'role': 'assistant', 'content': 'A1'},
        {'role': 'user', 'content': 'U2'},
        {'role': 'assistant', 'content': 'A2'},
    ]

    tokens, labels = tokenizer.encode_instruct_chat(
        conversation=conversation,
        ignore_index=IGNORE_INDEX,
    )

    expected_supervised = (
        tokenizer.encode('A1')
        + [tokenizer.eos_id]
        + tokenizer.encode('A2')
        + [tokenizer.eos_id]
    )

    assert len(tokens) == len(labels)
    assert supervised_ids(labels) == expected_supervised

    # Exclude BOS because some tokenizers use the same ID for BOS and EOS.
    assert tokens[1:].count(tokenizer.eos_id) == 2

def test_sft_source_system_prompt_overrides_default(tokenizer):
    source_system_prompt = 'Rewrite the input concisely.'

    tokens, _ = tokenizer.encode_instruct_chat(
        system_prompt=source_system_prompt,
        conversation=[
            {'role': 'user', 'content': 'Long input'},
            {'role': 'assistant', 'content': 'Short output'},
        ],
        ignore_index=IGNORE_INDEX,
    )

    expected_prefix = (
        [tokenizer.bos_id]
        + tokenizer.encode('System: ')
        + tokenizer.encode(source_system_prompt + '\n')
    )

    assert tokens[:len(expected_prefix)] == expected_prefix

    decoded = tokenizer.decode(tokens)
    assert source_system_prompt in decoded
    assert tokenizer.system_prompt not in decoded

def test_sft_none_system_prompt_uses_default(tokenizer):
    tokens, _ = tokenizer.encode_instruct_chat(
        system_prompt=None,
        conversation=[
            {'role': 'user', 'content': 'Question'},
            {'role': 'assistant', 'content': 'Answer'},
        ],
        ignore_index=IGNORE_INDEX,
    )

    expected_prefix = (
        [tokenizer.bos_id]
        + tokenizer.encode('System: ')
        + tokenizer.encode(tokenizer.system_prompt + '\n')
    )

    assert tokens[:len(expected_prefix)] == expected_prefix

def test_inference_history_uses_eos_after_assistant_turn(tokenizer):
    tokens = tokenizer.encode_instruct_messages_inference([
        {'role': 'system', 'content': 'System instruction'},
        {'role': 'user', 'content': 'First question'},
        {'role': 'assistant', 'content': 'First answer'},
        {'role': 'user', 'content': 'Second question'},
    ])

    expected_boundary = (
        tokenizer.encode('Assistant: ')
        + tokenizer.encode('First answer')
        + [tokenizer.eos_id]
        + tokenizer.encode('User: ')
        + tokenizer.encode('Second question\n')
        + tokenizer.encode('Assistant: ')
    )

    assert contains_subsequence(tokens, expected_boundary)

@pytest.mark.parametrize(
    'conversation, expected_error',
    [
        (
            [{'role': 'assistant', 'content': 'Unexpected'}],
            'Expected user',
        ),
        (
            [{'role': 'user', 'content': 'Missing answer'}],
            'must end with assistant',
        ),
        (
            [
                {'role': 'system', 'content': 'Unexpected system'},
                {'role': 'assistant', 'content': 'Answer'},
            ],
            'Unexpected role',
        ),
        (
            [
                {'role': 'user', 'content': 'U1'},
                {'role': 'user', 'content': 'U2'},
                {'role': 'assistant', 'content': 'A2'},
            ],
            'Expected assistant',
        ),
    ],
)
def test_sft_validation_runs_before_trimming(
    tokenizer,
    conversation,
    expected_error,
):
    with pytest.raises(ValueError, match=expected_error):
        tokenizer.encode_instruct_chat(
            conversation=conversation,
            ignore_index=IGNORE_INDEX,
            max_seq_len=10_000,
            trim_to_context=True,
        )

def test_sft_trimming_keeps_newest_complete_pairs(tokenizer):
    conversation = [
        {'role': 'user', 'content': 'Old user'},
        {'role': 'assistant', 'content': 'Old assistant'},
        {'role': 'user', 'content': 'Middle user'},
        {'role': 'assistant', 'content': 'Middle assistant'},
        {'role': 'user', 'content': 'Latest user'},
        {'role': 'assistant', 'content': 'Latest assistant'},
    ]

    expected_tokens, expected_labels = tokenizer.encode_instruct_chat(
        conversation=conversation[-4:],
        ignore_index=IGNORE_INDEX,
    )

    tokens, labels = tokenizer.encode_instruct_chat(
        conversation=conversation,
        ignore_index=IGNORE_INDEX,
        max_seq_len=len(expected_tokens),
        trim_to_context=True,
    )

    assert tokens == expected_tokens
    assert labels == expected_labels

    decoded = tokenizer.decode(tokens)

    assert 'Old user' not in decoded
    assert 'Old assistant' not in decoded
    assert 'Middle user' in decoded
    assert 'Middle assistant' in decoded
    assert 'Latest user' in decoded
    assert 'Latest assistant' in decoded

def test_sft_returns_empty_when_latest_pair_cannot_fit(tokenizer):
    tokens, labels = tokenizer.encode_instruct_chat(
        conversation=[
            {'role': 'user', 'content': 'Question'},
            {'role': 'assistant', 'content': 'Answer'},
        ],
        ignore_index=IGNORE_INDEX,
        max_seq_len=1,
        trim_to_context=True,
    )

    assert tokens == []
    assert labels == []
