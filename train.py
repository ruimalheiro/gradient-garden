import argparse

from config import load_config, TrainingStage
from engine import Trainer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train Script Options')

    parser.add_argument('--config', type=str, default=None, help='Path to the configuration definition (.yaml). If not provided, default values are used.')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--pretraining', action='store_true', help='Forces pretraining stage.')
    group.add_argument('--instruct', action='store_true', help='Forces instruct stage.')
    group.add_argument('--dpo', action='store_true', help='Forces DPO stage.')

    checkpoint_group = parser.add_mutually_exclusive_group()
    checkpoint_group.add_argument('--pretraining-checkpoint', type=str, default=None, help='Pretraining checkpoint to load.')
    checkpoint_group.add_argument('--instruct-checkpoint', type=str, default=None, help='Instruct checkpoint to load.')
    checkpoint_group.add_argument('--dpo-checkpoint', type=str, default=None, help='DPO checkpoint to load.')

    parser.add_argument('--reset-optimizers', action='store_true', help='Reset the optimizers state when loading a checkpoint.')
    parser.add_argument('--start-step', type=int, default=None, help='Starting step number for training.')

    args = parser.parse_args()

    cfg = load_config(args.config)

    if args.pretraining:
        cfg.training.stage = TrainingStage.PRETRAINING
    elif args.instruct:
        cfg.training.stage = TrainingStage.INSTRUCT
    elif args.dpo:
        cfg.training.stage = TrainingStage.DPO

    trainer = Trainer(
        config=cfg,
        args=args
    )
    trainer.train()
