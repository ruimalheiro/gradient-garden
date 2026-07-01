import json
import torch

from pathlib import Path
from tqdm.auto import tqdm
from tokenization.tokenizer import init_tokenizer
from datasets import load_dataset
from logger import logger


def prepare_arc_challenge_dataset(*, config, num_proc):
    current_dir = Path(__file__).resolve().parent.parent.parent

    data_cache_dir = current_dir / config.paths.evals.arc_challenge_path
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
            "id": "Mercury_SC_407695",
            "question": "Juan and LaKeisha roll a few objects down a ramp. They want to see which object rolls the farthest. What should they do so they can repeat their investigation?",
            "choices": {
                "text": [
                    "Put the objects in groups.",
                    "Change the height of the ramp.",
                    "Choose different objects to roll.",
                    "Record the details of the investigation.",
                ],
                "label": ["A", "B", "C", "D"],
            },
            "answerKey": "D",
        }
        """
        question = example['question']
        choices_texts = example['choices']['text']
        num_choices = len(choices_texts)
        label_index = example['choices']['label'].index(example['answerKey'])

        prompt = f'Question: {question}\nAnswer: '
        prompt_tokens = tokenizer.encode(prompt)

        tokens_rows = []
        mask_rows = []
        for choice_text in choices_texts:
            candidate_text = prompt + choice_text
            candidate_tokens = tokenizer.encode(candidate_text)

            tokens_rows.append(candidate_tokens)

            mask_row = torch.cat([
                torch.zeros(len(prompt_tokens), dtype=torch.long),
                torch.ones(len(candidate_tokens) - len(prompt_tokens), dtype=torch.long)
            ])

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
            'allenai/ai2_arc',
            name='ARC-Challenge',
            split='validation',
            num_proc=num_proc,
            token=config.third_party.hf_token
        )

        with open(data_filename, 'w', encoding='utf-8') as file:
            for example in tqdm(ds, desc='Preparing ARC-Challenge eval dataset'):
                processed_example = prepare_example(example)
                json.dump(processed_example, file, ensure_ascii=False)
                file.write('\n')
        logger.info(f'ARC-Challenge preprocessing completed and stored at: {data_filename}')
    else:
        logger.info(f'ARC-Challenge preprocessed file already exists: {data_filename}')
