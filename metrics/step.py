from dataclasses import dataclass
from enum import Enum


class StepType(str, Enum):
    TRAIN = 'train'
    VAL = 'val'
    HELLASWAG = 'hellaswag'
    WINOGRANDE = 'winogrande'
    ARC_CHALLENGE = 'arc_challenge'
    IFEVAL_NO_EXTERNAL = 'ifeval_no_external'

@dataclass(frozen=True)
class StepMetrics:
    step_type: StepType
    norm: float = None
    dt: float = None
    tokens_per_sec: int = None
    scheduler_metadata: dict[str, dict] = None
    accuracy: float = None
    prompt_accuracy: float = None
    instruction_accuracy: float = None
