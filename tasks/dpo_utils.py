import torch
import torch.nn.functional as F


def dpo_log_probs(model, input_ids, labels, ignore_index):
    ''' Computes de log probabilities for DPO.

        Assumes dimensions input_ids [B, L] and labels_ids [B, L]
        labels here are already shifted. Prompt and pad tokens are ignore_index (ignored)
    '''
    # compute logits
    logits = model(input_ids)['logits'] # [B, L, V]
    log_probs = F.log_softmax(logits, dim=-1)

    mask = labels != ignore_index # [B, L]
    safe_labels = labels.masked_fill(~mask, 0)

    token_log_probs = log_probs.gather(
        dim=-1,
        index=safe_labels.unsqueeze(-1)
    ).squeeze(-1) # [B, L]

    # cancels the fake log probs in token_log_probs
    token_log_probs = token_log_probs * mask

    logp_per_sequence = token_log_probs.sum(dim=-1)  # [B]

    return logp_per_sequence

def dpo_loss(
    policy_log_probs_pos,
    policy_log_probs_neg,
    reference_log_probs_pos,
    reference_log_probs_neg,
    beta
):
    ''' Computes the DPO loss.
        For reference, Direct Preference Optimization paper: https://arxiv.org/pdf/2305.18290
    '''
    beta = torch.as_tensor(beta, dtype=policy_log_probs_pos.dtype, device=policy_log_probs_pos.device)

    pos_difference = policy_log_probs_pos - reference_log_probs_pos
    neg_difference = policy_log_probs_neg - reference_log_probs_neg
    margin = pos_difference - neg_difference

    loss =  - F.logsigmoid(beta * margin).mean()

    # metrics
    rewards_chosen = pos_difference.mean().item()
    rewards_rejected = neg_difference.mean().item()
    accuracy = (pos_difference > neg_difference).float().mean().item()
    margin_avg = margin.mean().item()
    pol_logprobs_pos = policy_log_probs_pos.mean().item()
    pol_logprobs_neg = policy_log_probs_neg.mean().item()

    metrics_s = (
        f'rewards/chosen: {rewards_chosen:4f} | '
        f'rewards/rejected: {rewards_rejected:4f} | '
        f'accuracy: {accuracy:4f} | margin: {margin_avg:4f} | '
        f'pol_logprobs/chosen: {pol_logprobs_pos:4f} | '
        f'pol_logprobs/rejected: {pol_logprobs_neg:4f}'
    )
    metrics = {
        'str': metrics_s,
        'wandb': {
            'Rewards/Chosen': rewards_chosen,
            'Rewards/Rejected': rewards_rejected,
            'Accuracy': accuracy,
            'Margin': margin_avg,
            'PolicyLogP/Chosen': pol_logprobs_pos,
            'PolicyLogP/Rejected': pol_logprobs_neg
        }
    }
    return loss, metrics
