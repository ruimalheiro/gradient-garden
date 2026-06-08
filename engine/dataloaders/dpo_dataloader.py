import os
import torch
import datasets
import torch.distributed as dist

from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
from engine.dataloaders.common import pad_batch_to_multiple_of
from logger import logger


class DirectPreferenceOptimizationDataLoader:
    def __init__(
        self,
        batch_size,
        sequence_length,
        is_master_process,
        ddp_rank,
        ddp_world_size,
        data_root,
        split,
        use_shuffle,
        pad_id,
        drop_last,
        number_of_cpu_processes,
        ignore_index
    ):
        self.B = batch_size
        self.S = sequence_length
        self.is_master_process = is_master_process
        self.ddp_rank = ddp_rank
        self.ddp_world_size = ddp_world_size
        self.total_tokens = None
        self.number_of_cpu_processes = number_of_cpu_processes
        self.ignore_index = ignore_index

        dataset = datasets.load_from_disk(os.path.join(data_root, split))
        logger.info(f'found {len(dataset)} examples for {split}')

        self.is_master_process = is_master_process

        assert isinstance(dataset, datasets.Dataset)

        self.sampler = DistributedSampler(
            dataset,
            num_replicas=ddp_world_size,
            rank=ddp_rank,
            shuffle=use_shuffle,
            drop_last=drop_last
        )

        def collate(examples):
            chosen_ids = []
            chosen_labels = []
            rejected_ids = []
            rejected_labels = []

            for i, e in enumerate(examples):
                chosen_input_ids = torch.tensor(e['chosen_input_ids'], dtype=torch.long)
                chosen_target_labels = torch.tensor(e['chosen_labels'], dtype=torch.long)
                rejected_input_ids = torch.tensor(e['rejected_input_ids'], dtype=torch.long)
                rejected_target_labels = torch.tensor(e['rejected_labels'], dtype=torch.long)

                if chosen_input_ids.numel() == 0:
                    raise ValueError(f'Empty chosen_input_ids in collate example {i}: {e}')
                if chosen_target_labels.numel() == 0:
                    raise ValueError(f'Empty chosen_labels in collate example {i}: {e}')
                if rejected_input_ids.numel() == 0:
                    raise ValueError(f'Empty rejected_input_ids in collate example {i}: {e}')
                if rejected_target_labels.numel() == 0:
                    raise ValueError(f'Empty rejected_labels in collate example {i}: {e}')
                if chosen_input_ids.numel() != chosen_target_labels.numel():
                    raise ValueError(
                        f'chosen input_ids/labels length do not match in collate example {i}: '
                        f'{chosen_input_ids.numel()} vs {chosen_target_labels.numel()}'
                    )
                if rejected_input_ids.numel() != rejected_target_labels.numel():
                    raise ValueError(
                        f'rejected input_ids/labels length do not match in collate example {i}: '
                        f'{rejected_input_ids.numel()} vs {rejected_target_labels.numel()}'
                    )
                if (chosen_target_labels != self.ignore_index).sum().item() == 0:
                    raise ValueError(f'No chosen labels before truncation in collate example {i}: {e}')
                if (rejected_target_labels != self.ignore_index).sum().item() == 0:
                    raise ValueError(f'No rejected labels before truncation in collate example {i}: {e}')

                if chosen_input_ids.numel() > sequence_length:
                    chosen_input_ids = chosen_input_ids[-sequence_length:]
                    chosen_target_labels = chosen_target_labels[-sequence_length:]
                if rejected_input_ids.numel() > sequence_length:
                    rejected_input_ids = rejected_input_ids[-sequence_length:]
                    rejected_target_labels = rejected_target_labels[-sequence_length:]

                if (chosen_input_ids != int(pad_id)).sum().item() == 0:
                    raise ValueError(f'Chosen input ids after truncation are all pad tokens in collate example {i}: {e}')
                if (rejected_input_ids != int(pad_id)).sum().item() == 0:
                    raise ValueError(f'Rejected input ids after truncation are all pad tokens in collate example {i}: {e}')
                if (chosen_target_labels != self.ignore_index).sum().item() == 0:
                    raise ValueError(f'No chosen labels after truncation in collate example {i}: {e}')
                if (rejected_target_labels != self.ignore_index).sum().item() == 0:
                    raise ValueError(f'No rejected labels after truncation in collate example {i}: {e}')

                chosen_ids.append(chosen_input_ids)
                chosen_labels.append(chosen_target_labels)
                rejected_ids.append(rejected_input_ids)
                rejected_labels.append(rejected_target_labels)

            chosen_ids = pad_batch_to_multiple_of(
                sequences=chosen_ids,
                padding_value=int(pad_id),
                multiple=8,
                max_length=sequence_length,
            )
            chosen_labels = pad_batch_to_multiple_of(
                sequences=chosen_labels,
                padding_value=self.ignore_index,
                multiple=8,
                max_length=sequence_length,
            )
            rejected_ids = pad_batch_to_multiple_of(
                sequences=rejected_ids,
                padding_value=int(pad_id),
                multiple=8,
                max_length=sequence_length,
            )
            rejected_labels = pad_batch_to_multiple_of(
                sequences=rejected_labels,
                padding_value=self.ignore_index,
                multiple=8,
                max_length=sequence_length,
            )

            return chosen_ids, chosen_labels, rejected_ids, rejected_labels

        self._dataloader = DataLoader(
            dataset,
            batch_size=batch_size,
            sampler=self.sampler,
            collate_fn=collate,
            drop_last=drop_last,
            pin_memory=True
        )
        self._iterator = iter(self._dataloader)

    def next_batch(self):
        try:
            return next(self._iterator)
        except StopIteration:
            self.reset()
            return next(self._iterator)

    def reset(self):
        if hasattr(self.sampler, 'set_epoch'):
            update_epoch = 0
            if hasattr(self.sampler, 'epoch'):
                update_epoch = self.sampler.epoch + 1
            self.sampler.set_epoch(update_epoch)
        self._iterator = iter(self._dataloader)

    def num_examples(self):
        return len(self._dataloader.dataset)

    def calculate_max_tokens(self):
        if self.total_tokens:
            return self.total_tokens

        def _calculate():
            return sum(self._dataloader.dataset.map(
                lambda ex: {'len': len(ex['chosen_input_ids']) + len(ex['rejected_input_ids'])},
                num_proc=self.number_of_cpu_processes,
                remove_columns=[],
                desc='Calculating number of tokens'
            )['len'])

        if self.ddp_world_size <= 1 or not dist.is_available() or not dist.is_initialized():
            return _calculate()

        total_tokens = None
        object_list_to_sync = [total_tokens]
        if self.is_master_process:
            object_list_to_sync[0] = _calculate()
        dist.broadcast_object_list(object_list_to_sync, src=0)
        total_tokens = int(object_list_to_sync[0])
        self.total_tokens = total_tokens
        return total_tokens

    def state_dict(self):
        return {'epoch': getattr(self.sampler, 'epoch', 0)}

    def load_state_dict(self, state):
        if 'epoch' not in state:
            if self.is_master_process:
                logger.warning('"epoch" not present, starting fresh dataloader (most likely transition from pretraining to DPO).')
            return
        epoch = state['epoch']
        self.sampler.set_epoch(epoch)
        self.sampler.epoch = epoch
        self._iterator = iter(self._dataloader)
