import argparse
import json

from config import load_config
from datasets_preparation import (
    prepare_hellaswag_dataset,
    prepare_winogrande_dataset,
    prepare_arc_challenge_dataset,
    prepare_pretraining_dataset,
    prepare_instruct_dataset,
    prepare_dpo_dataset
)


def load_custom_dataset_mix(mix_file_path):
    if mix_file_path is None:
        return None 
    with open(mix_file_path, 'r') as file:
        return json.load(file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Datasets Preparation Script Options')

    parser.add_argument('--config', type=str, default=None, help='Path to the configuration definition (.yaml). If not provided, default values are used.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--hellaswag', action='store_true', help='Prepare HellaSwag eval dataset')
    group.add_argument('--winogrande', action='store_true', help='Prepare WinoGrande eval dataset')
    group.add_argument('--arc-challenge', action='store_true', help='Prepare ARC-Challenge eval dataset')
    group.add_argument('--pretraining', action='store_true', help='Prepare pretraining dataset')
    group.add_argument('--instruct', action='store_true', help='Prepare instruct (SFT) dataset')
    group.add_argument('--dpo', action='store_true', help='Prepare DPO (Direct Preference Optimization) dataset')

    parser.add_argument('--mix-file', type=str, default=None, help='Path to custom mix file')

    args = parser.parse_args()

    cfg = load_config(args.config)

    if (args.hellaswag or args.winogrande or args.arc_challenge) and args.mix_file:
        parser.error('"--mix-file" is only supported for training datasets.')

    datasets_mix = load_custom_dataset_mix(args.mix_file)

    if args.hellaswag:
        prepare_hellaswag_dataset(config=cfg)
    elif args.winogrande:
        prepare_winogrande_dataset(config=cfg)
    elif args.arc_challenge:
        prepare_arc_challenge_dataset(config=cfg)
    elif args.pretraining:
        prepare_pretraining_dataset(config=cfg, datasets_mix=datasets_mix)
    elif args.instruct:
        prepare_instruct_dataset(config=cfg, datasets_mix=datasets_mix)
    elif args.dpo:
        prepare_dpo_dataset(config=cfg, datasets_mix=datasets_mix)
