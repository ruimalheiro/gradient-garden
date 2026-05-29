import sys
import argparse
import json

from logger import logger
from config import load_config
from utils import load_json_file
from recipes.config import load_recipe
from datasets_preparation.data_preparation_utils import get_max_number_of_cpu_processes
from datasets_preparation.prepare_hellaswag_dataset import prepare_hellaswag_dataset
from datasets_preparation.prepare_winogrande_dataset import prepare_winogrande_dataset
from datasets_preparation.prepare_arc_challenge_dataset import prepare_arc_challenge_dataset
from datasets_preparation.prepare_pretraining_dataset import prepare_pretraining_dataset
from datasets_preparation.prepare_instruct_dataset import prepare_instruct_dataset
from datasets_preparation.prepare_dpo_dataset import prepare_dpo_dataset
from datasets_preparation.prepare_recipe_data import prepare_recipe_data
from engine.workload_estimation import estimate_workload_tokens_from_config


if __name__ == '__main__':
    logger.set_master(True)

    parser = argparse.ArgumentParser(description='Datasets Preparation Script Options')

    config_group = parser.add_mutually_exclusive_group()
    config_group.add_argument('--config', type=str, default=None, help='Path to the configuration definition (.yaml). If not provided, default values are used.')
    config_group.add_argument('--recipe', type=str, default=None, help='Path to a recipe YAML file.')

    dataset_group = parser.add_mutually_exclusive_group()
    dataset_group.add_argument('--hellaswag', action='store_true', help='Prepare HellaSwag eval dataset')
    dataset_group.add_argument('--winogrande', action='store_true', help='Prepare WinoGrande eval dataset')
    dataset_group.add_argument('--arc-challenge', action='store_true', help='Prepare ARC-Challenge eval dataset')
    dataset_group.add_argument('--pretraining', action='store_true', help='Prepare pretraining dataset')
    dataset_group.add_argument('--instruct', action='store_true', help='Prepare instruct (SFT) dataset')
    dataset_group.add_argument('--dpo', action='store_true', help='Prepare DPO (Direct Preference Optimization) dataset')

    parser.add_argument('--mix-file', type=str, default=None, help='Path to custom mix file')
    parser.add_argument('--estimate-token-target', action='store_true', help='Estimates the token count required for the current model configuration')

    args = parser.parse_args()

    dataset_group_flags_set = (
        args.hellaswag or
        args.winogrande or
        args.arc_challenge or
        args.pretraining or
        args.instruct or
        args.dpo
    )

    if args.recipe and (dataset_group_flags_set or args.mix_file):
        parser.error('--recipe defines the data configuration. Cannot combine --recipe with any other flag.')

    # if args.estimate_token_target and not (args.pretraining or args.instruct):
    #     parser.error('--estimate-token-target can only be used when preparing pretraining or instruct datasets.')

    # estimate_workload_tokens_from_config
    if args.recipe:
        recipe = load_recipe(args.recipe)
        cfg = recipe.config
    else:
        if not dataset_group_flags_set:
            parser.error('Please specify one dataset flag, or use --recipe.')
        cfg = load_config(args.config)

    if args.estimate_token_target:
        estimate_workload_tokens_from_config(config=cfg)
        sys.exit(0)

    num_proc = get_max_number_of_cpu_processes(cfg)

    if args.recipe:
        prepare_recipe_data(recipe=recipe, num_proc=num_proc)
    else:
        if (args.hellaswag or args.winogrande or args.arc_challenge) and args.mix_file:
            parser.error('"--mix-file" is only supported for training datasets.')

        datasets_mix = load_json_file(args.mix_file) if args.mix_file is not None else None

        if args.hellaswag:
            prepare_hellaswag_dataset(config=cfg, num_proc=num_proc)
        elif args.winogrande:
            prepare_winogrande_dataset(config=cfg, num_proc=num_proc)
        elif args.arc_challenge:
            prepare_arc_challenge_dataset(config=cfg, num_proc=num_proc)
        elif args.pretraining:
            prepare_pretraining_dataset(config=cfg, datasets_mix=datasets_mix, num_proc=num_proc)
        elif args.instruct:
            prepare_instruct_dataset(config=cfg, datasets_mix=datasets_mix, num_proc=num_proc)
        elif args.dpo:
            prepare_dpo_dataset(config=cfg, datasets_mix=datasets_mix, num_proc=num_proc)

    logger.info('Data preparation completed.')
