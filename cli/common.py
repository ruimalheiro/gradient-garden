import argparse

from pathlib import Path


def validate_file_path(path: str, parser: argparse.ArgumentParser):
    file_path = Path(path)
    if not file_path.exists():
        parser.error(f'The path does not exist: {path}')
    if not file_path.is_file():
        parser.error(f'The path does not point to a file: {path}')

def validate_input_prompts_list(prompts, parser: argparse.ArgumentParser) -> list[str]:
    if not isinstance(prompts, list):
        parser.error('--prompts must be a JSON file containing a list of strings.')

    if len(prompts) == 0:
        parser.error('--prompts must contain at least one prompt.')

    if not all(isinstance(prompt, str) for prompt in prompts):
        parser.error('--prompts must contain only strings.')

    return prompts

def add_generation_args(parser: argparse.ArgumentParser):
    parser.add_argument('--temperature', type=float, default=0.6, help='Temperature')
    parser.add_argument('--top-p', type=float, default=0.9, help='Top-P')
    parser.add_argument('--max-gen-len', type=int, default=128, help='Max number of tokens to generate.')
    parser.add_argument('--full-seq', action='store_true', help='Return full sequence including the prompt')
    parser.add_argument(
        '--instruct',
        action='store_true',
        help='Include the instruct control tokens in the prompt. Should not be set when testing base model.'
    )
    parser.add_argument('--use-kv-cache', action='store_true')
    parser.add_argument(
        '--repetition-penalty',
        type=float,
        default=1.0,
        help='Penalty for already generated tokens. 1.0 means disabled. Common values: ~1.05 to ~1.2.',
    )
    parser.add_argument(
        '--no-repeat-ngram-size',
        type=int,
        default=1,
        help='Block repeated ngrams of this size. 1 means disabled. Common values: ~3 to ~5.',
    )

def validate_generation_args(args: argparse.Namespace, parser: argparse.ArgumentParser):
    if args.temperature < 0:
        parser.error('--temperature must be >= 0.')
    if not (0.0 < args.top_p <= 1.0):
        parser.error('--top-p must be between 0.0 and 1.0.')
    if args.max_gen_len <= 0:
        parser.error('--max-gen-len must be > 0.')
    if args.repetition_penalty <= 0:
        parser.error('--repetition-penalty must be > 0')
    if args.no_repeat_ngram_size < 1:
        parser.error('--no-repeat-ngram-size must be >= 1')

def add_runtime_args(parser: argparse.ArgumentParser):
    parser.add_argument(
        '--device',
        type=str,
        default='cuda',
        choices=['cpu', 'cuda'],
        help='Target device type'
    )
    parser.add_argument(
        '--dtype',
        type=str,
        default='auto',
        choices=['auto', 'bf16', 'fp16', 'fp32'],
        help='By default the checkpoint/config dtype will be used.'
    )
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--batch-size', type=int, default=1)
    parser.add_argument('--use-torch-compile', action='store_true', help='Use torch compile')

def validate_runtime_args(args: argparse.Namespace, parser: argparse.ArgumentParser):
    if args.batch_size <= 0:
        parser.error('--batch-size must be > 0.')

def add_output_args(parser: argparse.ArgumentParser, *, default_dir):
    parser.add_argument('--output-file-name', type=str, default=None)
    parser.add_argument('--output-dir', type=str, default=default_dir)
