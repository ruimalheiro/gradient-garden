import argparse

from config import load_config, TrainingStage
from engine.trainer import Trainer
from recipes.config import load_recipe


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train Script Options')

    config_group = parser.add_mutually_exclusive_group()
    config_group.add_argument('--config', type=str, default=None, help='Path to the configuration definition (.yaml). If not provided, default values are used.')
    config_group.add_argument('--recipe', type=str, default=None, help='Path to a recipe YAML file.')

    stage_group = parser.add_mutually_exclusive_group()
    stage_group.add_argument('--pretraining', action='store_true', help='Forces pretraining stage.')
    stage_group.add_argument('--instruct', action='store_true', help='Forces instruct stage.')
    stage_group.add_argument('--dpo', action='store_true', help='Forces DPO stage.')

    checkpoint_group = parser.add_mutually_exclusive_group()
    checkpoint_group.add_argument('--checkpoint', type=str, default=None, help='Checkpoint file path to load.')

    parser.add_argument('--reset-optimizers', action='store_true', help='Reset the optimizers state when loading a checkpoint.')
    parser.add_argument('--start-step', type=int, default=None, help='Starting step number for training.')

    args = parser.parse_args()

    if args.recipe and (args.pretraining or args.instruct or args.dpo):
        parser.error('--recipe defines the training stage. Cannot combine --recipe with --pretraining, --instruct, or --dpo.')

    if args.recipe:
        cfg = load_recipe(args.recipe).config
    else:
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
