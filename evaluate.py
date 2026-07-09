import argparse

from logger import logger
from engine.checkpoints import (
    load_checkpoint_for_inference,
    load_shallow_hf_checkpoint_for_inference
)
from utils import (
    set_seed,
    build_output_path_for_run,
    write_outputs
)
from inference.runtime import prepare_runtime_for_inference
from cli.common import (
    validate_file_path,
    add_runtime_args,
    validate_runtime_args,
    add_output_args
)
from evals.validation import evaluate_validation_ppl
from evals.evaluation import (
    evaluate_hellaswag,
    evaluate_winogrande,
    evaluate_arc_challenge,
    evaluate_ifeval_no_external,
    evaluate_custom_sft_smoke
)
from config import TrainingStage


def check_stage_for_validation(stage: TrainingStage, parser: argparse.ArgumentParser):
    if stage not in (TrainingStage.PRETRAINING, TrainingStage.INSTRUCT):
        parser.error('--validation is only supported for pretraining and instruct checkpoints.')

def check_stage_for_multiple_choice_evals(stage: TrainingStage, parser: argparse.ArgumentParser):
    if stage not in (TrainingStage.PRETRAINING, TrainingStage.INSTRUCT):
        parser.error(
            '--hellaswag, --winogrande, and --arc-challenge '
            'are only supported for pretraining and instruct checkpoints.'
        )

def check_stage_for_instruction_following_evals(stage: TrainingStage, parser: argparse.ArgumentParser):
    if stage != TrainingStage.INSTRUCT:
        parser.error(
            '--ifeval-no-external and --custom-sft-smoke '
            'are only supported for instruct checkpoints.'
        )

def check_num_examples(*, enabled: bool, flag_name: str, value: int, parser: argparse.ArgumentParser):
    if enabled and (value == 0 or value < -1):
        parser.error(f'{flag_name} must be -1 or greater than 0')

def check_dataset_path_is_set(*, enabled: bool, flag_name: str, value: str, parser: argparse.ArgumentParser):
    if enabled and not value:
        parser.error(f'{flag_name} must be set.')

if __name__ == '__main__':
    logger.set_master(True)

    parser = argparse.ArgumentParser(description='Evals / Benchmark Script Options')

    checkpoint_group = parser.add_mutually_exclusive_group(required=True)
    checkpoint_group.add_argument('--checkpoint', type=str, help='Checkpoint file path to load.')
    checkpoint_group.add_argument('--hf-checkpoint', type=str, help='Hugging Face model id or checkpoint path to load.')

    parser.add_argument('--validation', action='store_true', help='Run validation.')
    parser.add_argument('--validation-steps', type=int, default=1000, help='Number of validation steps to take.')
    parser.add_argument('--validation-path', type=str, default=None, help='Dataset path')

    parser.add_argument('--hellaswag', action='store_true', help='Run HellaSwag eval.')
    parser.add_argument('--hellaswag-examples', type=int, default=-1, help='Number of HellaSwag examples to run. Use -1 for all.')
    parser.add_argument('--hellaswag-path', type=str, default=None, help='Dataset path')

    parser.add_argument('--winogrande', action='store_true', help='Run WinoGrande eval.')
    parser.add_argument('--winogrande-examples', type=int, default=-1, help='Number of WinoGrande examples to run. Use -1 for all.')
    parser.add_argument('--winogrande-path', type=str, default=None, help='Dataset path')

    parser.add_argument('--arc-challenge', action='store_true', help='Run ARC-Challenge eval.')
    parser.add_argument('--arc-challenge-examples', type=int, default=-1, help='Number of ARC-Challenge examples to run. Use -1 for all.')
    parser.add_argument('--arc-challenge-path', type=str, default=None, help='Dataset path')

    parser.add_argument('--ifeval-no-external', action='store_true', help='Run IFEval (no external) eval.')
    parser.add_argument('--ifeval-no-external-examples', type=int, default=-1, help='Number of IFEval (no external) examples to run. Use -1 for all.')
    parser.add_argument('--ifeval-no-external-path', type=str, default=None, help='Dataset path')

    parser.add_argument('--custom-sft-smoke', action='store_true', help='Run custom SFT smoke eval.')
    parser.add_argument('--custom-sft-smoke-examples', type=int, default=-1, help='Number of custom SFT smoke examples to run. Use -1 for all.')
    parser.add_argument('--custom-sft-smoke-path', type=str, default=None, help='Dataset path')

    parser.add_argument('--stage', choices=[stage.value for stage in TrainingStage], required=False, default=None, help='Training stage used to select the validation dataloader.')

    add_runtime_args(parser)
    add_output_args(parser, default_dir='outputs/evals')

    args = parser.parse_args()

    validate_runtime_args(args, parser)

    if not any([
        args.validation,
        args.hellaswag,
        args.winogrande,
        args.arc_challenge,
        args.ifeval_no_external,
        args.custom_sft_smoke
    ]):
        parser.error(
            'Select at least one eval: '
            '--validation, --hellaswag, --winogrande, --arc-challenge, '
            '--ifeval-no-external, or --custom-sft-smoke'
        )

    if args.validation and args.validation_steps <= 0:
        parser.error('--validation-steps must be greater than 0')

    check_num_examples(enabled=args.hellaswag, flag_name='--hellaswag-examples', value=args.hellaswag_examples, parser=parser)
    check_num_examples(enabled=args.winogrande, flag_name='--winogrande-examples', value=args.winogrande_examples, parser=parser)
    check_num_examples(enabled=args.arc_challenge, flag_name='--arc-challenge-examples', value=args.arc_challenge_examples, parser=parser)
    check_num_examples(enabled=args.ifeval_no_external, flag_name='--ifeval-no-external-examples', value=args.ifeval_no_external_examples, parser=parser)
    check_num_examples(enabled=args.custom_sft_smoke, flag_name='--custom-sft-smoke-examples', value=args.custom_sft_smoke_examples, parser=parser)

    if args.checkpoint:
        checkpoint = args.checkpoint
        validate_file_path(checkpoint, parser)
        checkpoint_data = load_checkpoint_for_inference(checkpoint)
    elif args.hf_checkpoint:
        checkpoint = args.hf_checkpoint
        checkpoint_data = load_shallow_hf_checkpoint_for_inference(checkpoint)

        if not args.stage:
            parser.error(f'--stage must be set when using --hf-checkpoint')

        checkpoint_data.config.training.stage = TrainingStage(args.stage)

        if args.validation:
            check_dataset_path_is_set(enabled=args.validation, flag_name='--validation-path', value=args.validation_path, parser=parser)
            checkpoint_data.config.paths.datasets.training_path = args.validation_path
        if args.hellaswag:
            check_dataset_path_is_set(enabled=args.hellaswag, flag_name='--hellaswag-path', value=args.hellaswag_path, parser=parser)
            checkpoint_data.config.paths.evals.hellaswag_path = args.hellaswag_path
        if args.winogrande:
            check_dataset_path_is_set(enabled=args.winogrande, flag_name='--winogrande-path', value=args.winogrande_path, parser=parser)
            checkpoint_data.config.paths.evals.winogrande_path = args.winogrande_path
        if args.arc_challenge:
            check_dataset_path_is_set(enabled=args.arc_challenge, flag_name='--arc-challenge-path', value=args.arc_challenge_path, parser=parser)
            checkpoint_data.config.paths.evals.arc_challenge_path = args.arc_challenge_path
        if args.ifeval_no_external:
            check_dataset_path_is_set(enabled=args.ifeval_no_external, flag_name='--ifeval-no-external-path', value=args.ifeval_no_external_path, parser=parser)
            checkpoint_data.config.paths.evals.ifeval_no_external_path = args.ifeval_no_external_path
        if args.custom_sft_smoke:
            check_dataset_path_is_set(enabled=args.custom_sft_smoke, flag_name='--custom-sft-smoke-path', value=args.custom_sft_smoke_path, parser=parser)
            checkpoint_data.config.paths.evals.custom_sft_smoke_path = args.custom_sft_smoke_path

    set_seed(args.seed)

    output_path, name, timestamp = build_output_path_for_run(
        run_name=checkpoint_data.config.run.name,
        stage=checkpoint_data.config.training.stage.value,
        output_file_name=args.output_file_name,
        output_dir=args.output_dir,
        extension='json'
    )

    inference_runtime = prepare_runtime_for_inference(
        checkpoint_data=checkpoint_data,
        dtype=args.dtype,
        device=args.device,
        use_torch_compile=args.use_torch_compile
    )

    results = {}

    if args.validation:
        check_stage_for_validation(checkpoint_data.config.training.stage, parser)
        results['validation'] = evaluate_validation_ppl(
            inference_runtime=inference_runtime,
            config=checkpoint_data.config,
            batch_size=args.batch_size,
            validation_steps=args.validation_steps,
            ignore_index=checkpoint_data.config.tokenizer.ignore_index
        )
    if args.hellaswag:
        check_stage_for_multiple_choice_evals(checkpoint_data.config.training.stage, parser)
        results['hellaswag'] = evaluate_hellaswag(
            inference_runtime=inference_runtime,
            config=checkpoint_data.config,
            batch_size=args.batch_size,
            num_examples=args.hellaswag_examples
        )
    if args.winogrande:
        check_stage_for_multiple_choice_evals(checkpoint_data.config.training.stage, parser)
        results['winogrande'] = evaluate_winogrande(
            inference_runtime=inference_runtime,
            config=checkpoint_data.config,
            batch_size=args.batch_size,
            num_examples=args.winogrande_examples
        )
    if args.arc_challenge:
        check_stage_for_multiple_choice_evals(checkpoint_data.config.training.stage, parser)
        results['arc_challenge'] = evaluate_arc_challenge(
            inference_runtime=inference_runtime,
            config=checkpoint_data.config,
            batch_size=args.batch_size,
            num_examples=args.arc_challenge_examples
        )
    if args.ifeval_no_external:
        check_stage_for_instruction_following_evals(checkpoint_data.config.training.stage, parser)
        results['ifeval_no_external'] = evaluate_ifeval_no_external(
            inference_runtime=inference_runtime,
            config=checkpoint_data.config,
            batch_size=args.batch_size,
            num_examples=args.ifeval_no_external_examples
        )
    if args.custom_sft_smoke:
        check_stage_for_instruction_following_evals(checkpoint_data.config.training.stage, parser)
        results['custom_sft_smoke'] = evaluate_custom_sft_smoke(
            inference_runtime=inference_runtime,
            config=checkpoint_data.config,
            batch_size=args.batch_size,
            num_examples=args.custom_sft_smoke_examples
        )

    data = {
        'name': name,
        'created_at_utc': timestamp.isoformat(),
        'checkpoint': checkpoint,
        'config': {
            'device': args.device,
            'dtype': args.dtype,
            'resolved_device': str(inference_runtime.device),
            'resolved_dtype': str(inference_runtime.dtype),
            'seed': args.seed,
            'batch_size': args.batch_size,
            'use_torch_compile': args.use_torch_compile,
            'validation': args.validation,
            'validation_steps': args.validation_steps,
            'hellaswag': args.hellaswag,
            'hellaswag_examples': args.hellaswag_examples,
            'winogrande': args.winogrande,
            'winogrande_examples': args.winogrande_examples,
            'arc_challenge': args.arc_challenge,
            'arc_challenge_examples': args.arc_challenge_examples,
            'ifeval_no_external': args.ifeval_no_external,
            'ifeval_no_external_examples': args.ifeval_no_external_examples,
            'custom_sft_smoke': args.custom_sft_smoke,
            'custom_sft_smoke_examples': args.custom_sft_smoke_examples,
        },
        'results': results,
    }

    logger.info({
        'name': name,
        'created_at_utc': timestamp.isoformat(),
        'checkpoint': checkpoint,
        'output_path': str(output_path),
        'config': data['config'],
    }, is_json=True)

    write_outputs(output_path, data)
    logger.info(f'Evals outputs saved to: {output_path}')
