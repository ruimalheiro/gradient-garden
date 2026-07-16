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

def test_dpo_history_boundaries_and_answer_supervision(tokenizer):
    conversation = [
        {'role': 'user', 'content': 'U1'},
        {'role': 'assistant', 'content': 'A1'},
        {'role': 'user', 'content': 'U2'},
    ]

    (
        prompt_ids,
        chosen_ids,
        chosen_labels,
        rejected_ids,
        rejected_labels,
    ) = tokenizer.encode_instruct_chat_dpo(
        conversation=conversation,
        chosen='Chosen answer',
        rejected='Rejected answer',
        system_prompt='Preference policy',
        ignore_index=IGNORE_INDEX,
    )

    expected_history_boundary = (
        tokenizer.encode('Assistant: ')
        + tokenizer.encode('A1')
        + [tokenizer.eos_id]
        + tokenizer.encode('User: ')
        + tokenizer.encode('U2\n')
        + tokenizer.encode('Assistant: ')
    )

    assert contains_subsequence(prompt_ids, expected_history_boundary)

    assert supervised_ids(chosen_labels) == (
        tokenizer.encode('Chosen answer')
        + [tokenizer.eos_id]
    )

    assert supervised_ids(rejected_labels) == (
        tokenizer.encode('Rejected answer')
        + [tokenizer.eos_id]
    )

    assert chosen_ids == (
        prompt_ids
        + tokenizer.encode('Chosen answer')
        + [tokenizer.eos_id]
    )

    assert rejected_ids == (
        prompt_ids
        + tokenizer.encode('Rejected answer')
        + [tokenizer.eos_id]
    )

@pytest.mark.parametrize(
    'conversation, expected_error',
    [
        (
            [
                {'role': 'user', 'content': 'Question'},
                {'role': 'assistant', 'content': 'Wrong final role'},
            ],
            'must end with user',
        ),
        (
            [
                {'role': 'assistant', 'content': 'Unexpected'},
                {'role': 'user', 'content': 'Question'},
            ],
            'Expected user',
        ),
        (
            [
                {'role': 'user', 'content': 'U1'},
                {'role': 'user', 'content': 'U2'},
            ],
            'Expected assistant',
        ),
    ],
)
def test_dpo_validation_runs_before_trimming(
    tokenizer,
    conversation,
    expected_error,
):
    with pytest.raises(ValueError, match=expected_error):
        tokenizer.encode_instruct_chat_dpo(
            conversation=conversation,
            chosen='Chosen',
            rejected='Rejected',
            ignore_index=IGNORE_INDEX,
            max_seq_len=10_000,
            trim_to_context=True,
        )
