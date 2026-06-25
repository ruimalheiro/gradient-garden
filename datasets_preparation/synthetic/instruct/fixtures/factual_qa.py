FACTUAL_QA_FIXTURES = {
    'capital': {
        'prompt_templates': [
            'What is the capital of {country}? Answer in one short sentence.',
            'What is the capital of {country}? Only provide one short sentence.',
            'Name the capital of {country}. Answer in one short sentence.',
            'Which city is the capital of {country}? Answer in one short sentence.',
        ],
        'examples': [
            {
                'country': 'Portugal',
                'answer': 'The capital of Portugal is Lisbon.',
                'entities': ['Portugal'],
            },
            {
                'country': 'France',
                'answer': 'The capital of France is Paris.',
                'entities': ['France'],
            },
            {
                'country': 'Spain',
                'answer': 'The capital of Spain is Madrid.',
                'entities': ['Spain'],
            },
            {
                'country': 'spain',
                'answer': 'The capital of Spain is Madrid.',
                'entities': ['Spain'],
            },
            {
                'country': 'Italy',
                'answer': 'The capital of Italy is Rome.',
                'entities': ['Italy'],
            },
            {
                'country': 'Germany',
                'answer': 'The capital of Germany is Berlin.',
                'entities': ['Germany'],
            },
            {
                'country': 'Japan',
                'answer': 'The capital of Japan is Tokyo.',
                'entities': ['Japan'],
            },
            {
                'country': 'Canada',
                'answer': 'The capital of Canada is Ottawa.',
                'entities': ['Canada'],
            },
            {
                'country': 'Brazil',
                'answer': 'The capital of Brazil is Brasília.',
                'entities': ['Brazil'],
            },
            {
                'country': 'Ireland',
                'answer': 'The capital of Ireland is Dublin.',
                'entities': ['Ireland'],
            },
            {
                'country': 'Greece',
                'answer': 'The capital of Greece is Athens.',
                'entities': ['Greece'],
            },
            {
                'country': 'Norway',
                'answer': 'The capital of Norway is Oslo.',
                'entities': ['Norway'],
            },
            {
                'country': 'Sweden',
                'answer': 'The capital of Sweden is Stockholm.',
                'entities': ['Sweden'],
            },
            {
                'country': 'Netherlands',
                'answer': 'The capital of the Netherlands is Amsterdam.',
                'entities': ['Netherlands'],
            },
            {
                'country': 'United Kingdom',
                'answer': 'The capital of the United Kingdom is London.',
                'entities': ['United Kingdom'],
            },
        ],
    },
    'science': {
        'prompt_templates': [
            '{question} Answer in one short sentence.',
            '{question} Only provide one short sentence.',
            'Answer this science question in one short sentence: {question}',
        ],
        'examples': [
            {
                'question': 'What is the largest planet in the solar system?',
                'answer': 'The largest planet in the solar system is Jupiter.',
                'entities': ['Jupiter'],
            },
            {
                'question': 'What planet is closest to the Sun?',
                'answer': 'Mercury is the planet closest to the Sun.',
                'entities': ['Mercury', 'Sun'],
            },
            {
                'question': 'What is the freezing point of water in Celsius?',
                'answer': 'Water freezes at 0 degrees Celsius.',
                'entities': ['water', 'Celsius'],
            },
            {
                'question': 'What is the boiling point of water in Celsius?',
                'answer': 'Water boils at 100 degrees Celsius.',
                'entities': ['water', 'Celsius'],
            },
            {
                'question': 'What is water made of?',
                'answer': 'Water is made of hydrogen and oxygen.',
                'entities': ['water'],
            },
            {
                'question': 'What gas do plants take in during photosynthesis?',
                'answer': 'Plants take in carbon dioxide during photosynthesis.',
                'entities': ['photosynthesis'],
            },
            {
                'question': 'What gas do humans need to breathe?',
                'answer': 'Humans need oxygen to breathe.',
                'entities': ['humans'],
            },
            {
                'question': 'What star is closest to Earth?',
                'answer': 'The Sun is the closest star to Earth.',
                'entities': ['Earth'],
            },
            {
                'question': 'What force pulls objects toward Earth?',
                'answer': 'Gravity pulls objects toward Earth.',
                'entities': ['Earth'],
            },
            {
                'question': 'What do plants need to grow?',
                'answer': 'Plants need sunlight, water, air, and nutrients to grow.',
            },
            {'question': 'What do bees make?', 'answer': 'Bees make honey.'},
            {
                'question': 'What do lungs help people do?',
                'answer': 'Lungs help people breathe.',
            },
            {
                'question': 'What does the heart pump?',
                'answer': 'The heart pumps blood through the body.',
            },
            {
                'question': 'What does a thermometer measure?',
                'answer': 'A thermometer measures temperature.',
            },
            {
                'question': 'What does a compass show?',
                'answer': 'A compass shows direction.',
            },
        ],
    },
    'solar_system': {
        'prompt_templates': [
            '{question}',
            '{question} Answer in one short sentence.',
            '{question} Only provide the answer.',
            'Answer this astronomy question: {question}',
        ],
        'examples': [
            {
                'question': 'What are the planets in the solar system?',
                'answer': 'The planets are Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune.',
            },
            {
                'question': 'Name the planets in the solar system.',
                'answer': 'The planets are Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune.',
            },
            {
                'question': 'Which planets orbit the Sun?',
                'answer': 'Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune orbit the Sun.',
            },
            {
                'question': 'Is the Sun a planet?',
                'answer': 'No, the Sun is a star.',
            },
            {
                'question': 'Is the Moon a planet?',
                'answer': 'No, the Moon is Earth’s natural satellite.',
            },
            {
                'question': 'Which planet do humans live on?',
                'answer': 'Humans live on Earth.',
            },
            {
                'question': 'Which planet is known as the Red Planet?',
                'answer': 'Mars is known as the Red Planet.',
            },
            {
                'question': 'Which planet has rings and is famous for them?',
                'answer': 'Saturn is famous for its rings.',
            },
        ],
    },
    'counts': {
        'prompt_templates': [
            '{question} Answer in one short sentence.',
            '{question} Only provide one short sentence.',
            'Answer this counting question in one short sentence: {question}',
        ],
        'examples': [
            {
                'question': 'How many days are in a week?',
                'answer': 'There are seven days in a week.',
            },
            {
                'question': 'How many months are in a year?',
                'answer': 'There are twelve months in a year.',
            },
            {
                'question': 'How many sides does a triangle have?',
                'answer': 'A triangle has three sides.',
            },
            {
                'question': 'How many sides does a square have?',
                'answer': 'A square has four sides.',
            },
            {
                'question': 'How many wheels does a bicycle usually have?',
                'answer': 'A bicycle usually has two wheels.',
            },
            {
                'question': 'How many legs does a spider have?',
                'answer': 'A spider has eight legs.',
            },
            {
                'question': 'How many hours are in a day?',
                'answer': 'There are twenty-four hours in a day.',
            },
            {
                'question': 'How many minutes are in an hour?',
                'answer': 'There are sixty minutes in an hour.',
            },
            {
                'question': 'How many fingers are on one human hand?',
                'answer': 'One human hand usually has five fingers.',
            },
            {
                'question': 'How many seasons are in a year?',
                'answer': 'There are four seasons in a year.',
            },
        ],
    },
    'authors_art': {
        'prompt_templates': [
            '{question} Answer in one short sentence.',
            '{question} Only provide one short sentence.',
            'Answer this question in one short sentence: {question}',
        ],
        'examples': [
            {
                'question': 'Who wrote Romeo and Juliet?',
                'answer': 'William Shakespeare wrote Romeo and Juliet.',
                'entities': ['Romeo and Juliet'],
            },
            {
                'question': 'Who is the author of Romeo and Juliet?',
                'answer': 'William Shakespeare is the author of Romeo and Juliet.',
                'entities': ['Romeo and Juliet'],
            },
            {
                'question': 'Who wrote the play Romeo and Juliet?',
                'answer': 'William Shakespeare wrote the play Romeo and Juliet.',
                'entities': ['Romeo and Juliet'],
            },
            {
                'question': 'Who wrote Hamlet?',
                'answer': 'William Shakespeare wrote Hamlet.',
                'entities': ['Hamlet'],
            },
            {
                'question': 'Who painted the Mona Lisa?',
                'answer': 'Leonardo da Vinci painted the Mona Lisa.',
                'entities': ['Mona Lisa'],
            },
            {
                'question': 'Who painted The Starry Night?',
                'answer': 'Vincent van Gogh painted The Starry Night.',
                'entities': ['The Starry Night'],
            },
            {
                'question': 'Who wrote Pride and Prejudice?',
                'answer': 'Jane Austen wrote Pride and Prejudice.',
                'entities': ['Pride and Prejudice'],
            },
            {
                'question': 'Who wrote The Cat in the Hat?',
                'answer': 'Dr. Seuss wrote The Cat in the Hat.',
                'entities': ['The Cat in the Hat'],
            },
        ],
    },
    'animals': {
        'prompt_templates': [
            '{question} Answer in one short sentence.',
            '{question} Only provide one short sentence.',
            'Answer this animal question in one short sentence: {question}',
        ],
        'examples': [
            {
                'question': "What animal is known as man's best friend?",
                'answer': "Dogs are often called man's best friend.",
            },
            {
                'question': 'What animal gives us wool?',
                'answer': 'Sheep give us wool.',
            },
            {
                'question': 'What animal is known for producing honey?',
                'answer': 'Bees are known for producing honey.',
            },
            {
                'question': 'What do cows produce that people drink?',
                'answer': 'Cows produce milk that people drink.',
            },
            {'question': 'What animal says meow?', 'answer': 'Cats say meow.'},
            {'question': 'What animal says woof?', 'answer': 'Dogs say woof.'},
            {
                'question': 'What animal has a long trunk?',
                'answer': 'Elephants have long trunks.',
            },
            {
                'question': 'What animal is known for black and white stripes?',
                'answer': 'Zebras are known for black and white stripes.',
            },
            {
                'question': 'What animal is the largest land animal?',
                'answer': 'The elephant is the largest land animal.',
            },
            {
                'question': 'What animal is known for hopping and carrying babies in a pouch?',
                'answer': 'Kangaroos are known for hopping and carrying babies in a pouch.',
            },
        ],
    },
    'geography': {
        'prompt_templates': [
            '{question} Answer in one short sentence.',
            '{question} Only provide one short sentence.',
            'Answer this geography question in one short sentence: {question}',
        ],
        'examples': [
            {
                'question': 'What is the largest ocean on Earth?',
                'answer': 'The Pacific Ocean is the largest ocean on Earth.',
            },
            {
                'question': 'What is the tallest mountain on Earth?',
                'answer': 'Mount Everest is the tallest mountain on Earth.',
            },
            {
                'question': 'What continent is Egypt in?',
                'answer': 'Egypt is in Africa.',
            },
            {
                'question': 'What continent is Brazil in?',
                'answer': 'Brazil is in South America.',
            },
            {
                'question': 'What continent is France in?',
                'answer': 'France is in Europe.',
            },
            {
                'question': 'What continent is Japan in?',
                'answer': 'Japan is in Asia.',
            },
            {
                'question': 'What ocean is east of the United States?',
                'answer': 'The Atlantic Ocean is east of the United States.',
            },
            {
                'question': 'What ocean is west of the United States?',
                'answer': 'The Pacific Ocean is west of the United States.',
            },
            {
                'question': 'What country is Lisbon in?',
                'answer': 'Lisbon is in Portugal.',
            },
            {
                'question': 'What country is Paris in?',
                'answer': 'Paris is in France.',
            },
        ],
    },
    'objects_body_plants': {
        'prompt_templates': [
            '{question} Answer in one short sentence.',
            '{question} Only provide one short sentence.',
            'Answer this question in one short sentence: {question}',
        ],
        'examples': [
            {
                'question': 'What do people use to tell time?',
                'answer': 'People use clocks to tell time.',
            },
            {
                'question': 'What do people use to cut paper?',
                'answer': 'People use scissors to cut paper.',
            },
            {
                'question': 'What do people use to write on a board?',
                'answer': 'People use chalk or markers to write on a board.',
            },
            {
                'question': 'What does a map show?',
                'answer': 'A map shows places and directions.',
            },
            {
                'question': 'What do roots do for a plant?',
                'answer': 'Roots help a plant absorb water and nutrients.',
            },
            {
                'question': 'What do eyes help people do?',
                'answer': 'Eyes help people see.',
            },
            {
                'question': 'What do ears help people do?',
                'answer': 'Ears help people hear.',
            },
            {
                'question': 'What do teeth help people do?',
                'answer': 'Teeth help people chew food.',
            },
            {
                'question': 'What do leaves help plants do?',
                'answer': 'Leaves help plants make food from sunlight.',
            },
            {
                'question': 'What does a key open?',
                'answer': 'A key opens a lock.',
            },
            {
                'question': 'What does a pencil write with?',
                'answer': 'A pencil writes with graphite.',
            },
            {
                'question': 'What does an umbrella protect people from?',
                'answer': 'An umbrella protects people from rain or sun.',
            },
        ],
    },
    'opposites': {
        'prompt_templates': [
            '{question} Answer with one word.',
            '{question} Only provide one word.',
            'Answer with exactly one word: {question}',
        ],
        'examples': [
            {'question': 'What is the opposite of hot?', 'answer': 'cold'},
            {'question': 'What is the opposite of up?', 'answer': 'down'},
            {'question': 'What is the opposite of left?', 'answer': 'right'},
            {'question': 'What is the opposite of fast?', 'answer': 'slow'},
            {'question': 'What is the opposite of big?', 'answer': 'small'},
            {'question': 'What is the opposite of happy?', 'answer': 'sad'},
            {'question': 'What is the opposite of open?', 'answer': 'closed'},
            {'question': 'What is the opposite of day?', 'answer': 'night'},
            {'question': 'What is the opposite of light?', 'answer': 'dark'},
            {'question': 'What is the opposite of full?', 'answer': 'empty'},
        ],
    },
    'one_word_factual': {
        'prompt_templates': [
            'Answer with exactly one word: {question}',
            '{question} Answer with exactly one word.',
            '{question} Only provide one word.',
            'Answer this question with one word only: {question}',
        ],
        'examples': [
            {
                'question': 'What color is the sky on a clear day?',
                'answer': 'blue',
            },
            {'question': 'What color is grass?', 'answer': 'green'},
            {'question': 'What color is snow?', 'answer': 'white'},
            {'question': 'What color is a ripe banana?', 'answer': 'yellow'},
            {'question': 'What animal says meow?', 'answer': 'cat'},
            {'question': 'What animal says woof?', 'answer': 'dog'},
            {'question': 'What do bees make?', 'answer': 'honey'},
            {'question': 'What do cows produce?', 'answer': 'milk'},
            {'question': 'What planet do humans live on?', 'answer': 'Earth'},
            {'question': 'What star gives Earth light?', 'answer': 'Sun'},
            {'question': 'What gas do humans breathe?', 'answer': 'oxygen'},
            {'question': 'What gas do plants take in?', 'answer': 'carbon'},
            {'question': 'What is frozen water called?', 'answer': 'ice'},
            {'question': 'What is liquid rain made of?', 'answer': 'water'},
            {
                'question': 'What do people use to tell time?',
                'answer': 'clock',
            },
            {'question': 'What shape has three sides?', 'answer': 'triangle'},
            {
                'question': 'What shape has four equal sides?',
                'answer': 'square',
            },
            {'question': 'What sense uses the ears?', 'answer': 'hearing'},
            {'question': 'What sense uses the eyes?', 'answer': 'sight'},
            {'question': 'What organ pumps blood?', 'answer': 'heart'},
        ],
    },
    'health_safety': {
        'prompt_templates': [
            '{question}',
            '{question} Answer in one short sentence.',
            'Answer this health question in one short sentence: {question}',
        ],
        'examples': [
            {
                'question': 'Is smoking healthy?',
                'answer': 'No, smoking is harmful to health.',
            },
            {
                'question': 'Is smoking good for your lungs?',
                'answer': 'No, smoking is bad for your lungs.',
            },
            {
                'question': 'Is drinking water important?',
                'answer': 'Yes, drinking water is important for health.',
            },
            {
                'question': 'Is exercise usually good for health?',
                'answer': 'Yes, exercise is usually good for health.',
            },
            {
                'question': 'Is sleep important for health?',
                'answer': 'Yes, sleep is important for health.',
            },
            {
                'question': 'Is eating only candy healthy?',
                'answer': 'No, eating only candy is not healthy.',
            },
            {
                'question': 'Can washing hands help prevent germs?',
                'answer': 'Yes, washing hands can help prevent germs.',
            },
            {
                'question': 'Can brushing teeth help keep teeth healthy?',
                'answer': 'Yes, brushing teeth helps keep teeth healthy.',
            },
            {
                'question': 'Is fresh air usually good for people?',
                'answer': 'Yes, fresh air is usually good for people.',
            },
            {
                'question': 'Is too much sugar usually healthy?',
                'answer': 'No, too much sugar is usually unhealthy.',
            },
        ],
    },
}
