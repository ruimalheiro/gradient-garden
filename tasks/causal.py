import torch

from dataclasses import dataclass
from transformers import AutoModelForCausalLM
from tasks.base import (
    BaseTask,
    TaskStepOutput,
    TaskAssets
)
from tasks.distillation_utils import distillation_loss
from logger import logger


@dataclass
class CausalTaskAssets(TaskAssets):
    teacher_model: torch.nn.Module | None = None

class CausalTask(BaseTask):
    name: str = 'causal'

    def setup(self, config, ctx, **kwargs):
        super().setup(config, ctx, **kwargs)
        return self

    def build_assets(self, tokenizer, model):
        config = self.config
        if not config.distillation.enabled:
            return CausalTaskAssets()
        ddp_rank = self.ctx.distributed.ddp_rank
        logger.info(f'Loading teacher model on gpu: {ddp_rank}...', True)
        teacher_model = AutoModelForCausalLM.from_pretrained(config.distillation.teacher_model_checkpoint, token=config.third_party.hf_token)
        if teacher_model.vocab_size != tokenizer.vocab_size:
            logger.warning(f'The sizes of the vocabularies for the teacher model and the tokenizer do not match: {teacher_model.vocab_size} != {tokenizer.vocab_size}\nResizing the vocab of the teacher model to match the tokenizer... NOTE: This can potentially cause issues.')
            teacher_model.resize_token_embeddings(tokenizer.vocab_size)
        logger.info(f'Finished loading teacher model on gpu: {ddp_rank}...', True)
        return CausalTaskAssets(teacher_model=teacher_model)

    def move_assets_to_device(self, assets: CausalTaskAssets) -> CausalTaskAssets:
        if not assets.teacher_model:
            return assets
        device = self.ctx.device.device
        model_dtype = self.ctx.precision.model_dtype
        assets.teacher_model = assets.teacher_model.to(device, dtype=model_dtype).eval()
        return assets

    def train_micro_step(self, model, batch, assets: CausalTaskAssets):
        device = self.ctx.device.device
        device_type = self.ctx.device.device_type
        autocast_dtype = self.ctx.precision.autocast_dtype
        use_autocast = self.ctx.precision.use_autocast
        ignore_index = self.config.tokenizer.ignore_index

        x, y, attention_mask = batch
        x = x.to(device, non_blocking=True)
        y = y.to(device, non_blocking=True)
        if attention_mask is not None:
            attention_mask = attention_mask.to(device, non_blocking=True)

        tokens_processed = x.numel()

        with torch.autocast(
            device_type=device_type,
            dtype=autocast_dtype,
            enabled=use_autocast
        ):
            result = model(x, labels=y, attention_mask=attention_mask)
            loss = result['loss']

        loss_for_backward = loss

        metrics = {
            'Train Loss': loss.detach()
        }

        n_valid = (y != ignore_index).sum()
        if n_valid.item() == 0:
            raise ValueError('Causal batch has no valid supervised tokens')

        if self.config.distillation.enabled:
            tokens_processed += x.numel()

            with torch.no_grad():
                teacher_logits = assets.teacher_model(input_ids=x, )['logits']

            valid_mask = y != ignore_index

            loss_distil = distillation_loss(
                teacher_logits,
                result['logits'],
                temperature=self.config.distillation.temperature,
                valid_mask=valid_mask
            )
            loss_for_backward = loss_for_backward + loss_distil

            metrics['Train Loss'] = loss_for_backward.detach()
            metrics['Train Distill Loss'] = loss_distil.detach()

        loss_for_backward = loss_for_backward * n_valid

        return TaskStepOutput(
            tokens_processed=tokens_processed,
            n_valid=n_valid,
            loss=loss,
            loss_for_backward=loss_for_backward,
            metrics=metrics
        )

    @torch.no_grad()
    def validation_step(self, model, batch, assets: CausalTaskAssets):
        device = self.ctx.device.device
        device_type = self.ctx.device.device_type
        autocast_dtype = self.ctx.precision.autocast_dtype
        use_autocast = self.ctx.precision.use_autocast

        x, y, attention_mask = batch
        x = x.to(device, non_blocking=True)
        y = y.to(device, non_blocking=True)
        if attention_mask is not None:
            attention_mask = attention_mask.to(device, non_blocking=True)

        with torch.autocast(device_type=device_type, dtype=autocast_dtype, enabled=use_autocast):
            loss = model(x, labels=y, attention_mask=attention_mask)['loss']
        
        n_valid = (y != self.config.tokenizer.ignore_index).sum().float()

        return TaskStepOutput(
            n_valid=n_valid,
            loss=loss
        )
