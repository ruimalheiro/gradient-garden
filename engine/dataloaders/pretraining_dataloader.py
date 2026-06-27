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

        logger.info(f'found {len(self.shards)} shards for split {split}')

        self.validate_shards_size()
        self.reset()

    def validate_shards_size(self):
        required_tokens = self.B * self.S * self.ddp_world_size + 1
        for shard_path in self.shards:
            shard = np.load(shard_path, mmap_mode='r', allow_pickle=False)
            shard_len = int(shard.shape[0])

            if shard_len < required_tokens:
                raise ValueError(
                    f'Shard is too small for distributed training: {shard_path}. '
                    f'Need a minimum of {required_tokens} tokens, got {shard_len}. '
                    f'B={self.B}, S={self.S}, world_size={self.ddp_world_size}.'
                )

    def calculate_max_tokens(self):
        if self.total_tokens:
            return self.total_tokens

        def _calculate():
            total = 0
            for path in self.shards:
                shard = np.load(path, mmap_mode='r', allow_pickle=False)
                total += int(shard.shape[0])
                del shard
            return total

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
        self.tokens = load_tokens(self.shards[self.current_shard])
        if torch.cuda.is_available():
            self.tokens = self.tokens.pin_memory()
        self.current_position = self.B * self.S * self.ddp_rank

    def state_dict(self):
        return {
            'shards' : list(self.shards),
            'current_shard' : self.current_shard,
            'current_position' : self.current_position
        }

    def load_state_dict(self, state):
        self.shards = state['shards']
        self.current_shard = state['current_shard']
        self.tokens = load_tokens(self.shards[self.current_shard])
        if torch.cuda.is_available():
            self.tokens = self.tokens.pin_memory()
        self.current_position = state['current_position']

    def next_batch(self):
        B, S = self.B, self.S
        buf = self.tokens[self.current_position : self.current_position+B*S+1]
        x = (buf[:-1]).view(B, S)
        y = (buf[1:]).view(B, S)
        self.current_position += B * S * self.ddp_world_size
        if self.current_position + (B * S * self.ddp_world_size + 1) > len(self.tokens):
            self.current_shard = (self.current_shard + 1) % len(self.shards)
            if self.current_shard == 0:
                self.sync_shuffle_shards()
            self.tokens = load_tokens(self.shards[self.current_shard])
            if torch.cuda.is_available():
                self.tokens = self.tokens.pin_memory()
            self.current_position = self.B * self.S * self.ddp_rank
        # None here is because we dont need attention mask.
        return x, y, None
