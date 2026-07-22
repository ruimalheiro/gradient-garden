import os
import numpy as np
import time
import copy

from tokenization.tokenizer import init_tokenizer
from datasets import (
    load_dataset,
    interleave_datasets
)
from datasets_preparation.data_preparation_utils import (
    make_source_key,
    assert_common_structure_and_extract,
    shard_and_tokenize
)
from datasets_preparation.default_mixes import DEFAULT_PRETRAINING_MIX
from logger import logger


os.environ.setdefault('TOKENIZERS_PARALLELISM', 'false') # HF to not use parallelism in tokenizer

#### ADAPTERS
def common_adapter(batch, transforms):
    return {'text': batch['text']}

def structured_wikipedia_adapter(batch, transforms):
    texts = []
    for name, description, abstract in zip(batch['name'], batch['description'], batch['abstract']):
        text = '\n\n'.join([x.strip() for x in [name, description, abstract] if x and x.strip()])
        texts.append(text)
    return {'text': texts}

#### SUPPORTED DATASETS
def hf_dataset(*, split='train', adapter=common_adapter):
    return {
        'split': split,
        'adapter': adapter
    }

SUPPORTED_HF_DATASETS = {
    'HuggingFaceFW/fineweb-edu': {
        'sample-10BT': hf_dataset(),
        'sample-100BT': hf_dataset()
    },
    'HuggingFaceTB/smollm-corpus': {
        'fineweb-edu-dedup': hf_dataset(),
        'cosmopedia-v2': hf_dataset(),
    },
    'Avelina/python-edu-cleaned': {
        'default': hf_dataset(),
    },
    'HuggingFaceFW/dclm_100BT': {
        'default': hf_dataset(),
    },
    'HuggingFaceFW/dclm_100BT-shuffled': {
        'default': hf_dataset(),
    },
    'HuggingFaceTB/finemath': {
        'finemath-4plus': hf_dataset(),
        'finemath-3plus': hf_dataset(),
        'infiwebmath-4plus': hf_dataset(),
        'infiwebmath-3plus': hf_dataset()
    },
    'open-web-math/open-web-math': {
        'default': hf_dataset(),
    },
    'wikimedia/wikipedia': {
        '20231101.en': hf_dataset()
    },
    'wikimedia/structured-wikipedia': {
        'enwiki_namespace_0': hf_dataset(adapter=structured_wikipedia_adapter)
    },
    'common-pile/stackexchange': {
        'default': hf_dataset()
    },
    'common-pile/project_gutenberg_filtered': {
        'default': hf_dataset()
    },
    'karpathy/climbmix-400b-shuffle': {
        'default': hf_dataset()
    },
    'HuggingFaceFW/finewiki': {
        'en': hf_dataset()
    },
}

def download_and_prepare_data(
    *,
    config,
    seed,
    valid_datasets,
    probabilities,
    interleave_stopping_strategy
):
    prepared_datasets = []
    for dataset in valid_datasets:
        ds_id = dataset['id']
        name = dataset.get('name', None)

        dataset_config = SUPPORTED_HF_DATASETS[ds_id][name]
        split = dataset_config['split']
        adapter = dataset_config['adapter']

        transforms = dataset.get('transforms', {})

        max_datapoints = transforms.get('max_datapoints', None)

        hf_name = None if name == 'default' else name
        source_key = make_source_key(ds_id, name)

        ds = load_dataset(
            ds_id,
            name=hf_name,
            split=split,
            streaming=True,
            token=config.third_party.hf_token
        )

        columns_to_remove = ds.column_names

        if max_datapoints is not None:
            max_datapoints = int(max_datapoints)
            assert max_datapoints > 0
            ds = ds.take(max_datapoints)

        def normalize(
            batch,
            *,
            adapter=adapter,
            transforms=transforms,
            source_key=source_key
        ):
            batch = adapter(batch, transforms)
            texts = batch['text']

            return {
                'text': texts,
                'source': [source_key] * len(texts)
            }

        ds = ds.map(
            normalize,
            batched=True,
            batch_size=config.data_preparation.hf_map_batch_size,
            remove_columns=columns_to_remove
        )

        prepared_datasets.append(ds)

    if len(prepared_datasets) > 1:
        logger.info(f'Preparing Interleaving iterator... This operation can take a few minutes... Using strategy: {interleave_stopping_strategy}')
        prepared_dataset = interleave_datasets(
            prepared_datasets,
            probabilities=probabilities,
            seed=seed,
            stopping_strategy=interleave_stopping_strategy
        )
        time.sleep(2) # Workaround for occasional streaming/interleave iterator shutdown issue.
        logger.info('Interleaving datasets complete')
    else:
        prepared_dataset = prepared_datasets[0]

    return prepared_dataset

tokenizer = None
def tokenize(tokenizer_kwargs, doc):
    global tokenizer
    if tokenizer is None:
        tokenizer = init_tokenizer(**tokenizer_kwargs)
    input_ids = tokenizer.encode(doc['text'])
    tokens_np = np.empty(len(input_ids) + 1, dtype=np.uint32)
    tokens_np[:-1] = input_ids
    tokens_np[-1] = tokenizer.eos_id
    return tokens_np

def prepare_pretraining_dataset(
    *,
    config,
    datasets_mix,
    num_proc
):
    datasets_mix = copy.deepcopy(datasets_mix) if datasets_mix else copy.deepcopy(DEFAULT_PRETRAINING_MIX)

    assert 'datasets_common_settings' in datasets_mix
    assert 'shard_size' in datasets_mix['datasets_common_settings']
    shard_size = datasets_mix['datasets_common_settings']['shard_size']
    assert isinstance(shard_size, int)

    #### VERIFY MIX FILE STRUCTURE
    seed, common_settings, valid_datasets, probabilities = assert_common_structure_and_extract(datasets_mix, SUPPORTED_HF_DATASETS)

    target_tokens = common_settings.get('target_tokens')
    if target_tokens is not None:
        target_tokens = int(target_tokens)

    validation_ratio = float(common_settings.get('validation_ratio', 0.01))

    prepared_dataset = download_and_prepare_data(
        config=config,
        seed=seed,
        valid_datasets=valid_datasets,
        probabilities=probabilities,
        interleave_stopping_strategy=common_settings['interleave_stopping_strategy']
    )

    tokenizer_kwargs = {
        'path': config.tokenizer.checkpoint_path,
        'system_prompt': config.prompts.system_prompt,
        'is_huggingface_tokenizer': config.tokenizer.huggingface_tokenizer,
        'hf_token': config.third_party.hf_token if config.tokenizer.huggingface_tokenizer else None
    }

    shard_and_tokenize(
        seed=seed,
        dataset=prepared_dataset,
        tokenize_function=tokenize,
        tokenizer_kwargs=tokenizer_kwargs,
        train_path=os.path.join(config.paths.datasets.training_path, 'train'),
        val_path=os.path.join(config.paths.datasets.training_path, 'val'),
        shard_file_prefix='data',
        shard_size=shard_size,
        target_tokens=target_tokens,
        validation_ratio=validation_ratio,
        num_proc=num_proc,
        chunksize=config.data_preparation.mp_pool_chunk_size
    )
