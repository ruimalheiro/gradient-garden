import json
import torch

from pathlib import Path
from tqdm.auto import tqdm
from tokenization.tokenizer import init_tokenizer
from datasets import load_dataset
from logger import logger


def prepare_winogrande_dataset(*, config, num_proc):
    current_dir = Path(__file__).resolve().parent.parent.parent

    data_cache_dir = current_dir / config.paths.evals.winogrande_path
    data_cache_dir.mkdir(parents=True, exist_ok=True)
    data_filename = data_cache_dir / config.paths.evals.data_filename

    tokenizer = init_tokenizer(
        path=config.tokenizer.checkpoint_path,
        system_prompt=config.prompts.system_prompt,
        is_huggingface_tokenizer=config.tokenizer.huggingface_tokenizer,
        hf_token=config.third_party.hf_token if config.tokenizer.huggingface_tokenizer else None
    )

    def prepare_example(example):
        """
        Sample example:
        {
            "sentence": "Only the bag got melted and not the wood when they were inside the flame. The _ is soft.",
            "option1": "wood",
            "option2": "bag",
            "answer": "2",
        }

        """
        sentence = example['sentence']
        options = [example['option1'].strip(), example['option2'].strip()]
        num_choices = len(options)
        label_index = int(example['answer']) - 1

        if sentence.count('_') != 1:
            raise ValueError(f'Expected exactly one blank in sentence, got: {sentence}')
        prefix, suffix = sentence.split('_', 1)
        prefix_tokens = tokenizer.encode(prefix)

        tokens_rows = []
        mask_rows = []
        for option in options:
            candidate_text = prefix + option + suffix
            candidate_tokens = tokenizer.encode(candidate_text)

            mask_row = torch.cat([
                torch.zeros(len(prefix_tokens), dtype=torch.long),
                torch.ones(len(candidate_tokens) - len(prefix_tokens), dtype=torch.long)
            ])

            tokens_rows.append(candidate_tokens)
            mask_rows.append(mask_row)

        max_len = max(len(row) for row in tokens_rows)

        tokens = torch.zeros((num_choices, max_len), dtype=torch.long)
        mask = torch.zeros((num_choices, max_len), dtype=torch.long)
        for i, (tokens_row, mask_row) in enumerate(zip(tokens_rows, mask_rows)):
            tokens[i, :len(tokens_row)] = torch.tensor(tokens_row, dtype=torch.long)
            mask[i, :len(mask_row)] = mask_row

        processed_example = {
            'tokens': tokens.tolist(),
            'mask': mask.tolist(),
            'label_index': label_index
        }

        return processed_example

    if not data_filename.exists():
        ds = load_dataset(
            'allenai/winogrande',
            name='winogrande_debiased',
            split='validation',
            num_proc=num_proc,
            token=config.third_party.hf_token
        )

        with open(data_filename, 'w', encoding='utf-8') as file:
            for example in tqdm(ds, desc='Preparing WinoGrande eval dataset'):
                processed_example = prepare_example(example)
                json.dump(processed_example, file, ensure_ascii=False)
                file.write('\n')
        logger.info(f'WinoGrande preprocessing completed and stored at: {data_filename}')
    else:
        logger.info(f'WinoGrande preprocessed file already exists: {data_filename}')
