import argparse

from logger import logger
from engine.checkpoints import (
    load_checkpoint_for_inference,
    load_shallow_hf_checkpoint_for_inference
)
from utils import (
    load_json_file,
    set_seed,
    build_output_path_for_run,
    write_outputs
)
from inference.runtime import prepare_runtime_for_inference
from inference.generation import generate_and_decode
from cli.common import (
    validate_file_path,
    validate_input_prompts_list,
    add_generation_args,
    validate_generation_args,
    add_runtime_args,
    validate_runtime_args,
    add_output_args
)


if __name__ == '__main__':
    logger.set_master(True)

    parser = argparse.ArgumentParser(description='Text Generation Script Options')

    checkpoint_group = parser.add_mutually_exclusive_group(required=True)
    checkpoint_group.add_argument('--checkpoint', type=str, help='Checkpoint file path to load.')
    checkpoint_group.add_argument('--hf-checkpoint', type=str, help='Hugging Face model id or checkpoint path to load.')

    parser.add_argument('--prompts', type=str, required=True, help='Path to the prompts file.')

    add_generation_args(parser)
    add_runtime_args(parser)
    add_output_args(parser, default_dir='outputs/generations')

    args = parser.parse_args()

    validate_generation_args(args, parser)
    validate_runtime_args(args, parser)

    if args.checkpoint:
        checkpoint = args.checkpoint
        validate_file_path(checkpoint, parser)
        checkpoint_data = load_checkpoint_for_inference(checkpoint)
    elif args.hf_checkpoint:
        checkpoint = args.hf_checkpoint
        checkpoint_data = load_shallow_hf_checkpoint_for_inference(checkpoint)

    validate_file_path(args.prompts, parser)
    prompts = validate_input_prompts_list(load_json_file(args.prompts), parser)

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

    outputs = generate_and_decode(
        prompts=prompts,
        model=inference_runtime.model,
        tokenizer=inference_runtime.tokenizer,
        max_gen_len=args.max_gen_len,
        temperature=args.temperature,
        top_p=args.top_p,
        repetition_penalty=args.repetition_penalty,
        no_repeat_ngram_size=args.no_repeat_ngram_size,
        full_seq=args.full_seq,
        device=inference_runtime.device,
        dtype=inference_runtime.dtype,
        is_instruct=args.instruct,
        use_kv_cache=args.use_kv_cache,
        batch_size=args.batch_size,
        show_progress=True,
        progress_bar_label='Generating...'
    )

    results = []
    for output in outputs:
        results.append({
            'prompt': output['prompt'],
            'prepared_prompt': output['prepared_prompt'],
            'output': output['result_decoded'],
            'metadata': output['metadata']
        })

    data = {
        'name': name,
        'created_at_utc': timestamp.isoformat(),
        'checkpoint': checkpoint,
        'prompts': args.prompts,
        'config': {
            'max_gen_len': args.max_gen_len,
            'temperature': args.temperature,
            'top_p': args.top_p,
            'repetition_penalty': args.repetition_penalty,
            'no_repeat_ngram_size': args.no_repeat_ngram_size,
            'device': args.device,
            'dtype': args.dtype,
            'resolved_device': str(inference_runtime.device),
            'resolved_dtype': str(inference_runtime.dtype),
            'seed': args.seed,
            'batch_size': args.batch_size,
            'use_kv_cache': args.use_kv_cache,
            'use_torch_compile': args.use_torch_compile,
            'full_seq': args.full_seq,
            'instruct': args.instruct,
        },
        'generations': results,
    }

    logger.info({
        'name': name,
        'created_at_utc': timestamp.isoformat(),
        'checkpoint': checkpoint,
        'prompts': args.prompts,
        'num_prompts': len(prompts),
        'output_path': str(output_path),
        'config': data['config'],
    }, is_json=True)

    write_outputs(output_path, data)
    logger.info(f'Generation outputs saved to: {output_path}')
