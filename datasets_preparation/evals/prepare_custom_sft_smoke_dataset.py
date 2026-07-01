import json

from pathlib import Path
from tqdm.auto import tqdm
from datasets_preparation.synthetic.instruct.fixtures.evals.custom_sft_smoke import CUSTOM_SFT_SMOKE_EVAL
from logger import logger


def prepare_custom_sft_smoke_dataset(*, config, num_proc):
    current_dir = Path(__file__).resolve().parent.parent.parent

    data_cache_dir = current_dir / config.paths.evals.custom_sft_smoke_path
    data_cache_dir.mkdir(parents=True, exist_ok=True)
    data_filename = data_cache_dir / config.paths.evals.data_filename

    if not data_filename.exists():
        with open(data_filename, 'w', encoding='utf-8') as file:
            for example in tqdm(CUSTOM_SFT_SMOKE_EVAL, desc='Preparing custom SFT smoke eval dataset'):
                json.dump(example, file, ensure_ascii=False)
                file.write('\n')
        logger.info(f'Custom SFT smoke eval preprocessing completed and stored at: {data_filename}')
    else:
        logger.info(f'Custom SFT smoke eval preprocessed file already exists: {data_filename}')
