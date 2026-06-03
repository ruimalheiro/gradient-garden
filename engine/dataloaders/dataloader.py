from config import TrainingStage
from engine.dataloaders.pretraining_dataloader import PretrainingDataLoader
from engine.dataloaders.instruct_dataloader import InstructDataLoader
from engine.dataloaders.dpo_dataloader import DirectPreferenceOptimizationDataLoader
from logger import logger


def init_data_loaders(
    batch_size,
    sequence_length,
    is_master_process,
    ddp_rank,
    ddp_world_size,
    data_root,
    training_stage,
    number_of_cpu_processes,
    ignore_index,
    pad_id=None,
    validation_only=False
):
    train_loader = None
    if training_stage == TrainingStage.PRETRAINING:
        logger.section('Pretraining Data Loaders')

        if validation_only is False:
            train_loader = PretrainingDataLoader(
                batch_size=batch_size,
                sequence_length=sequence_length,
                is_master_process=is_master_process,
                ddp_rank=ddp_rank,
                ddp_world_size=ddp_world_size,
                data_root=data_root,
                split='train',
                use_shuffle=True
            )
        val_loader = PretrainingDataLoader(
            batch_size=batch_size,
            sequence_length=sequence_length,
            is_master_process=is_master_process,
            ddp_rank=ddp_rank,
            ddp_world_size=ddp_world_size,
            data_root=data_root,
            split='val',
            use_shuffle=False
        )
    elif training_stage == TrainingStage.INSTRUCT:
        assert pad_id is not None

        logger.section('Instruct Finetuning Data Loaders')

        if validation_only is False:
            train_loader = InstructDataLoader(
                batch_size=batch_size,
                sequence_length=sequence_length,
                is_master_process=is_master_process,
                ddp_rank=ddp_rank,
                ddp_world_size=ddp_world_size,
                data_root=data_root,
                split='train',
                use_shuffle=True,
                pad_id=pad_id,
                drop_last=True,
                number_of_cpu_processes=number_of_cpu_processes,
                ignore_index=ignore_index
            )
        val_loader = InstructDataLoader(
            batch_size=batch_size,
            sequence_length=sequence_length,
            is_master_process=is_master_process,
            ddp_rank=ddp_rank,
            ddp_world_size=ddp_world_size,
            data_root=data_root,
            split='val',
            use_shuffle=False,
            pad_id=pad_id,
            drop_last=False,
            number_of_cpu_processes=number_of_cpu_processes,
            ignore_index=ignore_index
        )
    elif training_stage == TrainingStage.DPO:
        assert pad_id is not None

        logger.section('Direct Preference Optimization Data Loaders')

        if validation_only is False:
            train_loader = DirectPreferenceOptimizationDataLoader(
                batch_size=batch_size,
                sequence_length=sequence_length,
                is_master_process=is_master_process,
                ddp_rank=ddp_rank,
                ddp_world_size=ddp_world_size,
                data_root=data_root,
                split='train',
                use_shuffle=True,
                pad_id=pad_id,
                drop_last=True,
                number_of_cpu_processes=number_of_cpu_processes,
                ignore_index=ignore_index
            )
        val_loader = DirectPreferenceOptimizationDataLoader(
            batch_size=batch_size,
            sequence_length=sequence_length,
            is_master_process=is_master_process,
            ddp_rank=ddp_rank,
            ddp_world_size=ddp_world_size,
            data_root=data_root,
            split='val',
            use_shuffle=False,
            pad_id=pad_id,
            drop_last=False,
            number_of_cpu_processes=number_of_cpu_processes,
            ignore_index=ignore_index
        )
    else:
        raise ValueError('Invalid training stage for dataloader')

    return train_loader, val_loader
