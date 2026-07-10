import json
import torch
import torch.nn.functional as F

from engine.distributed import load_jsonl_file_and_scatter


def load_multiple_choice_eval_file(
    *,
    filepath,
    ddp,
    is_master_process,
    pad_token_id,
    size=None
):
    def prepare_line_fn(line):
        example = json.loads(line)
        tokens = torch.tensor(example['tokens'], dtype=torch.long)
        scoring_mask = torch.tensor(example['mask'], dtype=torch.long)
        label_index = int(example['label_index'])

        assert tokens.ndim == 2
        assert scoring_mask.shape == tokens.shape
        assert 0 <= label_index < tokens.size(0)
        return {
            'tokens': tokens,
            'mask': scoring_mask,
            'label_index': label_index,
            'valid': True
        }

    def prepare_dummy_line_fn():
        tokens = torch.full((1, 2), pad_token_id, dtype=torch.long)
        return {
            'tokens': tokens,
            'mask': torch.zeros_like(tokens),
            'label_index': -1,
            'valid': False
        }

    return load_jsonl_file_and_scatter(
        filepath=filepath,
        ddp=ddp,
        is_master_process=is_master_process,
        prepare_line_fn=prepare_line_fn,
        prepare_dummy_line_fn=prepare_dummy_line_fn,
        size=size
    )

def estimate_best_candidate_index_from_logits(tokens, mask, logits):
    # align tokens mask and logits (remove first token in tokens/mask and last logit in logits)
    shift_tokens = (tokens[..., 1:]).contiguous()
    shift_mask = (mask[..., 1:]).contiguous()
    shift_logits = (logits[..., :-1, :]).contiguous()

    # Flatten for cross_entropy
    flat_shift_tokens = shift_tokens.view(-1)
    flat_shift_logits = shift_logits.view(-1, shift_logits.size(-1))

    losses = F.cross_entropy(flat_shift_logits, flat_shift_tokens, reduction='none')

    # restore shape same as tokens
    shift_losses = losses.view(tokens.size(0), -1)

    # Apply the mask
    masked_shift_losses = shift_losses.masked_fill(shift_mask == 0, 0.0)

    # calculate loss for each candidate completion.
    scored_token_counts = shift_mask.sum(dim=1)
    sum_loss = masked_shift_losses.sum(dim=1)

    avg_loss = sum_loss / scored_token_counts.clamp_min(1)
    avg_loss = avg_loss.masked_fill(scored_token_counts == 0, float('inf'))

    # Pick the one with lowest loss.
    estimated_correct = avg_loss.argmin().item()
    return estimated_correct
