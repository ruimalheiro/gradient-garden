import torch

from dataclasses import dataclass


@dataclass
class MoeLayerMetrics:
    layer_id: int
    acc_top1_counts: torch.Tensor
    acc_topk_counts: torch.Tensor
    acc_p_sum: torch.Tensor
    acc_tokens: torch.Tensor

@dataclass
class ModelMetrics:
    moe: list[MoeLayerMetrics] | None = None
