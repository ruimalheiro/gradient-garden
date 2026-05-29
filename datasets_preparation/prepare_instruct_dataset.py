import os
import numpy as np
import re
import random
import copy
import time

from functools import partial
from tokenization.tokenizer import init_tokenizer
from datasets import (
    load_dataset,
    interleave_datasets
)
from datasets_preparation.data_preparation_utils import (
    stable_hash,
    assert_common_structure_and_extract,
    make_source_key
)
from datasets_preparation.default_mixes import DEFAULT_INSTRUCT_MIX
from logger import logger


#### ADAPTERS
def adapt_ultrachat_200k(doc, transforms, seed):
    messages = doc['messages']
    conversation = []
    for message in messages:
        conversation.append({'role': message['role'], 'content': message['content']})
    return conversation

def adapt_lmsys_chat_1m(doc, transforms, seed):
    messages = doc['conversation']
    replace = False
    name_mapping = None

    if transforms.get('placeholders') and transforms['placeholders'].get('replace', False):
        # The replacements in the config file are a suggestion of more neutral names.
        replace = True
        assert 'random_options' in transforms['placeholders']
        assert len(transforms['placeholders']['random_options']) > 0, 'List of replacements("random_options") cannot be empty'
        replacements = transforms['placeholders']['random_options']

        full_conversation = ' '.join(message['content'] for message in messages)
        name_ids = sorted(set(re.compile(r'\bNAME_(\d+)\b').findall(full_conversation)))

        # Local random generator because of the multi processing
        local_rng = random.Random(seed ^ stable_hash(full_conversation))

        # Selected names. + 1 here because when len(name_ids) < len(replacements)
        name_pool = (replacements * ((len(name_ids) // len(replacements)) + 1))[:len(name_ids)]

        local_rng.shuffle(name_pool)

        # mapping 1 (NAME_1) -> Sam
        name_mapping = {f'NAME_{name_id}': name for name_id, name in zip(name_ids, name_pool)}

    conversation = []
    for message in messages:
        content = message['content']
        if replace:
            for name_id, name in name_mapping.items():
                content = content.replace(name_id, name)
        conversation.append({'role': message['role'], 'content': content})
    return conversation

#### SUPPORTED DATASETS
SUPPORTED_HF_DATASETS = {
    'HuggingFaceH4/ultrachat_200k': {
        'default': {
            'id': 'HuggingFaceH4/ultrachat_200k',
            'split': 'train_sft',
            'adapter': adapt_ultrachat_200k
        }
    },
    'lmsys/lmsys-chat-1m': {
        'default': {
            'id': 'lmsys/lmsys-chat-1m',
            'split': 'train',
            'adapter': adapt_lmsys_chat_1m
        }
    }
}

def ensure_user_first(conversation):
    if not conversation:
        return conversation
    if conversation[0]['role'] != 'user':
        # add default empty user conversation if it is missing (If it starts with assistant)
        return [{'role': 'user', 'content': ''}] + conversation
    return conversation

def trim_to_last_assistant(conversation):
    for i in range(len(conversation) - 1, -1, -1):
        if (
            conversation[i]['role'] == 'assistant' and
            conversation[i]['content'].strip()
        ):
            return conversation[:i + 1]
    return []

tokenizer = None

def tokenize(tokenizer_kwargs, ignore_index, doc):
    global tokenizer
    if tokenizer is None:
        tokenizer = init_tokenizer(**tokenizer_kwargs)

    tokens, labels = tokenizer.encode_instruct_chat(
        conversation=doc['conversation'],
        ignore_index=ignore_index
    )

    return {
        'input_ids': np.array(tokens, dtype=np.uint32),
        'labels': np.array(labels, dtype=np.int32)
    }

def download_and_prepare_data(
    *,
    config,
    seed,
    valid_datasets,
    probabilities,
    num_proc,
    validation_ratio
):
    tokenizer_kwargs = {
        'path': config.tokenizer.checkpoint_path,
        'system_prompt': config.prompts.system_prompt,
        'is_huggingface_tokenizer': config.tokenizer.huggingface_tokenizer,
        'hf_token': config.third_party.hf_token if config.tokenizer.huggingface_tokenizer else None
    }

    prepared_datasets = []
    for dataset in valid_datasets:
        ds_id = dataset['id']
        name = dataset.get('name', None)

        dataset_config = SUPPORTED_HF_DATASETS[ds_id][name]
        split = dataset_config['split']
        adapter = dataset_config['adapter']

        transforms = dataset.get('transforms', {})

        max_datapoints = transforms.get('max_datapoints', None)
        max_messages = transforms.get('max_messages', 8)

        hf_name = None if name == 'default' else name
        source_key = make_source_key(ds_id, name)

        ds = load_dataset(
            ds_id,
            name=hf_name,
            split=split,
            num_proc=num_proc,
            token=config.third_party.hf_token
        )

        if max_datapoints is not None:
            max_datapoints = int(max_datapoints)
            ds = ds.select(range(max_datapoints))

        def normalize(doc):
            conversation = adapter(doc, transforms, seed)
            conversation = ensure_user_first(conversation)
            conversation = conversation[:max_messages]
            conversation = trim_to_last_assistant(conversation)

            return {
                'conversation': conversation,
                'source': source_key
            }

        ds = ds.map(normalize, num_proc=num_proc)
        ds = ds.filter(lambda x: len(x['conversation']) > 0, num_proc=num_proc)

        columns_to_remove = [c for c in ds.column_names if c not in ['source']]
        tokenized_ds = ds.map(
            partial(
                tokenize,
                tokenizer_kwargs,
                config.tokenizer.ignore_index
            ),
            num_proc=num_proc,
            remove_columns=columns_to_remove
        )

        def has_supervision(example):
            return any(label != config.tokenizer.ignore_index for label in example['labels'])

        tokenized_ds = tokenized_ds.filter(has_supervision, num_proc=num_proc)

        prepared_datasets.append(tokenized_ds)

    if len(prepared_datasets) > 1:
        logger.info('Preparing Interleaving iterator... This operation can take a few minutes...')
        prepared_dataset = interleave_datasets(
            prepared_datasets,
            probabilities=probabilities,
            seed=seed
        )
        time.sleep(2) # Workaround for occasional streaming/interleave iterator shutdown issue.
        logger.info('Interleaving datasets complete')
    else:
        prepared_dataset = prepared_datasets[0]

    logger.info('Summary:')
    for d, ds in zip(valid_datasets, prepared_datasets):
        logger.info(f'- Total for: {d["id"]} : {len(ds)}')

    logger.info('- Mix total len:', len(prepared_dataset))

    splits = prepared_dataset.train_test_split(test_size=validation_ratio, seed=seed)

    logger.info(f'- Train len: {len(splits["train"])} Val len: {len(splits["test"])}\n')

    splits['train'].save_to_disk(os.path.join(config.paths.datasets.instruct_path, 'train'))
    splits['test'] .save_to_disk(os.path.join(config.paths.datasets.instruct_path, 'val'))

def prepare_instruct_dataset(
    *,
    config,
    datasets_mix,
    num_proc
):
    datasets_mix = copy.deepcopy(datasets_mix) if datasets_mix else copy.deepcopy(DEFAULT_INSTRUCT_MIX)

    #### VERIFY MIX FILE STRUCTURE
    seed, common_settings, valid_datasets, probabilities = assert_common_structure_and_extract(datasets_mix, SUPPORTED_HF_DATASETS)

    if common_settings.get('shard_size') is not None:
        logger.warning('datasets_common_settings.shard_size is only used for pretraining data preparation.')
    if common_settings.get('target_tokens') is not None:
        logger.warning('datasets_common_settings.target_tokens is only used for pretraining data preparation.')

    validation_ratio = float(common_settings.get('validation_ratio', 0.01))

    download_and_prepare_data(
        config=config,
        seed=seed,
        valid_datasets=valid_datasets,
        probabilities=probabilities,
        num_proc=num_proc,
        validation_ratio=validation_ratio
    )
