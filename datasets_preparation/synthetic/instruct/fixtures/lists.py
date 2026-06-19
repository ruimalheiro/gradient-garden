LIST_FIXTURES = {
    'dedup': {
        'examples': [
            {
                'prompt': 'List exactly three unique fruits, separated by commas. Only provide the list.',
                'answer': 'apple, banana, orange',
            },
            {
                'prompt': 'List exactly three unique animals, separated by commas. Only provide the list.',
                'answer': 'cat, dog, rabbit',
            },
            {
                'prompt': 'List exactly three unique colors, separated by commas. Only provide the list.',
                'answer': 'red, blue, green',
            },
            {
                'prompt': 'List exactly three unique vegetables, separated by commas. Only provide the list.',
                'answer': 'carrot, onion, broccoli',
            },
            {
                'prompt': 'List exactly three unique programming languages, separated by commas. Only provide the list.',
                'answer': 'Python, JavaScript, Rust',
            },
            {
                'prompt': 'List exactly three unique countries, separated by commas. Only provide the list.',
                'answer': 'Portugal, France, Japan',
            },
            {
                'prompt': 'List exactly three unique cities, separated by commas. Only provide the list.',
                'answer': 'London, Lisbon, Paris',
            },
            {
                'prompt': 'List exactly three unique school subjects, separated by commas. Only provide the list.',
                'answer': 'math, history, science',
            },
            {
                'prompt': 'List exactly three unique sports, separated by commas. Only provide the list.',
                'answer': 'soccer, tennis, basketball',
            },
            {
                'prompt': 'List exactly three unique drinks, separated by commas. Only provide the list.',
                'answer': 'water, tea, coffee',
            },
        ],
    },

    'sampled_categories': {
        'examples': [
            {
                'category': 'fruits',
                'count': 3,
                'items': [
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
                    'cherry',
                ],
                'prompt_templates': [
                    'List exactly three unique {category}, separated by commas. Only provide the list.',
                    'Name exactly three unique {category}, separated by commas. Only provide the list.',
                    'Give exactly three unique {category}. Use commas and no extra text.',
                    'Provide exactly three unique {category}, separated only by commas.',
                ],
            },
            {
                'category': 'colors',
                'count': 3,
                'items': [
                    'red',
                    'blue',
                    'green',
                    'yellow',
                    'purple',
                    'orange',
                    'black',
                    'white',
                    'pink',
                    'brown',
                ],
                'prompt_templates': [
                    'List exactly three unique {category}, separated by commas. Only provide the list.',
                    'Name exactly three unique {category}, separated by commas. Only provide the list.',
                    'Give exactly three unique {category}. Use commas and no extra text.',
                    'Provide exactly three unique {category}, separated only by commas.',
                ],
            },
            {
                'category': 'animals',
                'count': 3,
                'items': [
                    'cat',
                    'dog',
                    'horse',
                    'rabbit',
                    'lion',
                    'tiger',
                    'zebra',
                    'bear',
                    'fox',
                    'elephant',
                ],
                'prompt_templates': [
                    'List exactly three unique {category}, separated by commas. Only provide the list.',
                    'Name exactly three unique {category}, separated by commas. Only provide the list.',
                    'Give exactly three unique {category}. Use commas and no extra text.',
                    'Provide exactly three unique {category}, separated only by commas.',
                ],
            },
            {
                'category': 'tools',
                'count': 3,
                'items': [
                    'hammer',
                    'screwdriver',
                    'wrench',
                    'drill',
                    'saw',
                    'pliers',
                    'level',
                    'tape measure',
                ],
                'prompt_templates': [
                    'List exactly three unique {category}, separated by commas. Only provide the list.',
                    'Name exactly three unique {category}, separated by commas. Only provide the list.',
                    'Give exactly three unique {category}. Use commas and no extra text.',
                    'Provide exactly three unique {category}, separated only by commas.',
                ],
            },
        ],
    },
}
