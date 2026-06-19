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

def generate_weighted_group_examples(*, groups, transforms, count, dedupe_key_fn=None):
    oversample_factor = transforms.get('oversample_factor', 1.0)
    generation_count = round(count * oversample_factor)

    default_weights = {
        group_name: default_weight
        for group_name, (_, default_weight) in groups.items()
    }

    weights = resolve_group_weights(default_weights, transforms)

    logger.section('Applied weights')
    for group_name, weight in weights.items():
        logger.info(f'{group_name}: {weight:.2f}')

    resolved_groups = [
        (group_name, generator_fn, weights[group_name])
        for group_name, (generator_fn, _) in groups.items()
    ]

    remaining_to_generate = generation_count
    remaining = remaining_to_generate

    logger.section('Generation')
    examples = []

    for group_idx, (group_name, generator_fn, weight) in enumerate(resolved_groups):
        if group_idx == len(resolved_groups) - 1:
            group_count = remaining
        else:
            group_count = round(generation_count * weight)
            remaining -= group_count

        logger.info(f'generating {group_count} examples for group: {group_name}')

        for _ in range(group_count):
            examples.append(generator_fn())

    max_duplicates_per_example = transforms.get('max_duplicates_per_example')
    deduped = limit_duplicate_examples(
        examples,
        dedupe_key_fn,
        max_duplicates_per_example,
    )

    if len(deduped) != len(examples):
        logger.info(f'removed {len(examples) - len(deduped)} examples above duplicate limit')

    if len(deduped) < count:
        logger.info(
            f'warning: requested {count} examples but only '
            f'{len(deduped)} examples were generated after duplicate limiting. '
            'Increase oversample_factor, increase max_duplicates_per_example, '
            'or add more fixture variety.'
        )

    logger.info('\n')
    return deduped[:count]
