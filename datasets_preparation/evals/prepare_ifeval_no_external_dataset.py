import re
import json

from pathlib import Path
from tqdm.auto import tqdm
from datasets import load_dataset
from evals.ifeval.checkers import CHECKERS
from logger import logger


def prepare_ifeval_no_external_dataset(*, config, num_proc):
    current_dir = Path(__file__).resolve().parent.parent.parent

    data_cache_dir = current_dir / config.paths.evals.ifeval_no_external_path
    data_cache_dir.mkdir(parents=True, exist_ok=True)
    data_filename = data_cache_dir / config.paths.evals.data_filename

    if not data_filename.exists():
        ds = load_dataset(
            'google/IFEval',
            split='train',
            num_proc=num_proc,
            token=config.third_party.hf_token
        )

        EXTERNAL_PROMPT_PATTERNS = [
            r'https?://',
            r'www\.',
            r'wikipedia',
            r'wiki page',
            r'webpage',
            r'web page',
            r'this article',
            r'the article',
            r'this page',
            r'the page',
            r'this link',
            r'the link',
            r'above article',
            r'above page',
            r'above link',
        ]

        def has_no_external_dependency(example: dict) -> bool:
            prompt = example['prompt']
            return not any(
                re.search(pattern, prompt, flags=re.IGNORECASE)
                for pattern in EXTERNAL_PROMPT_PATTERNS
            )

        def only_supported_checkers(example: dict) -> bool:
            return all(
                instruction_id in CHECKERS
                for instruction_id in example['instruction_id_list']
            )

        ds = ds.filter(has_no_external_dependency, num_proc=num_proc)
        ds = ds.filter(only_supported_checkers, num_proc=num_proc)

        ds.to_json(data_filename, lines=True, force_ascii=False)
        logger.info(f'IFEval (no external knowledge) preprocessing completed and stored at: {data_filename}')
    else:
        logger.info(f'IFEval (no external knowledge) preprocessed file already exists: {data_filename}')
