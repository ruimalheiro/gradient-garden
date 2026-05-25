import torch

from inference.runtime import InferenceRuntime
from config import GlobalConfig


@torch.inference_mode()
def evaluate_validation_ppl(
    inference_runtime: InferenceRuntime,
    config: GlobalConfig,
    batch_size: int,
    validation_steps: int,
    ignore_index: int
):
    pass