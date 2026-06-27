import os
import numpy as np
import re
import copy
import time

from functools import partial
from tokenization.tokenizer import init_tokenizer
from datasets import (
    load_dataset,
    interleave_datasets
)
from datasets_preparation.data_preparation_utils import (
    assert_common_structure_and_extract,
    make_source_key
)
from datasets_preparation.default_mixes import DEFAULT_DPO_MIX
from logger import logger


#### ADAPTERS
def adapt_anthropic_hh_rlhf(doc, transforms):
    def extract_interactions(text):
        conversation = []
        assistant_statements = []

        role_re = re.compile(
            r'(?:^|\n\n)(Human|Assistant): (.*?)(?=\n\n(?:Human|Assistant): |\Z)',
            re.DOTALL,
        )

        for role, content in role_re.findall(text):
            role = 'user' if role.lower() == 'human' else 'assistant'

            conversation.append({
                'role': role,
                'content': content
            })

            if role == 'assistant':
                assistant_statements.append(content)

        return conversation, assistant_statements

    chosen_conversation, chosen_assistant = extract_interactions(doc['chosen'])
    _, rejected_assistant = extract_interactions(doc['rejected'])

    prompt = chosen_conversation[:-1]

    return {'prompt': prompt, 'chosen': chosen_assistant[-1], 'rejected': rejected_assistant[-1] }

#### SUPPORTED DATASETS
SUPPORTED_HF_DATASETS = {
    'Anthropic/hh-rlhf': {
        'default': {
            'split': 'train',
            'adapter': adapt_anthropic_hh_rlhf
        }
    }
}

def remove_system_messages(conversation):
    return [
        message for message in conversation
        if message['role'] != 'system'
    ]

def ensure_only_user_assistant(conversation):
    allowed_roles = {'user', 'assistant'}

    if not conversation:
        return []

    for message in conversation:
        if message['role'] not in allowed_roles:
            return []

    return conversation

def ensure_user_first(conversation):
    if not conversation:
        return []
    if conversation[0]['role'] != 'user':
        return []
    return conversation

def ensure_user_last(conversation):
    if not conversation:
        return []
    if conversation[-1]['role'] != 'user':
        return []
    return conversation

def ensure_alternating_prompt_for_dpo(conversation):
    """
    DPO prompt should be:
      user, assistant, user, assistant, ..., user

    chosen/rejected are the final assistant replies.
    """
    if not conversation:
        return []

    for idx, message in enumerate(conversation):
        expected_role = 'user' if idx % 2 == 0 else 'assistant'
        if message['role'] != expected_role:
            return []

    if conversation[-1]['role'] != 'user':
        return []

    return conversation

tokenizer = None

def tokenize(tokenizer_kwargs, ignore_index, max_seq_len, doc):
    global tokenizer
    if tokenizer is None:
        tokenizer = init_tokenizer(**tokenizer_kwargs)

    (
        prompt_input_ids,
        chosen_input_ids,
        chosen_labels,
        rejected_input_ids,
        rejected_labels
    ) = tokenizer.encode_instruct_chat_dpo(
        conversation=doc['prompt'],
        chosen=doc['chosen'],
        rejected=doc['rejected'],
        ignore_index=ignore_index,
        max_seq_len=max_seq_len,
        trim_to_context=True
    )

    return {
        'prompt_input_ids': np.array(prompt_input_ids, dtype=np.uint32),
        'chosen_input_ids': np.array(chosen_input_ids, dtype=np.uint32),
        'chosen_labels': np.array(chosen_labels, dtype=np.int64),
        'rejected_input_ids': np.array(rejected_input_ids, dtype=np.uint32),
        'rejected_labels': np.array(rejected_labels, dtype=np.int64),
    }

def download_and_prepare_data(
    *,
    config,
    seed,
    valid_datasets,
    probabilities,
    num_proc,
    validation_ratio,
    interleave_stopping_strategy
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
            data = adapter(doc, transforms)

            prompt = data['prompt']
            prompt = remove_system_messages(prompt)
            prompt = ensure_only_user_assistant(prompt)
            prompt = ensure_user_first(prompt)
            prompt = ensure_user_last(prompt)
            prompt = ensure_alternating_prompt_for_dpo(prompt)

            data['prompt'] = prompt
            data['chosen'] = data['chosen'].strip()
            data['rejected'] = data['rejected'].strip()
            data['source'] = source_key

            return data

        ds = ds.map(normalize, num_proc=num_proc)
        ds = ds.filter(
            lambda x: (
                len(x['prompt']) > 0 and
                len(x['chosen']) > 0 and
                len(x['rejected']) > 0
            ),
            num_proc=num_proc
        )

        columns_to_remove = [c for c in ds.column_names if c not in ['source']]
        tokenized_ds = ds.map(
            partial(
                tokenize,
                tokenizer_kwargs,
                config.tokenizer.ignore_index,
                config.model.max_seq_len
            ),
            num_proc=num_proc,
            remove_columns=columns_to_remove
        )

        def is_valid_tokenized_dpo(example):
            ignore_index = config.tokenizer.ignore_index
            max_seq_len = config.model.max_seq_len

            return (
                len(example['prompt_input_ids']) > 0 and
                len(example['chosen_input_ids']) > 0 and
                len(example['rejected_input_ids']) > 0 and

                len(example['chosen_input_ids']) == len(example['chosen_labels']) and
                len(example['rejected_input_ids']) == len(example['rejected_labels']) and

                len(example['prompt_input_ids']) <= max_seq_len and
                len(example['chosen_input_ids']) <= max_seq_len and
                len(example['rejected_input_ids']) <= max_seq_len and

                any(label != ignore_index for label in example['chosen_labels']) and
                any(label != ignore_index for label in example['rejected_labels'])
            )

        tokenized_ds = tokenized_ds.filter(
            is_valid_tokenized_dpo,
            num_proc=num_proc,
        )

        prepared_datasets.append(tokenized_ds)

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

    logger.info('Summary:')
    for d, ds in zip(valid_datasets, prepared_datasets):
        logger.info(f'- Total for: {d["id"]} : {len(ds)}')

    logger.info('- Mix total len:', len(prepared_dataset))

    splits = prepared_dataset.train_test_split(test_size=validation_ratio, seed=seed)

    logger.info(f'- Train len: {len(splits["train"])} Val len: {len(splits["test"])}\n')

    splits['train'].save_to_disk(os.path.join(config.paths.datasets.dpo_path, 'train'))
    splits['test'] .save_to_disk(os.path.join(config.paths.datasets.dpo_path, 'val'))


def prepare_dpo_dataset(
    *,
    config,
    datasets_mix,
    num_proc
):
    datasets_mix = copy.deepcopy(datasets_mix) if datasets_mix else copy.deepcopy(DEFAULT_DPO_MIX)

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
        validation_ratio=validation_ratio,
        interleave_stopping_strategy=common_settings['interleave_stopping_strategy']
    )
