import sys
import argparse
import json

from logger import logger
from config import load_config, TrainingStage
from utils import load_json_file
from recipes.config import load_recipe
from datasets_preparation.data_preparation_utils import get_max_number_of_cpu_processes
from datasets_preparation.evals.prepare_hellaswag_dataset import prepare_hellaswag_dataset
from datasets_preparation.evals.prepare_winogrande_dataset import prepare_winogrande_dataset
from datasets_preparation.evals.prepare_arc_challenge_dataset import prepare_arc_challenge_dataset
from datasets_preparation.evals.prepare_ifeval_no_external_dataset import prepare_ifeval_no_external_dataset
from datasets_preparation.evals.prepare_custom_sft_smoke_dataset import prepare_custom_sft_smoke_dataset
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

    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument('--hellaswag', action='store_true', help='Prepare HellaSwag eval dataset')
    action_group.add_argument('--winogrande', action='store_true', help='Prepare WinoGrande eval dataset')
    action_group.add_argument('--arc-challenge', action='store_true', help='Prepare ARC-Challenge eval dataset')
    action_group.add_argument('--ifeval-no-external', action='store_true', help='Prepare IFEval (no external) eval dataset')
    action_group.add_argument('--custom-sft-smoke', action='store_true', help='Prepare custom SFT smoke eval dataset')

    action_group.add_argument('--pretraining', action='store_true', help='Prepare pretraining dataset')
    action_group.add_argument('--instruct', action='store_true', help='Prepare instruct (SFT) dataset')
    action_group.add_argument('--dpo', action='store_true', help='Prepare DPO (Direct Preference Optimization) dataset')
    action_group.add_argument('--estimate-token-target', action='store_true', help='Estimates the token count required for the current model configuration')

    parser.add_argument('--mix-file', type=str, default=None, help='Path to custom mix file')

    args = parser.parse_args()

    dataset_group_flags_set = (
        args.hellaswag or
        args.winogrande or
        args.arc_challenge or
        args.ifeval_no_external or
        args.custom_sft_smoke or
        args.pretraining or
        args.instruct or
        args.dpo
    )

    action_group_flags_set = (
        dataset_group_flags_set or
        args.estimate_token_target
    )

    if args.recipe and (dataset_group_flags_set or args.mix_file):
        parser.error(
            '--recipe defines the data configuration. Cannot combine --recipe '
            'with dataset preparation flags or --mix-file.'
        )

    if args.estimate_token_target and args.mix_file:
        parser.error('--estimate-token-target cannot be combined with --mix-file.')

    if args.recipe:
        recipe = load_recipe(args.recipe)
        cfg = recipe.config
    else:
        if not action_group_flags_set:
            parser.error('Please specify one dataset flag/action, or use --recipe.')
        cfg = load_config(args.config)

    if args.estimate_token_target:
        if cfg.training.stage == TrainingStage.DPO:
            parser.error('--estimate-token-target is not supported for DPO.')
        estimate_workload_tokens_from_config(config=cfg)
        sys.exit(0)

    num_proc = get_max_number_of_cpu_processes(cfg)

    if args.recipe:
        prepare_recipe_data(recipe=recipe, num_proc=num_proc)
    else:
        if (args.hellaswag or args.winogrande or args.arc_challenge or args.ifeval_no_external or args.custom_sft_smoke) and args.mix_file:
            parser.error('"--mix-file" is only supported for training datasets.')

        datasets_mix = load_json_file(args.mix_file) if args.mix_file is not None else None

        if args.hellaswag:
            prepare_hellaswag_dataset(config=cfg, num_proc=num_proc)
        elif args.winogrande:
            prepare_winogrande_dataset(config=cfg, num_proc=num_proc)
        elif args.arc_challenge:
            prepare_arc_challenge_dataset(config=cfg, num_proc=num_proc)
        elif args.ifeval_no_external:
            prepare_ifeval_no_external_dataset(config=cfg, num_proc=num_proc)
        elif args.custom_sft_smoke:
            prepare_custom_sft_smoke_dataset(config=cfg, num_proc=num_proc)
        elif args.pretraining:
            prepare_pretraining_dataset(config=cfg, datasets_mix=datasets_mix, num_proc=num_proc)
        elif args.instruct:
            prepare_instruct_dataset(config=cfg, datasets_mix=datasets_mix, num_proc=num_proc)
        elif args.dpo:
            prepare_dpo_dataset(config=cfg, datasets_mix=datasets_mix, num_proc=num_proc)

    logger.info('Data preparation completed.')
