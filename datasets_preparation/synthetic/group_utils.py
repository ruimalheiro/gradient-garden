from logger import logger


def resolve_group_weights(default_weights, transforms):
    custom_weights = transforms.get('weights', {})

    unknown_groups = set(custom_weights) - set(default_weights)

    if unknown_groups:
        raise ValueError(
            f'Unknown weight groups: {sorted(unknown_groups)}. '
            f'Expected one of: {sorted(default_weights)}'
        )

    weights = {
        group_name: custom_weights.get(group_name, default_weight)
        for group_name, default_weight in default_weights.items()
    }

    negative_weights = {
        group_name: weight
        for group_name, weight in weights.items()
        if weight < 0
    }

    if negative_weights:
        raise ValueError(f'Group weights must be non-negative. Got: {negative_weights}')

    total_weight = sum(weights.values())

    if total_weight <= 0:
        raise ValueError(f'Group weights must sum to a positive value. Got: {weights}')

    return {
        group_name: weight / total_weight
        for group_name, weight in weights.items()
    }

def choose_weighted_group(*, rng, groups, transforms=None):
    default_weights = {
        group_name: default_weight
        for group_name, default_weight in groups.items()
    }

    weights = resolve_group_weights(default_weights, transforms or {})

    value = rng.random()
    cumulative = 0.0

    for group_name, weight in weights.items():
        cumulative += weight

        if value <= cumulative:
            return group_name

    return next(reversed(weights))

def limit_duplicate_examples(examples, dedupe_key_fn, max_duplicates_per_example):
    if dedupe_key_fn is None or max_duplicates_per_example is None:
        return examples

    logger.info(f'Deduplicating... Max duplicates allowed: {max_duplicates_per_example}')

    counts = {}
    limited = []

    for example in examples:
        key = dedupe_key_fn(example)
        count = counts.get(key, 0)

        if count >= max_duplicates_per_example:
            continue

        counts[key] = count + 1
        limited.append(example)

    return limited

def allocate_group_counts(*, groups, weights, count):
    resolved = []
    remaining = count

    group_items = list(groups.items())

    for group_idx, (group_name, _) in enumerate(group_items):
        if group_idx == len(group_items) - 1:
            group_count = remaining
        else:
            group_count = round(count * weights[group_name])
            remaining -= group_count

        resolved.append((group_name, group_count))

    return resolved

def generate_weighted_group_examples(
    *,
    groups,
    transforms,
    count,
    dedupe_key_fn=None,
    rng=None,
):
    oversample_factor = transforms.get('oversample_factor', 1.0)
    max_duplicates_per_example = transforms.get('max_duplicates_per_example')

    default_weights = {
        group_name: default_weight
        for group_name, (_, default_weight) in groups.items()
    }

    weights = resolve_group_weights(default_weights, transforms)

    logger.section('Applied weights')
    for group_name, weight in weights.items():
        logger.info(f'{group_name}: {weight:.2f}')

    group_counts = allocate_group_counts(
        groups=groups,
        weights=weights,
        count=count,
    )

    logger.section('Generation')

    examples = []

    for group_name, group_target_count in group_counts:
        generator_fn, _ = groups[group_name]
        group_generation_count = round(group_target_count * oversample_factor)

        logger.info(
            f'generating {group_generation_count} examples for group: '
            f'{group_name} target: {group_target_count}'
        )

        group_examples = [
            generator_fn()
            for _ in range(group_generation_count)
        ]

        limited_group_examples = limit_duplicate_examples(
            group_examples,
            dedupe_key_fn,
            max_duplicates_per_example,
        )

        if len(limited_group_examples) != len(group_examples):
            logger.info(
                f'{group_name}: removed '
                f'{len(group_examples) - len(limited_group_examples)} '
                'examples above duplicate limit'
            )

        if len(limited_group_examples) < group_target_count:
            logger.info(
                f'warning: group {group_name} requested '
                f'{group_target_count} examples but only '
                f'{len(limited_group_examples)} were available after '
                'duplicate limiting.'
            )

        examples.extend(limited_group_examples[:group_target_count])

    if len(examples) < count:
        logger.info(
            f'warning: requested {count} examples but only '
            f'{len(examples)} examples were generated after group-level '
            'duplicate limiting.'
        )

    if rng is not None:
        rng.shuffle(examples)

    logger.info('\n')
    return examples[:count]
