import os
import numpy as np
import torch
import random
import torch.distributed as dist
import re

from engine.dataloaders.common import load_tokens
from logger import logger


class PretrainingDataLoader:
    def __init__(
        self,
        batch_size,
        sequence_length,
        is_master_process,
        ddp_rank,
        ddp_world_size,
        data_root,
        split,
        use_shuffle=False
    ):
        self.B = batch_size
        self.S = sequence_length
        self.is_master_process = is_master_process
        self.ddp_rank = ddp_rank
        self.ddp_world_size = ddp_world_size
        self.data_root = data_root
        assert split in {'train', 'val'}
        self.split = split
        self.use_shuffle = use_shuffle
        self.total_tokens = None

        split_root = os.path.join(data_root, split)
        assert os.path.isdir(split_root), f'missing split dir: {split_root}'

        target_pattern = re.compile(r'^data_(\d+)\.npy$')
        valid_shards = []
        for file_name in os.listdir(split_root):
            match = target_pattern.match(file_name)
            if match:
                valid_shards.append((int(match.group(1)), os.path.join(split_root, file_name)))

        valid_shards.sort(key=lambda x: x[0])
        indexes = [i for i, _ in valid_shards]
        assert indexes == list(range(len(valid_shards))), f'Shard sequence is broken: {indexes}'

        self.shards = [shard_path for _, shard_path in valid_shards]
        assert self.shards, f'no shards found in split {split}'

        self.group_undersized_final_shard()

        logger.info(f'found {len(self.shards)} shards for split {split}')

        self.validate_shards_size()
        self.reset()

    def get_shard_paths(self, shard):
        if isinstance(shard, tuple):
            return shard
        return (shard,)

    def get_shard_size(self, shard):
        total = 0
        for shard_path in self.get_shard_paths(shard):
            data = np.load(shard_path, mmap_mode='r', allow_pickle=False)
            total += int(data.shape[0])
            del data
        return total

    def load_shard(self, shard):
        shard_paths = self.get_shard_paths(shard)

        if len(shard_paths) == 1:
            return load_tokens(shard_paths[0])

        return torch.cat([load_tokens(shard_path) for shard_path in shard_paths])

    def group_undersized_final_shard(self):
        if len(self.shards) < 2:
            return

        required_tokens = self.B * self.S * self.ddp_world_size + 1
        final_shard = self.shards[-1]
        final_shard_size = self.get_shard_size(final_shard)

        if final_shard_size >= required_tokens:
            return

        previous_shard = self.shards[-2]

        grouped_shard = (
            self.get_shard_paths(previous_shard) +
            self.get_shard_paths(final_shard)
        )

        self.shards[-2:] = [grouped_shard]

        logger.warning(f'Final shard has only {final_shard_size} tokens, below the {required_tokens} required for one distributed batch. Grouping it with the previous shard.')

    def validate_shards_size(self):
        required_tokens = self.B * self.S * self.ddp_world_size + 1

        for shard in self.shards:
            shard_len = self.get_shard_size(shard)

            if shard_len < required_tokens:
                raise ValueError(
                    f'Shard is too small for distributed training: {shard}. '
                    f'Need a minimum of {required_tokens} tokens, got {shard_len}. '
                    f'B={self.B}, S={self.S}, world_size={self.ddp_world_size}.'
                )

    def calculate_max_tokens(self):
        if self.total_tokens:
            return self.total_tokens

        def _calculate():
            return sum(self.get_shard_size(shard) for shard in self.shards)

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

    def sync_shuffle_shards(self):
        if not self.use_shuffle:
            return

        if self.ddp_world_size <= 1 or not dist.is_available() or not dist.is_initialized():
            random.shuffle(self.shards)
            return

        # create the indexes and shuffle
        target_indexes = list(range(len(self.shards)))
        if self.is_master_process:
            random.shuffle(target_indexes)

        # synchronize the shuffle
        object_list_to_sync = [target_indexes]
        dist.broadcast_object_list(object_list_to_sync, src=0)
        order = object_list_to_sync[0]
        self.shards = [self.shards[i] for i in order]

    def reset(self):
        self.current_shard = 0
        self.sync_shuffle_shards()
        self.tokens = self.load_shard(self.shards[self.current_shard])
        if torch.cuda.is_available():
            self.tokens = self.tokens.pin_memory()
        self.current_position = 0

    def state_dict(self):
        return {
            'shards' : list(self.shards),
            'current_shard' : self.current_shard,
            'current_position' : self.current_position
        }

    def load_state_dict(self, state):
        self.shards = state['shards']
        self.current_shard = state['current_shard']
        self.tokens = self.load_shard(self.shards[self.current_shard])
        if torch.cuda.is_available():
            self.tokens = self.tokens.pin_memory()
        self.current_position = state['current_position']

    def next_batch(self):
        B, S = self.B, self.S
        local_batch_tokens = B * S
        global_batch_tokens = local_batch_tokens * self.ddp_world_size

        # current_position is global and equal on all ranks. (same starting point reference)
        rank_position = self.current_position + local_batch_tokens * self.ddp_rank

        buf = self.tokens[rank_position : rank_position + local_batch_tokens + 1]

        if len(buf) != local_batch_tokens + 1:
            raise RuntimeError(
                f'Invalid batch slice on rank {self.ddp_rank}: '
                f'global_position={self.current_position}, '
                f'rank_position={rank_position}, '
                f'needed={local_batch_tokens + 1}, '
                f'got={len(buf)}, '
                f'shard={self.current_shard}, '
                f'shard_len={len(self.tokens)}'
            )

        x = (buf[:-1]).view(B, S)
        y = (buf[1:]).view(B, S)

        self.current_position += global_batch_tokens

        # If needed to change shard, all ranks change.
        if self.current_position + global_batch_tokens + 1 > len(self.tokens):
            self.current_shard = (self.current_shard + 1) % len(self.shards)

            if self.current_shard == 0:
                self.sync_shuffle_shards()

            self.tokens = self.load_shard(self.shards[self.current_shard])
            if torch.cuda.is_available():
                self.tokens = self.tokens.pin_memory()

            self.current_position = 0

        # None here is because we dont need attention mask.
        return x, y, None
