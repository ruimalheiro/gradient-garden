import os
import torch
import torch.distributed as dist

from torch.nn.parallel import DistributedDataParallel as DDP
from torch.distributed import init_process_group
from torch.distributed.fsdp import fully_shard


os.environ.setdefault('TORCH_NCCL_ASYNC_ERROR_HANDLING', '1')

def init_multi_gpu(device_type):
    ddp = int(os.environ.get('RANK', -1)) != -1

    assert torch.cuda.is_available()

    if ddp:
        ddp_rank = int(os.environ['RANK'])
        ddp_local_rank = int(os.environ['LOCAL_RANK'])
        ddp_world_size = int(os.environ['WORLD_SIZE'])

        torch.cuda.set_device(ddp_local_rank)
        init_process_group(backend='nccl', device_id=torch.device(f'cuda:{ddp_local_rank}'))

        device = f'cuda:{ddp_local_rank}'
        is_master_process = ddp_rank == 0
    else:
        ddp_rank = 0
        ddp_local_rank = 0
        ddp_world_size = 1

        device = 'cuda'
        is_master_process = True

    return ddp, ddp_rank, ddp_local_rank, ddp_world_size, is_master_process, device


def prepare_model_for_ddp(model, ddp_local_rank):
    ''' More details for the following config:
        https://docs.pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html
    '''
    ddp = int(os.environ.get('RANK', -1)) != -1
    if ddp:
        model = DDP(
            model,
            device_ids=[ddp_local_rank],
            broadcast_buffers=False,
            gradient_as_bucket_view=True,
            bucket_cap_mb=32,
            static_graph=True,
            find_unused_parameters=False
        )
    return model

def prepare_model_for_fsdp(model, ddp_local_rank, fsdp_precision):
    ddp = int(os.environ.get('RANK', -1)) != -1
    if ddp:
        for block in model.layers:
            fully_shard(block, reshard_after_forward=True, mp_policy=fsdp_precision)
        fully_shard(model, reshard_after_forward=False, mp_policy=fsdp_precision)
    return model

def get_model(model):
    if hasattr(model, 'module'):
        return model.module
    return model

def load_jsonl_file_and_scatter(
    *,
    filepath,
    ddp,
    is_master_process,
    prepare_line_fn,
    prepare_dummy_line_fn,
    size=None,
    ensure_at_least_one_per_rank=True
):
    # Loads the file and scatters to other ranks
    world_size = dist.get_world_size() if ddp else 1

    shards = None
    if is_master_process:
        # master builds the shards
        with open(filepath, 'r', encoding='utf-8') as f:
            data = [prepare_line_fn(line) for line in f if line.strip()]
            if size is not None:
                data = data[:size]

        if ensure_at_least_one_per_rank:
            shard_size = max(1, (len(data) + world_size - 1) // world_size)
        else:
            shard_size = (len(data) + world_size - 1) // world_size
            if shard_size == 0:
                raise ValueError('Cannot scatter an empty JSONL file with ensure_at_least_one_per_rank=False.')

        shards = [data[i * shard_size : (i+1) * shard_size] for i in range(world_size)]

        while len(shards) < world_size: # number of shards must be equal to the world size
            shards.append([])

        # need to pad as each shard needs to have same size so all ranks call forward()
        for rank in range(world_size):
            target = shard_size - len(shards[rank])
            if target > 0:
                shards[rank].extend(prepare_dummy_line_fn() for _ in range(target))

    if ddp:
        # scatter the shards for respective rank
        buffer_obj = [None]
        dist.scatter_object_list(buffer_obj, scatter_object_input_list=shards if is_master_process else None, src=0)
        data = buffer_obj[0]
    else:
        data = shards[0]

    return data
