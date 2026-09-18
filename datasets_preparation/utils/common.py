import hashlib

from datasets import concatenate_datasets
from recipes.config import MixStrategy
from logger import logger


def stable_hash(text, *, seed=None, hash_bytes=8):
    # fast and stable hash. More info: https://docs.python.org/3/library/hashlib.html#blake2
    if seed is not None:
        salt = f'{seed}-salt'.encode('utf-8')
        return int.from_bytes(hashlib.blake2b(text.encode(), digest_size=hash_bytes, key=salt).digest(), 'big')
    return int.from_bytes(hashlib.blake2b(text.encode(), digest_size=hash_bytes).digest(), 'big')

def make_source_key(ds_id, name):
    if name and name != 'default':
        return f'{ds_id}::{name}'
    return ds_id

def assert_common_structure_and_extract(datasets_mix, supported_datasets):
    ''' Validates common file structure and extracts seed, common dataset settings, valid datasets and probabilities (normalized weight distribution)
    '''
    assert 'seed' in datasets_mix
    seed = datasets_mix['seed']
    assert isinstance(seed, int)

    # Validate common settings if present.
    common_settings = datasets_mix.get('datasets_common_settings', {})

    shard_size = None
    target_tokens = None
    validation_ratio = None

    assert 'mix_strategy' in common_settings, 'common_settings.mix_strategy is required'
    mix_strategy = common_settings['mix_strategy']

    if 'shard_size' in common_settings:
        shard_size = common_settings['shard_size']
        assert shard_size is None or int(shard_size) > 0, 'datasets_common_settings.shard_size must be > 0'
    if 'target_tokens' in common_settings:
        target_tokens = common_settings['target_tokens']
        assert target_tokens is None or isinstance(target_tokens, int), 'datasets_common_settings.target_tokens must be an integer'

        if mix_strategy == MixStrategy.TOKEN_BUDGET:
            assert target_tokens is None, 'common_settings.target_tokens cannot be set when using mix strategy token_budget. Targets must be set per dataset.'

    if 'validation_ratio' in common_settings:
        validation_ratio = common_settings['validation_ratio']
        assert validation_ratio is None or isinstance(validation_ratio, float), 'datasets_common_settings.validation_ratio must be a float'
    assert 'interleave_stopping_strategy' in common_settings, 'common_settings.interleave_stopping_strategy is required'


    assert 'datasets' in datasets_mix
    datasets = datasets_mix['datasets']

    probabilities = None

    # Validate candidates
    valid_datasets = []
    for dataset_id, names in datasets.items():
        assert dataset_id in supported_datasets

        for name in names:
            assert name in supported_datasets[dataset_id]

            if mix_strategy == MixStrategy.LEGACY_INTERLEAVE:
                assert datasets[dataset_id][name].get('target_tokens') is None, '"target_tokens" per ds cannot be set with the current mix strategy'
                assert 'weight' in datasets[dataset_id][name]
                assert datasets[dataset_id][name]['weight'] is not None, 'weight needs to be specified per dataset.'
                weight = float(datasets[dataset_id][name].get('weight', 0.0))
                assert weight >= 0.0, f'weight must be >= 0 for {dataset_id}/{name}'
                if weight > 0:
                    valid_datasets.append({
                        'id': dataset_id,
                        'name': name,
                        **datasets[dataset_id][name],
                        'weight': weight,
                    })
            elif mix_strategy == MixStrategy.TOKEN_BUDGET:
                assert datasets[dataset_id][name].get('weight') is None, '"weight" per ds cannot be set with the current mix strategy'
                assert 'target_tokens' in datasets[dataset_id][name]
                assert datasets[dataset_id][name]['target_tokens'] is not None, 'target_tokens needs to be specified per dataset.'
                target_tokens = int(datasets[dataset_id][name].get('target_tokens', 0))
                if target_tokens > 0:
                    valid_datasets.append({
                        'id': dataset_id,
                        'name': name,
                        **datasets[dataset_id][name],
                        'target_tokens': target_tokens,
                    })

    if mix_strategy == MixStrategy.LEGACY_INTERLEAVE:
        assert valid_datasets, 'No datasets with weight > 0'

        probabilities = [ds['weight'] for ds in valid_datasets]

        # normalize probabilities
        total_p = sum(probabilities)
        assert total_p > 0.0, 'weight distribution must have positive total weight'
        probabilities = [p / total_p for p in probabilities]

        mixture_probs = [
            {make_source_key(ds['id'], ds.get('name', None)): round(p, 3)}
            for ds, p in zip(valid_datasets, probabilities)
        ]
        logger.info(f'Mixture probabilities: {mixture_probs}\n')
    elif mix_strategy == MixStrategy.TOKEN_BUDGET:
        assert valid_datasets, 'No datasets with target_tokens > 0'

        total_target_tokens = sum([ds['target_tokens'] for ds in valid_datasets])
        mixture_target_tokens = [
            {make_source_key(ds['id'], ds.get('name', None)): ds['target_tokens']}
            for ds in valid_datasets
        ]
        logger.info(f'Mixture target_tokens: {mixture_target_tokens}')
        logger.info(f'Total target tokens: {total_target_tokens}\n')

    return seed, common_settings, valid_datasets, probabilities

def token_budget_dataset_mix(*, datasets, weights, target_tokens, seed):
    weights_total = sum(weights)
    target_counts = [int(target_tokens * (weight / weights_total)) for weight in weights]

    prepared_datasets = []
    for dataset, target_count in zip(datasets, target_counts):
        if target_count == 0:
            continue

        shuffled_ds = dataset.shuffle(seed=seed)

        selected_indices = []
        tokens = 0
        for i, example in enumerate(shuffled_ds):
            selected_indices.append(i)
            tokens += example['supervised_tokens']
            if tokens >= target_count:
                break

        if tokens < target_count:
            logger.warning(f'Dataset exhausted before reaching token target: {dataset} - {tokens:,}/{target_count:,}')

        prepared_datasets.append(shuffled_ds.select(selected_indices))

    prepared_dataset = concatenate_datasets(prepared_datasets)

    return prepared_dataset

def compute_stats(prepared_dataset):
    stats_per_dataset = {}

    for source, total_tokens, supervised_tokens in zip(
        prepared_dataset['source'],
        prepared_dataset['total_tokens'],
        prepared_dataset['supervised_tokens']
    ):
        if source not in stats_per_dataset:
            stats_per_dataset[source] = {
                'examples': 0,
                'total_tokens': 0,
                'supervised_tokens': 0,
            }

        stats_per_dataset[source]['examples'] += 1
        stats_per_dataset[source]['total_tokens'] += total_tokens
        stats_per_dataset[source]['supervised_tokens'] += supervised_tokens

    total_examples = sum(s['examples'] for s in stats_per_dataset.values())
    total_tokens = sum(s['total_tokens'] for s in stats_per_dataset.values())
    total_supervised_tokens = sum(s['supervised_tokens'] for s in stats_per_dataset.values())

    for source, source_stats in stats_per_dataset.items():
        stats_per_dataset[source]['examples %'] = f'{source_stats["examples"] / total_examples:.2%}'
        stats_per_dataset[source]['tokens %'] = f'{source_stats["total_tokens"] / total_tokens:.2%}'
        stats_per_dataset[source]['supervised_tokens %'] = f'{source_stats["supervised_tokens"] / total_supervised_tokens:.2%}'

    return {
        'total_examples': total_examples,
        'total_tokens': total_tokens,
        'total_supervised_tokens': total_supervised_tokens,
        'sources': stats_per_dataset
    }
