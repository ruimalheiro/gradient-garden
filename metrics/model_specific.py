import torch

from dataclasses import dataclass
from metrics.moe import (
    MoeLayerMetrics,
    collect_moe_metrics
)


@dataclass
class ModelMetrics:
    moe: list[MoeLayerMetrics] | None = None

def collect_model_specific_metrics(
    *,
    model_metrics: ModelMetrics,
    ddp,
    is_master_process
):
    metrics = {}

    metrics.update(collect_moe_metrics(model_metrics.moe, ddp, is_master_process))

    return metrics
