import random

from typing import Protocol
from pathlib import Path
from utils import save_jsonl_file
from config import GlobalConfig
from logger import logger


class GeneratorFn(Protocol):
    def __call__(
        self,
        config: GlobalConfig,
        rng: random.Random,
        count: int,
        transforms: dict
    ) -> list: ...

def generate_dataset(
    *,
    config: GlobalConfig,
    ds_id: str,
    seed: int,
    count: int,
    transforms: dict,
    label: str,
    file_name: str,
    generator_fn: GeneratorFn
):
    current_dir = Path(__file__).resolve().parent.parent.parent

    target_dir = current_dir / ds_id
    target_dir.mkdir(parents=True, exist_ok=True)
    data_filename = target_dir / f'{file_name}.jsonl'

    if data_filename.exists():
        logger.warning(f'Dataset raw source already exists: {data_filename} \nDelete this file manually to regenerate it.')
        return

    rng = random.Random(seed)

    transforms = transforms or {}
    custom_example_count = transforms.get('count', None)
    count = custom_example_count if custom_example_count is not None else count

    logger.info(f'Generating synthetic {label} dataset with a total of {count} examples...')

    examples = generator_fn(
        config=config,
        rng=rng,
        count=count,
        transforms=transforms
    )

    rng.shuffle(examples)

    save_jsonl_file(data_filename, examples)
    logger.info(f'Dataset prepared and stored at: {data_filename}')
