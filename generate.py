import argparse
import torch
import random
import json

from logger import logger
from pathlib import Path
from config import GlobalConfig
from engine.checkpoints import load_checkpoint_for_inference
from utils import (
    generate_name,
    load_json_file,
    set_seed
)
from inference.runtime import prepare_runtime_for_inference
from inference.generation import generate_and_decode


def validate_file_path(path: str, parser: argparse.ArgumentParser):
    file_path = Path(path)
    if not file_path.exists():
        parser.error(f'The path does not exist: {path}')
    if not file_path.is_file():
        parser.error(f'The path does not point to a file: {path}')

def validate_prompts(prompts, parser: argparse.ArgumentParser) -> list[str]:
    if not isinstance(prompts, list):
        parser.error('--prompts must be a JSON file containing a top-level list of strings.')

    if len(prompts) == 0:
        parser.error('--prompts must contain at least one prompt.')

    if not all(isinstance(prompt, str) for prompt in prompts):
        parser.error('--prompts must contain only strings.')

    return prompts

def build_output_path(
    *,
    config: GlobalConfig,
    output_file_name: str,
    output_dir: str = 'outputs/generations',
) -> tuple[Path, str, object]:
    if output_file_name is not None:
        output_file_name = Path(output_file_name).stem
    generation_name, timestamp = generate_name(
        name=output_file_name if output_file_name is not None else config.run.name
    )

    return (
        Path(output_dir) / config.training.stage.value / f'{generation_name}.json',
        generation_name,
        timestamp
    )

def write_outputs(output_file_path: Path, data: dict):
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    output_file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    logger.set_master(True)

    parser = argparse.ArgumentParser(description='Inference Script Options')

    parser.add_argument('--checkpoint', type=str, required=True, help='Checkpoint file path to load.')
    parser.add_argument('--prompts', type=str, required=True, help='Path to the prompts file.')

    parser.add_argument('--max-gen-len', type=int, default=128, help='Max number of tokens to generate.')
    parser.add_argument('--temperature', type=float, default=0.6, help='Temperature')
    parser.add_argument('--top-p', type=float, default=0.9, help='Top-P')
    parser.add_argument('--device', type=str, default='cuda', help='Target device type')
    parser.add_argument('--dtype', type=str, default='auto', choices=['auto', 'bf16', 'fp16', 'fp32'], help='By default the checkpoint/config dtype will be used.')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--batch-size', type=int, default=1)
    parser.add_argument('--use-kv-cache', action='store_true')
    parser.add_argument('--use-torch-compile', action='store_true', help='Use torch compile')
    parser.add_argument('--full-seq', action='store_true', help='Return full sequence including the prompt')
    parser.add_argument('--instruct', action='store_true', help='Include the instruct control tokens in the prompt. Should not be set when testing base model.')

    parser.add_argument('--output-file-name', type=str, default=None)
    parser.add_argument('--output-dir', type=str, default='outputs/generations')

    args = parser.parse_args()

    if args.max_gen_len <= 0:
        parser.error('--max-gen-len must be > 0.')
    if args.temperature < 0:
        parser.error('--temperature must be >= 0.')
    if not (0.0 < args.top_p <= 1.0):
        parser.error('--top-p must be between 0.0 and 1.0.')
    if args.batch_size <= 0:
        parser.error('--batch-size must be > 0.')

    validate_file_path(args.checkpoint, parser)
    validate_file_path(args.prompts, parser)

    checkpoint_data = load_checkpoint_for_inference(args.checkpoint)
    prompts = validate_prompts(load_json_file(args.prompts), parser)

    if args.batch_size > checkpoint_data.config.model.max_batch_size:
        parser.error(f'--batch-size cannot exceed model.max_batch_size ')

    set_seed(args.seed)

    output_path, generation_name, timestamp = build_output_path(
        config=checkpoint_data.config,
        output_file_name=args.output_file_name,
        output_dir=args.output_dir
    )

    inference_runtime = prepare_runtime_for_inference(
        checkpoint_data=checkpoint_data,
        dtype=args.dtype,
        device=args.device,
        use_torch_compile=args.use_torch_compile
    )

    with torch.inference_mode():
        outputs = generate_and_decode(
            texts=prompts,
            model=inference_runtime.model,
            tokenizer=inference_runtime.tokenizer,
            max_gen_len=args.max_gen_len,
            temperature=args.temperature,
            top_p=args.top_p,
            repetition_penalty=1.0,
            no_repeat_ngram_size=1,
            full_seq=args.full_seq,
            device=inference_runtime.device,
            dtype=inference_runtime.dtype,
            is_instruct=args.instruct,
            skip_encoding=False,
            use_kv_cache=args.use_kv_cache,
            batch_size=args.batch_size
        )

    results = []
    for prompt, output in zip(prompts, outputs):
        results.append({
            'prompt': prompt,
            'output': output,
        })

    data = {
        'name': generation_name,
        'created_at_utc': timestamp.isoformat(),
        'checkpoint': args.checkpoint,
        'prompts': args.prompts,
        'config': {
            'max_gen_len': args.max_gen_len,
            'temperature': args.temperature,
            'top_p': args.top_p,
            'device': args.device,
            'dtype': args.dtype,
            'seed': args.seed,
            'batch_size': args.batch_size,
            'use_kv_cache': args.use_kv_cache,
            'use_torch_compile': args.use_torch_compile,
            'full_seq': args.full_seq,
            'instruct': args.instruct,
        },
        'generations': results,
    }

    logger.info(data, is_json=True)

    write_outputs(output_path, data)
    logger.info(f'Generation outputs saved to: {output_path}')
