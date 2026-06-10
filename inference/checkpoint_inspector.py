import torch
import textwrap

from engine.checkpoints import load_checkpoint_for_inference
from inference.runtime import prepare_runtime_for_inference
from inference.generation import generate_and_decode
from logger import logger


class CheckpointInspector:
    def __init__(self, *, checkpoint_path, dtype=None, device=None, use_torch_compile=False, text_width=160):
        logger.set_master(True)

        self.checkpoint_path = checkpoint_path
        self.use_torch_compile = use_torch_compile
        self.checkpoint_data = load_checkpoint_for_inference(self.checkpoint_path)
        self.config = self.checkpoint_data.config
        self.inference_runtime = prepare_runtime_for_inference(
            checkpoint_data=self.checkpoint_data,
            dtype=dtype if dtype is not None else self.config.runtime.training_precision.value,
            device=device if device is not None else self.config.runtime.device_type.value,
            use_torch_compile=self.use_torch_compile
        )
        self.model = self.inference_runtime.model
        self.tokenizer = self.inference_runtime.tokenizer
        self.device = self.inference_runtime.device
        self.dtype = self.inference_runtime.dtype
        self.autocast_enabled = (self.dtype != torch.float32)
        self.text_width = text_width

    def generate(
        self,
        prompts,
        *,
        max_gen_len=256,
        temperature=0.0,
        top_p=1.0,
        repetition_penalty=1.0,
        no_repeat_ngram_size=1,
        full_seq=False,
        instruct=False,
        use_kv_cache=True,
        batch_size=2,
        print_text=True
    ):
        with torch.autocast(
            device_type=self.device,
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
                batch_size=batch_size
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
