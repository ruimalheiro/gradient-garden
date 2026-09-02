import os
import numpy as np
import re
import copy
import time
import math

from functools import partial
from tokenization.tokenizer import init_tokenizer
from datasets import (
    load_dataset,
    interleave_datasets
)
from datasets_preparation.utils.common import (
    assert_common_structure_and_extract,
    make_source_key,
    token_budget_dataset_mix,
    compute_stats
)
from datasets_preparation.default_mixes import DEFAULT_DPO_MIX
from recipes.config import MixStrategy
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

def adapt_ultrafeedback_binarized(doc, transforms):
    chosen = doc['chosen']
    rejected = doc['rejected']

    if not chosen or not rejected:
        return {'prompt': [], 'chosen': '', 'rejected': ''}

    chosen_prompt = chosen[:-1]
    rejected_prompt = rejected[:-1]

    if chosen_prompt != rejected_prompt:
        return {'prompt': [], 'chosen': '', 'rejected': ''}

    if chosen[-1]['role'] != 'assistant':
        return {'prompt': [], 'chosen': '', 'rejected': ''}

    if rejected[-1]['role'] != 'assistant':
        return {'prompt': [], 'chosen': '', 'rejected': ''}

    return {
        'prompt': chosen_prompt,
        'chosen': chosen[-1]['content'],
        'rejected': rejected[-1]['content']
    }

#### SUPPORTED DATASETS
SUPPORTED_HF_DATASETS = {
    'Anthropic/hh-rlhf': {
        'default': {
            'split': 'train',
            'adapter': adapt_anthropic_hh_rlhf
        }
    },
    'HuggingFaceH4/ultrafeedback_binarized': {
        'default': {
            'split': 'train_prefs',
            'adapter': adapt_ultrafeedback_binarized
        }
    }
}

def extract_leading_system_prompt(conversation):
    system_parts = []
    remaining = []
    seen_non_system = False

    for message in conversation:
        role = message['role']
        content = message['content'].strip()

        if role == 'system':
            if seen_non_system:
                return '', []
            if content:
                system_parts.append(content)
            continue

        seen_non_system = True
        remaining.append(message)

    system_prompt = '\n\n'.join(system_parts)

    return system_prompt or '', remaining

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

def ensure_nonempty_content(conversation):
    for message in conversation:
        content = message.get('content')

        if not isinstance(content, str):
            return []

        if not content.strip():
            return []

    return conversation

tokenizer = None

def tokenize(tokenizer_kwargs, ignore_index, max_seq_len, doc):
    global tokenizer
    if tokenizer is None:
        tokenizer = init_tokenizer(**tokenizer_kwargs)

    source_system_prompt = doc.get('system_prompt', '').strip() or None

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
        system_prompt=source_system_prompt,
        max_seq_len=max_seq_len,
        trim_to_context=True
    )

    total_tokens = len(chosen_input_ids) + len(rejected_input_ids)
    supervised_tokens = sum(label != ignore_index for label in chosen_labels) + sum(label != ignore_index for label in rejected_labels)

    return {
        'prompt_input_ids': np.array(prompt_input_ids, dtype=np.uint32),
        'chosen_input_ids': np.array(chosen_input_ids, dtype=np.uint32),
        'chosen_labels': np.array(chosen_labels, dtype=np.int64),
        'rejected_input_ids': np.array(rejected_input_ids, dtype=np.uint32),
        'rejected_labels': np.array(rejected_labels, dtype=np.int64),
        'total_tokens': total_tokens,
        'supervised_tokens': supervised_tokens
    }

def download_and_prepare_data(
    *,
    config,
    seed,
    valid_datasets,
    probabilities,
    num_proc,
    target_tokens,
    validation_ratio,
    mix_strategy,
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

            source_system_prompt, prompt = extract_leading_system_prompt(prompt)

            prompt = ensure_only_user_assistant(prompt)
            prompt = ensure_user_first(prompt)
            prompt = ensure_user_last(prompt)
            prompt = ensure_alternating_prompt_for_dpo(prompt)
            prompt = ensure_nonempty_content(prompt)

            data['system_prompt'] = source_system_prompt
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

    logger.info(f'Using data mix strategy: {mix_strategy.value}')
    if mix_strategy == MixStrategy.LEGACY_INTERLEAVE:
        logger.info(f'Preparing HF Interleaving iterator... This operation can take a few minutes... Using stopping strategy: {interleave_stopping_strategy}')
        prepared_dataset = interleave_datasets(
            prepared_datasets,
            probabilities=probabilities,
            seed=seed,
            stopping_strategy=interleave_stopping_strategy
        )
        time.sleep(2) # Workaround for occasional streaming/interleave iterator shutdown issue.
    elif mix_strategy == MixStrategy.TOKEN_BUDGET:
        if target_tokens is None or target_tokens <= 0:
            raise ValueError(f'"target_tokens" must be set to a value > 0 when using mix strategy: {mix_strategy}')

        mix_target_tokens = math.ceil(target_tokens / (1 - validation_ratio))
        logger.info(f'Adjusted token budget from {target_tokens:,} to {mix_target_tokens:,} to account for validation_ratio={validation_ratio}')

        logger.info(f'Mixing data based in token budget... This operation can take a few minutes...')
        prepared_dataset = token_budget_dataset_mix(
            datasets=prepared_datasets,
            weights=probabilities,
            target_tokens=mix_target_tokens,
            seed=seed
        )
    else:
        raise ValueError(f'Invalid mix strategy: {mix_strategy}')

    logger.info(f'Applying {validation_ratio} train/val split...\n')
    splits = prepared_dataset.train_test_split(test_size=validation_ratio, seed=seed)

    train_ds = splits['train']
    train_ds_stats = compute_stats(train_ds)
    train_ds = train_ds.remove_columns(['total_tokens', 'supervised_tokens'])

    val_ds = splits['test']
    val_ds_stats = compute_stats(val_ds)
    val_ds = val_ds.remove_columns(['total_tokens', 'supervised_tokens'])

    logger.section('Train mixture')
    logger.info(train_ds_stats, is_json=True)

    logger.section('Validation mixture')
    logger.info(val_ds_stats, is_json=True)

    train_ds.save_to_disk(os.path.join(config.paths.datasets.training_path, 'train'))
    val_ds.save_to_disk(os.path.join(config.paths.datasets.training_path, 'val'))

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

    target_tokens = common_settings.get('target_tokens')
    if target_tokens is not None:
        target_tokens = int(target_tokens)

    validation_ratio = float(common_settings.get('validation_ratio', 0.01))
    if not 0.0 < validation_ratio < 1.0:
        raise ValueError('"validation_ratio" must be > 0 and < 1')

    download_and_prepare_data(
        config=config,
        seed=seed,
        valid_datasets=valid_datasets,
        probabilities=probabilities,
        num_proc=num_proc,
        target_tokens=target_tokens,
        validation_ratio=validation_ratio,
        mix_strategy=MixStrategy(common_settings.get('mix_strategy', MixStrategy.LEGACY_INTERLEAVE)),
        interleave_stopping_strategy=common_settings['interleave_stopping_strategy']
    )
