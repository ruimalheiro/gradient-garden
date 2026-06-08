import random

from pathlib import Path
from utils import save_jsonl_file
from logger import logger


def build_constraints_dataset(*, config, ds_id, seed, count, transforms):
    logger.info(f'Generating synthetic constraints dataset...')

    current_dir = Path(__file__).resolve().parent.parent.parent

    target_dir = current_dir / ds_id
    target_dir.mkdir(parents=True, exist_ok=True)
    data_filename = target_dir / 'constraints.jsonl'

    if data_filename.exists():
        logger.warn(f'Synthetic constraints dataset raw source already exists: {data_filename}')
        return

    rng = random.Random(seed)

    custom_example_count = transforms.get('count', None)

    count = custom_example_count if custom_example_count else count

    logger.info(f'generating {count} examples...')

    def row(user_content, assistant_content):
        return {
            'messages': [
                {'role': 'user', 'content': user_content.strip()},
                {'role': 'assistant', 'content': assistant_content.strip()}
            ]
        }

    examples = []

    fruits = [
        'apple',
        'banana',
        'orange',
        'pear',
        'grape',
        'mango',
        'peach',
        'plum',
        'kiwi',
        'pineapple',
        'melon',
        'cherry'
    ]

    topics = {
        'rain': [
            'Rain falls from clouds and helps plants grow.',
            'Rain brings water to rivers, lakes, and soil.',
            'Rain is water that falls from clouds to the ground.',
        ],
        'snow': [
            'Snow is frozen water that falls from clouds in cold weather.',
            'Snow can cover the ground when the air is cold enough.',
        ],
        'sleep': [
            'Sleep helps the body rest, recover, and store memories.',
            'Sleep gives the brain and body time to recharge.',
        ],
    }

    rewrites = [
        (
            'The thing was bad because it was not good.',
            'The item was poor quality.',
        ),
        (
            'He went to the place where the thing happened.',
            'He went to the location where the event occurred.',
        ),
        (
            'The food was nice and I liked it a lot.',
            'I really enjoyed the food.',
        ),
        (
            'This is a thing that people use to do work.',
            'This is a tool people use for work.',
        ),
    ]

    grammar = [
        ("He don't like apples.", "He doesn't like apples."),
        ('She go to school every day.', 'She goes to school every day.'),
        ('They was happy.', 'They were happy.'),
        ('I has a book.', 'I have a book.'),
        ('The cats is sleeping.', 'The cats are sleeping.'),
    ]

    procedures = [
        (
            'cooking a boiled egg',
            [
                'Place the egg in a pot and cover it with water.',
                'Bring the water to a boil, then simmer for 9 to 12 minutes.',
                'Cool the egg in cold water, then peel it.',
            ],
        ),
        (
            'brushing your teeth',
            [
                'Put toothpaste on a toothbrush.',
                'Brush all sides of your teeth for about two minutes.',
                'Rinse your mouth and toothbrush with water.',
            ],
        ),
        (
            'making toast',
            [
                'Place a slice of bread in the toaster.',
                'Toast it until it is golden brown.',
                'Remove it carefully and add butter or another topping.',
            ],
        ),
    ]

    examples = []

    # exactly three items sepparated by comma
    for _ in range(800):
        chosen = random.sample(fruits, 3)
        prompt = 'List exactly three fruits, separated by commas.'
        answer = ', '.join(chosen)
        examples.append({
            'messages': [
                {'role': 'user', 'content': prompt},
                {'role': 'assistant', 'content': answer},
            ]
        })

    # one-sentence answers
    for _ in range(800):
        topic = random.choice(list(topics.keys()))
        answer = random.choice(topics[topic])
        prompt = f'Write exactly one sentence about {topic}.'
        examples.append({
            'messages': [
                {'role': 'user', 'content': prompt},
                {'role': 'assistant', 'content': answer},
            ]
        })

    # rewriting in a cleaner way
    for _ in range(800):
        bad, good = random.choice(rewrites)
        prompt = (
            f'Rewrite this sentence to be clearer:\n'
            f'{bad}\n'
            f'Only provide the rewritten sentence.'
        )
        examples.append({
            'messages': [
                {'role': 'user', 'content': prompt},
                {'role': 'assistant', 'content': good},
            ]
        })

    # grammar-only
    for _ in range(800):
        bad, good = random.choice(grammar)
        prompt = (
            f'Correct the grammar of this sentence:\n'
            f'{bad}\n'
            f'Only provide the corrected sentence.'
        )
        examples.append({
            'messages': [
                {'role': 'user', 'content': prompt},
                {'role': 'assistant', 'content': good},
            ]
        })

    # exactly three numbered steps
    for _ in range(800):
        task, steps = random.choice(procedures)
        answer = '\n'.join(f'{i + 1}. {step}' for i, step in enumerate(steps))
        prompt = f'Give exactly three numbered steps for {task}.'
        examples.append({
            'messages': [
                {'role': 'user', 'content': prompt},
                {'role': 'assistant', 'content': answer},
            ]
        })

    random.shuffle(examples)

    save_jsonl_file(data_filename, examples)
    logger.info(f'Synthetic constraints dataset completed and stored at: {data_filename}')
