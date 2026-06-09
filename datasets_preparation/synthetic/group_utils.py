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

def generate_weighted_group_examples(*, groups, transforms, count):
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

    remaining_to_generate = count
    remaining = remaining_to_generate

    logger.section('Generation')
    examples = []

    for group_idx, (group_name, generator_fn, weight) in enumerate(resolved_groups):
        if group_idx == len(resolved_groups) - 1:
            group_count = remaining
        else:
            group_count = round(remaining_to_generate * weight)
            remaining -= group_count

        logger.info(f'generating {group_count} examples for group: {group_name}')

        for _ in range(group_count):
            examples.append(generator_fn())

    logger.info('\n')
    return examples
