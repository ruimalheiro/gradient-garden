import argparse

from pathlib import Path
from engine.checkpoints import load_checkpoint_for_inference
from utils import load_json_file
from inference.runtime import prepare_runtime_for_inference
from inference.generation import generate_and_decode


def validate_file_path(path: str, parser: argparse.ArgumentParser):
    file_path = Path(path)
    if not file_path.exists():
        parser.error(f'The path does not exist: {path}')
    if not file_path.is_file():
        parser.error(f'The path does not point to a file: {path}')

if __name__ == '__main__':
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
    parser.add_argument('--use-kv-cache', action='store_true', default=True)
    parser.add_argument('--use-torch-compile', action='store_true', help='Use torch compile', default=True)
    parser.add_argument('--full-seq', action='store_true', help='Return full sequence including the prompt')
    parser.add_argument('--instruct', action='store_true', help='Include the instruct control tokens in the prompt. Should not be set when testing base model.')

    parser.add_argument('--output', type=str, default=None, help='Path to store the output file')

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
    prompts = load_json_file(args.prompts)

    if args.batch_size > checkpoint_data.config.model.max_batch_size:
        parser.error(f'--batch-size cannot exceed model.max_batch_size ')

    inference_runtime = prepare_runtime_for_inference(
        checkpoint_data=checkpoint_data,
        dtype=args.dtype,
        device=args.device,
        use_torch_compile=args.use_torch_compile
    )

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

    for text in outputs:
        print(text)
    # output_file_path=args.output
