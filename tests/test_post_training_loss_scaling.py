import torch

from types import SimpleNamespace
from torch import nn
from engine.trainer import Trainer


def _build_trainer_for_gradient_scaling(model: nn.Module, world_size: int) -> Trainer:
    """Build only the Trainer state required by scale_gradients_by_n_valid."""
    trainer = object.__new__(Trainer)
    trainer.model = model
    trainer.trainer_ctx = SimpleNamespace(
        distributed=SimpleNamespace(ddp_world_size=world_size)
    )
    return trainer

def test_unequal_n_valid_microbatches_use_global_token_mean():
    """
    Two microbatches contain 1 and 3 valid tokens.

    The correct gradient is the mean over all four valid tokens:
        (1 + 3 + 5 + 7) / 4 = 4

    Equal averaging of the two microbatch means would incorrectly produce:
        (1 + 5) / 2 = 3
    """
    parameter = nn.Parameter(torch.tensor(2.0))
    model = nn.Module()
    model.register_parameter('weight', parameter)

    trainer = _build_trainer_for_gradient_scaling(model, world_size=1)

    microbatch_token_coefficients = (
        torch.tensor([1.0]),
        torch.tensor([3.0, 5.0, 7.0]),
    )

    n_valid_sum = torch.zeros(())

    for coefficients in microbatch_token_coefficients:
        # This represents a task returning a summed objective numerator.
        loss_for_backward = (parameter * coefficients).sum()
        loss_for_backward.backward()
        n_valid_sum += coefficients.numel()

    grad_scale = trainer.scale_gradients_by_n_valid(n_valid_sum)

    torch.testing.assert_close(torch.tensor(grad_scale), torch.tensor(1.0 / 4.0))
    torch.testing.assert_close(parameter.grad, torch.tensor(4.0))

    incorrect_equal_microbatch_mean = torch.tensor(3.0)
    assert not torch.isclose(parameter.grad, incorrect_equal_microbatch_mean)


def test_scale_gradients_by_n_valid_accounts_for_ddp_gradient_averaging():
    """
    Simulate two DDP ranks.

    Rank-local summed gradients:
        rank 0: gradient=6, n_valid=2
        rank 1: gradient=12, n_valid=6

    DDP first averages the gradients:
        (6 + 12) / 2 = 9

    The production helper must then multiply by:
        world_size / global_n_valid = 2 / 8

    producing the global mean gradient:
        9 * (2 / 8) = (6 + 12) / 8 = 2.25
    """
    model = nn.Linear(1, 1, bias=False)
    parameter = model.weight

    ddp_averaged_gradient = torch.tensor([[9.0]])
    parameter.grad = ddp_averaged_gradient.clone()

    trainer = _build_trainer_for_gradient_scaling(model, world_size=2)

    global_n_valid = torch.tensor(8.0)
    grad_scale = trainer.scale_gradients_by_n_valid(global_n_valid)

    expected_scale = torch.tensor(2.0 / 8.0)
    expected_global_mean_gradient = torch.tensor([[(6.0 + 12.0) / (2.0 + 6.0)]])

    torch.testing.assert_close(torch.tensor(grad_scale), expected_scale)
    torch.testing.assert_close(parameter.grad, expected_global_mean_gradient)
