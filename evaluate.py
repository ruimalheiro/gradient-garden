import argparse

from logger import logger
from engine.checkpoints import load_checkpoint_for_inference
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
    evaluate_arc_challenge
)
from config import TrainingStage


def check_stage_for_validation(stage: TrainingStage, parser: argparse.ArgumentParser):
    if stage not in (TrainingStage.PRETRAINING, TrainingStage.INSTRUCT):
        parser.error('--validation is only supported for pretraining and instruct checkpoints.')

def check_stage_for_evals(stage: TrainingStage, parser: argparse.ArgumentParser):
    if stage != TrainingStage.PRETRAINING:
        parser.error('--hellaswag, --winogrande, or --arc-challenge are only supported for pretraining checkpoints.')

if __name__ == '__main__':
    logger.set_master(True)

    parser = argparse.ArgumentParser(description='Evals / Benchmark Script Options')

    parser.add_argument('--checkpoint', type=str, required=True, help='Checkpoint file path to load.')

    parser.add_argument('--validation', action='store_true', help='Run validation.')
    parser.add_argument('--validation-steps', type=int, default=1000, help='Number of validation steps to take.')

    parser.add_argument('--hellaswag', action='store_true', help='Run HellaSwag eval.')
    parser.add_argument('--hellaswag-examples', type=int, default=-1, help='Number of HellaSwag examples to run. Use -1 for all.')

    parser.add_argument('--winogrande', action='store_true', help='Run WinoGrande eval.')
    parser.add_argument('--winogrande-examples', type=int, default=-1, help='Number of WinoGrande examples to run. Use -1 for all.')

    parser.add_argument('--arc-challenge', action='store_true', help='Run ARC-Challenge eval.')
    parser.add_argument('--arc-challenge-examples', type=int, default=-1, help='Number of ARC-Challenge examples to run. Use -1 for all.')

    add_runtime_args(parser)
    add_output_args(parser, default_dir='outputs/evals')

    args = parser.parse_args()

    validate_runtime_args(args, parser)

    if not any([args.validation, args.hellaswag, args.winogrande, args.arc_challenge]):
        parser.error('Select at least one eval: --validation, --hellaswag, --winogrande, or --arc-challenge')

    if args.validation and args.validation_steps <= 0:
        parser.error('--validation-steps must be greater than 0')
    if args.hellaswag and (args.hellaswag_examples == 0 or args.hellaswag_examples < -1):
        parser.error('--hellaswag-examples must be -1 or greater than 0')
    if args.winogrande and (args.winogrande_examples == 0 or args.winogrande_examples < -1):
        parser.error('--winogrande-examples must be -1 or greater than 0')
    if args.arc_challenge and (args.arc_challenge_examples == 0 or args.arc_challenge_examples < -1):
        parser.error('--arc-challenge-examples must be -1 or greater than 0')

    validate_file_path(args.checkpoint, parser)

    checkpoint_data = load_checkpoint_for_inference(args.checkpoint)

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
        check_stage_for_evals(checkpoint_data.config.training.stage, parser)
        results['hellaswag'] = evaluate_hellaswag(
            inference_runtime=inference_runtime,
            config=checkpoint_data.config,
            batch_size=args.batch_size,
            num_examples=args.hellaswag_examples
        )
    if args.winogrande:
        check_stage_for_evals(checkpoint_data.config.training.stage, parser)
        results['winogrande'] = evaluate_winogrande(
            inference_runtime=inference_runtime,
            config=checkpoint_data.config,
            batch_size=args.batch_size,
            num_examples=args.winogrande_examples
        )
    if args.arc_challenge:
        check_stage_for_evals(checkpoint_data.config.training.stage, parser)
        results['arc_challenge'] = evaluate_arc_challenge(
            inference_runtime=inference_runtime,
            config=checkpoint_data.config,
            batch_size=args.batch_size,
            num_examples=args.arc_challenge_examples
        )

    data = {
        'name': name,
        'created_at_utc': timestamp.isoformat(),
        'checkpoint': args.checkpoint,
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
        },
        'results': results,
    }

    logger.info({
        'name': name,
        'created_at_utc': timestamp.isoformat(),
        'checkpoint': args.checkpoint,
        'output_path': str(output_path),
        'config': data['config'],
    }, is_json=True)

    write_outputs(output_path, data)
    logger.info(f'Evals outputs saved to: {output_path}')
