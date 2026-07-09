import torch
import textwrap

from engine.checkpoints import (
    load_checkpoint_for_inference,
    load_shallow_hf_checkpoint_for_inference
)
from inference.runtime import prepare_runtime_for_inference
from inference.generation import generate_and_decode
from logger import logger


class CheckpointInspector:
    def __init__(
        self,
        *,
        checkpoint_path=None,
        hf_checkpoint_path=None,
        dtype=None,
        device=None,
        use_torch_compile=False,
        text_width=160,
        hf_token=None
    ):
        logger.set_master(True)

        if checkpoint_path is not None and hf_checkpoint_path is not None:
            raise ValueError('"checkpoint_path" and "hf_checkpoint_path" are mutually exclusive.')

        self.checkpoint_path = checkpoint_path
        self.use_torch_compile = use_torch_compile

        if checkpoint_path is not None:
            checkpoint_data = load_checkpoint_for_inference(self.checkpoint_path)
        elif hf_checkpoint_path is not None:
            checkpoint_data = load_shallow_hf_checkpoint_for_inference(hf_checkpoint_path=hf_checkpoint_path)
            checkpoint_data.config.third_party.hf_token=hf_token
        else:
            raise ValueError('"checkpoint_path" or "hf_checkpoint_path" must be set.')

        self.checkpoint_data = checkpoint_data
        self.config = checkpoint_data.config

        self.inference_runtime = prepare_runtime_for_inference(
            checkpoint_data=checkpoint_data,
            dtype=dtype if dtype is not None else checkpoint_data.config.runtime.training_precision.value,
            device=device if device is not None else checkpoint_data.config.runtime.device_type.value,
            use_torch_compile=self.use_torch_compile
        )

        self.model = self.inference_runtime.model
        self.tokenizer = self.inference_runtime.tokenizer
        self.device = self.inference_runtime.device
        self.device_type = self.device.type if isinstance(self.device, torch.device) else str(self.device).split(':')[0]
        self.dtype = self.inference_runtime.dtype
        self.autocast_enabled = (self.dtype != torch.float32)
        self.text_width = text_width

    def generate(
        self,
        prompts,
        *,
        max_gen_len=128,
        temperature=0.0,
        top_p=1.0,
        repetition_penalty=None,
        no_repeat_ngram_size=None,
        full_seq=False,
        instruct=False,
        use_kv_cache=False,
        batch_size=1,
        skip_encoding=False,
        print_text=True,
        prompts_are_messages=False
    ):
        with torch.autocast(
            device_type=self.device_type,
            dtype=self.dtype,
            enabled=self.autocast_enabled
        ):
            outputs = generate_and_decode(
                prompts=prompts,
                model=self.model,
                tokenizer=self.tokenizer,
                max_gen_len=max_gen_len,
                temperature=temperature,
                top_p=top_p,
                repetition_penalty=repetition_penalty,
                no_repeat_ngram_size=no_repeat_ngram_size,
                full_seq=full_seq,
                device=self.device,
                dtype=self.dtype,
                is_instruct=instruct,
                use_kv_cache=use_kv_cache,
                batch_size=batch_size,
                skip_encoding=skip_encoding,
                prompts_are_messages=prompts_are_messages
            )

        results = [
            textwrap.fill(output['result_decoded'], self.text_width)
            for output in outputs
        ]

        if print_text:
            for result in results:
                logger.info(result)
            return None

        return results
