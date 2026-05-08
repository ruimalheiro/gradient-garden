import argparse

from config import load_config
from engine import Trainer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train Script Options')

    parser.add_argument('--config', type=str, default=None, help='Path to the configuration definition (.yaml). If not provided, default values are used.')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--pretraining-checkpoint', type=str, default=None, help='Pretraining checkpoint to load.')
    group.add_argument('--instruct-checkpoint', type=str, default=None, help='Instruct checkpoint to load.')
    group.add_argument('--dpo-checkpoint', type=str, default=None, help='DPO checkpoint to load.')

    parser.add_argument('--reset-optimizers', action='store_true', help='Reset the optimizers state when loading a checkpoint.')
    parser.add_argument('--start-step', type=int, default=None, help='Starting step number for training.')

    args = parser.parse_args()

    cfg = load_config(args.config)

    trainer = Trainer(
        config=cfg,
        args=args
    )
    trainer.train()
