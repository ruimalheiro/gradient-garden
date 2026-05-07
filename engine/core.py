import math

from dataclasses import dataclass


@dataclass
class TrainerState:
    start_step: int = 0
    current_step: int = 0
    max_steps: int = 0
    best_val_loss: float = float('inf')
    last_val_loss: float = float('inf')
    num_val_runs_no_improve: int = 0
    should_stop: bool = False
    is_last_step: bool = False

    def to_dict(self):
        return {
            'start_step': self.start_step,
            'current_step': self.current_step,
            'max_steps': self.max_steps,
            'best_val_loss': self.best_val_loss if not math.isinf(self.best_val_loss) else None,
            'last_val_loss': self.last_val_loss if not math.isinf(self.last_val_loss) else None,
            'num_val_runs_no_improve': self.num_val_runs_no_improve,
            'should_stop': self.should_stop,
            'is_last_step': self.is_last_step
        }
