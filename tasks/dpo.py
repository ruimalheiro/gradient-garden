import torch
import copy

from dataclasses import dataclass
from tasks.base import (
    BaseTask,
    TaskStepOutput,
    TaskAssets
)
from tasks.dpo_utils import (
    dpo_log_probs,
    dpo_loss
)
from logger import logger


@dataclass
class DPOTaskAssets(TaskAssets):
    dpo_ref_model: torch.nn.Module | None = None

class DPOTask(BaseTask):
    name: str = 'dpo'

    def setup(self, config, ctx, **kwargs):
        super().setup(config, ctx, **kwargs)
        return self

    def build_assets(self, tokenizer, model):
        model_dtype = self.ctx.precision.model_dtype
        logger.info(f'Preparing DPO reference model...', True)
        dpo_ref_model = copy.deepcopy(model).eval()
        for p in dpo_ref_model.parameters():
            p.requires_grad = False
        logger.info(f'Finished preparing DPO reference model', True)
        return DPOTaskAssets(dpo_ref_model=dpo_ref_model)

    def move_assets_to_device(self, assets: DPOTaskAssets) -> DPOTaskAssets:
        if not assets.dpo_ref_model:
            return assets
        device = self.ctx.device.device
        model_dtype = self.ctx.precision.model_dtype
        assets.dpo_ref_model = assets.dpo_ref_model.to(device, dtype=model_dtype).eval()
        return assets

    def train_micro_step(self, model, batch, assets: DPOTaskAssets):
        device = self.ctx.device.device
        device_type = self.ctx.device.device_type
        autocast_dtype = self.ctx.precision.autocast_dtype
        use_autocast = self.ctx.precision.use_autocast
        dpo_beta = self.config.dpo.beta
        ignore_index = self.config.tokenizer.ignore_index

        chosen_input_ids, chosen_labels, chosen_mask, rejected_input_ids, rejected_labels, rejected_mask = batch
        chosen_input_ids = chosen_input_ids.to(device, non_blocking=True)
        chosen_labels = chosen_labels.to(device, non_blocking=True)
        chosen_mask = chosen_mask.to(device, non_blocking=True)
        rejected_input_ids = rejected_input_ids.to(device, non_blocking=True)
        rejected_labels = rejected_labels.to(device, non_blocking=True)
        rejected_mask = rejected_mask.to(device, non_blocking=True)

        chosen_valid_tokens = (chosen_labels != ignore_index).sum()
        rejected_valid_tokens = (rejected_labels != ignore_index).sum()

        if chosen_valid_tokens.item() == 0:
            raise ValueError('DPO batch has no supervised chosen tokens')
        if rejected_valid_tokens.item() == 0:
            raise ValueError('DPO batch has no supervised rejected tokens')

        tokens_processed = (
            chosen_input_ids.numel()
            + rejected_input_ids.numel()
        )

        with torch.autocast(device_type=device_type, dtype=autocast_dtype, enabled=use_autocast):
            policy_log_probs_pos = dpo_log_probs(model, chosen_input_ids, chosen_labels, chosen_mask, ignore_index)
            policy_log_probs_neg = dpo_log_probs(model, rejected_input_ids, rejected_labels, rejected_mask, ignore_index)

        with torch.no_grad():
            with torch.autocast(device_type=device_type, dtype=autocast_dtype, enabled=use_autocast):
                reference_log_probs_pos = dpo_log_probs(assets.dpo_ref_model, chosen_input_ids, chosen_labels, chosen_mask, ignore_index)
                reference_log_probs_neg = dpo_log_probs(assets.dpo_ref_model, rejected_input_ids, rejected_labels, rejected_mask, ignore_index)

        loss, dpo_metrics = dpo_loss(
            policy_log_probs_pos,
            policy_log_probs_neg,
            reference_log_probs_pos,
            reference_log_probs_neg,
            dpo_beta
        )

        n_valid = torch.tensor(
            chosen_input_ids.size(0),
            device=device,
            dtype=loss.dtype
        )

        loss_for_backward = loss * n_valid

        return TaskStepOutput(
            tokens_processed=tokens_processed,
            n_valid=n_valid,
            loss=loss,
            loss_for_backward=loss_for_backward,
            metrics={
                'Train Loss': loss.detach(),
                **dpo_metrics['wandb']
            }
        )

    @torch.no_grad()
    def validation_step(self, model, batch, assets: DPOTaskAssets):
        device = self.ctx.device.device
        device_type = self.ctx.device.device_type
        autocast_dtype = self.ctx.precision.autocast_dtype
        use_autocast = self.ctx.precision.use_autocast
        dpo_beta = self.config.dpo.beta
        ignore_index = self.config.tokenizer.ignore_index

        chosen_input_ids, chosen_labels, chosen_mask, rejected_input_ids, rejected_labels, rejected_mask = batch
        chosen_input_ids = chosen_input_ids.to(device, non_blocking=True)
        chosen_labels = chosen_labels.to(device, non_blocking=True)
        chosen_mask = chosen_mask.to(device, non_blocking=True)
        rejected_input_ids = rejected_input_ids.to(device, non_blocking=True)
        rejected_labels = rejected_labels.to(device, non_blocking=True)
        rejected_mask = rejected_mask.to(device, non_blocking=True)

        chosen_valid_tokens = (chosen_labels != ignore_index).sum()
        rejected_valid_tokens = (rejected_labels != ignore_index).sum()

        if chosen_valid_tokens.item() == 0:
            raise ValueError('DPO validation batch has no supervised chosen tokens')
        if rejected_valid_tokens.item() == 0:
            raise ValueError('DPO validation batch has no supervised rejected tokens')

        with torch.autocast(device_type=device_type, dtype=autocast_dtype, enabled=use_autocast):
            policy_log_probs_pos = dpo_log_probs(model, chosen_input_ids, chosen_labels, chosen_mask, ignore_index)
            policy_log_probs_neg = dpo_log_probs(model, rejected_input_ids, rejected_labels, rejected_mask, ignore_index)
            reference_log_probs_pos = dpo_log_probs(assets.dpo_ref_model, chosen_input_ids, chosen_labels, chosen_mask, ignore_index)
            reference_log_probs_neg = dpo_log_probs(assets.dpo_ref_model, rejected_input_ids, rejected_labels, rejected_mask, ignore_index)

        loss, dpo_metrics = dpo_loss(
            policy_log_probs_pos,
            policy_log_probs_neg,
            reference_log_probs_pos,
            reference_log_probs_neg,
            dpo_beta
        )
        n_valid = torch.tensor(
            chosen_input_ids.size(0),
            device=device,
            dtype=loss.dtype
        )

        return TaskStepOutput(
            n_valid=n_valid,
            loss=loss,
            metrics=dpo_metrics['wandb']
        )
