import torch

from models.implementations.tendril_moe import MoEFeedForward


def _build_deterministic_moe() -> MoEFeedForward:
    moe = MoEFeedForward(
        dim=2,
        hidden_dim=4,
        multiple_of=1,
        ffn_dim_multiplier=None,
        num_experts=2,
        expert_dim=2,
        top_k=1,
        load_balancing_coef=1.0,
        z_loss_coef=0.0,
    )

    with torch.no_grad():
        # Positive first coordinates route to expert 0; negative ones to expert 1.
        moe.router.weight.copy_(
            torch.tensor(
                [
                    [1.0, 0.0],
                    [-1.0, 0.0],
                ]
            )
        )

        # Make every expert deterministic and ensure every routed token receives
        # a non-zero feed-forward output.
        identity = torch.eye(2)
        for expert in moe.experts:
            expert.w1.weight.copy_(identity)
            expert.w2.weight.copy_(identity)
            expert.w3.weight.copy_(identity)

    return moe


def test_moe_router_loss_mask_only_changes_auxiliary_loss():
    """
    The supervised-token mask must affect router auxiliary statistics only.

    Every token must still be routed through an expert, including tokens that
    are excluded from the auxiliary objective.
    """
    moe = _build_deterministic_moe()

    x = torch.tensor(
        [
            [
                [2.0, 1.0],
                [1.0, 1.0],
                [-1.0, 1.0],
                [-2.0, 1.0],
            ]
        ]
    )

    all_tokens_mask = torch.ones((1, 4), dtype=torch.bool)
    supervised_tokens_mask = torch.tensor([[True, True, False, False]], dtype=torch.bool)

    output_all, aux_loss_all = moe(x, router_loss_mask=all_tokens_mask)
    output_supervised, aux_loss_supervised = moe(x, router_loss_mask=supervised_tokens_mask)

    # The mask must not change actual expert routing or model activations.
    torch.testing.assert_close(output_supervised, output_all)

    # The masked-out tokens must still have passed through their experts.
    assert torch.count_nonzero(output_supervised[:, 2:]).item() > 0

    # The auxiliary population changed from balanced routing over all tokens to
    # only the two tokens routed to expert 0, so the auxiliary loss must change.
    assert not torch.isclose(aux_loss_supervised, aux_loss_all)

    torch.testing.assert_close(aux_loss_all, torch.tensor(1.0))

    expected_supervised_aux_loss = 2.0 * torch.stack(
        [
            aux_loss_supervised.new_tensor(4.0).sigmoid(),
            aux_loss_supervised.new_tensor(2.0).sigmoid(),
        ]
    ).mean()
