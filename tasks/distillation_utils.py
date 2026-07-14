import torch
import torch.nn.functional as F


def distillation_loss(teacher_logits, student_logits, temperature=2.0, valid_mask=None):
    teacher_probabilities = F.softmax(teacher_logits.view(-1, teacher_logits.size(-1)) / temperature, dim=-1)
    student_log_probabilities = F.log_softmax(student_logits.view(-1, student_logits.size(-1)) / temperature, dim=-1)

    kl_divergence_per_token = F.kl_div(student_log_probabilities, teacher_probabilities, reduction='none').sum(dim=-1) * (temperature ** 2)
    kl_divergence_per_token_sum = kl_divergence_per_token.sum()

    if valid_mask is not None:
        valid_mask = valid_mask.reshape(-1).to(dtype=kl_divergence_per_token.dtype)
        kl_divergence_per_token = kl_divergence_per_token * valid_mask
        return kl_divergence_per_token_sum / valid_mask.sum().clamp_min(1.0)

    return kl_divergence_per_token_sum / torch.tensor(kl_divergence_per_token.numel(), dtype=kl_divergence_per_token.dtype)
