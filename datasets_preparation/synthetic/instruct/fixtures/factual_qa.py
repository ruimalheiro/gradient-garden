FACTUAL_QA_FIXTURES = {
    'capital': {
        'examples': [
            {
                'prompt': 'What is the capital of Portugal? Answer in one short sentence.',
                'answer': 'The capital of Portugal is Lisbon.',
                'entities': ['Portugal'],
            },
            {
                'prompt': 'What is the capital of France? Answer in one short sentence.',
                'answer': 'The capital of France is Paris.',
                'entities': ['France'],
            },
            {
                'prompt': 'What is the capital of Spain? Answer in one short sentence.',
                'answer': 'The capital of Spain is Madrid.',
                'entities': ['Spain'],
            },
            {
                'prompt': 'What is the capital of Italy? Answer in one short sentence.',
                'answer': 'The capital of Italy is Rome.',
                'entities': ['Italy'],
            },
            {
                'prompt': 'What is the capital of Germany? Answer in one short sentence.',
                'answer': 'The capital of Germany is Berlin.',
                'entities': ['Germany'],
            },
            {
                'prompt': 'What is the capital of Japan? Answer in one short sentence.',
                'answer': 'The capital of Japan is Tokyo.',
                'entities': ['Japan'],
            },
        ],
    },

    'science': {
        'examples': [
            {
                'prompt': 'What is the largest planet in the solar system? Answer in one short sentence.',
                'answer': 'The largest planet in the solar system is Jupiter.',
                'entities': ['Jupiter'],
            },
            {
                'prompt': 'What planet is closest to the Sun? Answer in one short sentence.',
                'answer': 'Mercury is the planet closest to the Sun.',
                'entities': ['Mercury', 'Sun'],
            },
            {
                'prompt': 'What is the freezing point of water in Celsius? Answer in one short sentence.',
                'answer': 'Water freezes at 0 degrees Celsius.',
                'entities': ['water', 'Celsius'],
            },
            {
                'prompt': 'What is the boiling point of water in Celsius? Answer in one short sentence.',
                'answer': 'Water boils at 100 degrees Celsius.',
                'entities': ['water', 'Celsius'],
            },
            {
                'prompt': 'What is water made of? Answer in one short sentence.',
                'answer': 'Water is made of hydrogen and oxygen.',
                'entities': ['water'],
            },
            {
                'prompt': 'What gas do plants take in during photosynthesis? Answer in one short sentence.',
                'answer': 'Plants take in carbon dioxide during photosynthesis.',
                'entities': ['photosynthesis'],
            },
            {
                'prompt': 'What gas do humans need to breathe? Answer in one short sentence.',
                'answer': 'Humans need oxygen to breathe.',
                'entities': ['humans'],
            },
            {
                'prompt': 'What star is closest to Earth? Answer in one short sentence.',
                'answer': 'The Sun is the closest star to Earth.',
                'entities': ['Earth'],
            },
            {
                'prompt': 'What force pulls objects toward Earth? Answer in one short sentence.',
                'answer': 'Gravity pulls objects toward Earth.',
                'entities': ['Earth'],
            },
        ],
    },

    'counts': {
        'examples': [
            {'prompt': 'How many days are in a week? Answer in one short sentence.', 'answer': 'There are seven days in a week.'},
            {'prompt': 'How many months are in a year? Answer in one short sentence.', 'answer': 'There are twelve months in a year.'},
            {'prompt': 'How many sides does a triangle have? Answer in one short sentence.', 'answer': 'A triangle has three sides.'},
            {'prompt': 'How many sides does a square have? Answer in one short sentence.', 'answer': 'A square has four sides.'},
        ],
    },

    'authors_art': {
        'examples': [
            {
                'prompt': 'Who wrote Romeo and Juliet? Answer in one short sentence.',
                'answer': 'William Shakespeare wrote Romeo and Juliet.',
                'entities': ['Romeo and Juliet'],
            },
            {
                'prompt': 'Who painted the Mona Lisa? Answer in one short sentence.',
                'answer': 'Leonardo da Vinci painted the Mona Lisa.',
                'entities': ['Mona Lisa'],
            },
        ],
    },

    'animals': {
        'examples': [
            {'prompt': "What animal is known as man's best friend? Answer in one short sentence.", 'answer': "Dogs are often called man's best friend."},
            {'prompt': 'What animal gives us wool? Answer in one short sentence.', 'answer': 'Sheep give us wool.'},
            {'prompt': 'What animal is known for producing honey? Answer in one short sentence.', 'answer': 'Bees are known for producing honey.'},
            {'prompt': 'What do cows produce that people drink? Answer in one short sentence.', 'answer': 'Cows produce milk that people drink.'},
        ],
    },

    'geography': {
        'examples': [
            {'prompt': 'What is the largest ocean on Earth? Answer in one short sentence.', 'answer': 'The Pacific Ocean is the largest ocean on Earth.'},
            {'prompt': 'What is the tallest mountain on Earth? Answer in one short sentence.', 'answer': 'Mount Everest is the tallest mountain on Earth.'},
            {'prompt': 'What continent is Egypt in? Answer in one short sentence.', 'answer': 'Egypt is in Africa.'},
            {'prompt': 'What continent is Brazil in? Answer in one short sentence.', 'answer': 'Brazil is in South America.'},
        ],
    },

    'objects_body_plants': {
        'examples': [
            {'prompt': 'What do people use to tell time? Answer in one short sentence.', 'answer': 'People use clocks to tell time.'},
            {'prompt': 'What do people use to cut paper? Answer in one short sentence.', 'answer': 'People use scissors to cut paper.'},
            {'prompt': 'What do people use to write on a board? Answer in one short sentence.', 'answer': 'People use chalk or markers to write on a board.'},
            {'prompt': 'What does a thermometer measure? Answer in one short sentence.', 'answer': 'A thermometer measures temperature.'},
            {'prompt': 'What does a map show? Answer in one short sentence.', 'answer': 'A map shows places and directions.'},
            {'prompt': 'What do roots do for a plant? Answer in one short sentence.', 'answer': 'Roots help a plant absorb water and nutrients.'},
            {'prompt': 'What do lungs help people do? Answer in one short sentence.', 'answer': 'Lungs help people breathe.'},
            {'prompt': 'What does the heart pump? Answer in one short sentence.', 'answer': 'The heart pumps blood through the body.'},
        ],
    },

    'opposites': {
        'examples': [
            {'prompt': 'What is the opposite of hot? Answer with one word.', 'answer': 'Cold'},
            {'prompt': 'What is the opposite of up? Answer with one word.', 'answer': 'Down'},
            {'prompt': 'What is the opposite of left? Answer with one word.', 'answer': 'Right'},
        ],
    },
}
