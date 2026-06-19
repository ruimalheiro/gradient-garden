import random

from typing import Protocol
from pathlib import Path
from utils import save_jsonl_file
from config import GlobalConfig
from logger import logger
from datasets_preparation.synthetic.group_utils import choose_weighted_group


def make_fixture_dataset_generator(
    *,
    fixtures,
    rng,
    render_example,
    transforms=None,
    default_weights=None,
    variables=None,
    prompt_transforms=None,
    answer_selector=None,
    answer_transform=None,
    override_group_answer=None,
):
    variables = variables or {}
    override_group_answer = override_group_answer or {}

    default_weights = (
        default_weights
        if default_weights is not None
        else {group_name: 1.0 for group_name in fixtures.keys()}
    )

    def generate_example():
        group_name = choose_weighted_group(
            rng=rng,
            groups=default_weights,
            transforms=transforms or {},
        )

        return render_example(
            fixtures,
            group_name,
            rng=rng,
            variables=dict(variables),
            prompt_transforms=prompt_transforms,
            answer_selector=answer_selector,
            answer_transform=answer_transform,
            override_group_answer=override_group_answer,
        )

    return generate_example

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
