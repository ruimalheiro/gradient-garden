import torch

from inference.runtime import InferenceRuntime
from config import GlobalConfig
from enum import Enum


class EvalTask(str, Enum):
    HELLASWAG = 'hellaswag'
    WINOGRANDE = 'winogrande'
    ARC_CHALLENGE = 'arc_challenge'

def evaluate_hellaswag(
    inference_runtime: InferenceRuntime,
    config: GlobalConfig,
    batch_size: int,
    num_examples: int
):
    return evaluate_multiple_choice_task(
        task=EvalTask.HELLASWAG,
        inference_runtime=inference_runtime,
        config=config,
        batch_size=batch_size,
        num_examples=num_examples
    )

def evaluate_winogrande(
    inference_runtime: InferenceRuntime,
    config: GlobalConfig,
    batch_size: int,
    num_examples: int
):
    return evaluate_multiple_choice_task(
        task=EvalTask.WINOGRANDE,
        inference_runtime=inference_runtime,
        config=config,
        batch_size=batch_size,
        num_examples=num_examples
    )

def evaluate_arc_challenge(
    inference_runtime: InferenceRuntime,
    config: GlobalConfig,
    batch_size: int,
    num_examples: int
):
    return evaluate_multiple_choice_task(
        task=EvalTask.ARC_CHALLENGE,
        inference_runtime=inference_runtime,
        config=config,
        batch_size=batch_size,
        num_examples=num_examples
    )

@torch.inference_mode()
def evaluate_multiple_choice_task(
    task: EvalTask,
    inference_runtime: InferenceRuntime,
    config: GlobalConfig,
    batch_size: int,
    num_examples: int
):
    pass
