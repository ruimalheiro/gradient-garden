EXACT_WORD_COUNT_FIXTURES = {
    'one_word': {
        'prompt_templates': [
            'Answer with exactly one word: {question}',
            '{question} Answer with exactly one word.',
            'Answer with one word only: {question}',
            '{question} Only provide one word.',
            'Use exactly one word to answer: {question}',
        ],
        'examples': [
            {
                'question': 'What color is the sky on a clear day?',
                'answer': 'blue',
            },
            {'question': 'What is the opposite of hot?', 'answer': 'cold'},
            {'question': 'What animal says meow?', 'answer': 'cat'},
            {'question': 'What animal barks?', 'answer': 'dog'},
            {'question': 'What do bees make?', 'answer': 'honey'},
            {
                'question': 'What do people drink when they are thirsty?',
                'answer': 'water',
            },
            {
                'question': 'What season comes after winter?',
                'answer': 'spring',
            },
            {'question': 'What shape has three sides?', 'answer': 'triangle'},
            {
                'question': 'What fruit is usually yellow and curved?',
                'answer': 'banana',
            },
            {
                'question': 'What color are most leaves in summer?',
                'answer': 'green',
            },
            {
                'question': 'What do you use to write on paper?',
                'answer': 'pen',
            },
            {'question': 'What do you wear on your feet?', 'answer': 'shoes'},
            {'question': 'What planet do humans live on?', 'answer': 'Earth'},
            {'question': 'What is frozen water called?', 'answer': 'ice'},
            {'question': 'What do birds use to fly?', 'answer': 'wings'},
            {'question': 'What organ pumps blood?', 'answer': 'heart'},
            {'question': 'What sense uses the eyes?', 'answer': 'sight'},
            {
                'question': 'What shape has four equal sides?',
                'answer': 'square',
            },
            {'question': 'What star gives Earth light?', 'answer': 'Sun'},
            {'question': 'What color is snow?', 'answer': 'white'},
        ],
    },
    'two_words': {
        'prompt_templates': [
            'Answer in exactly two words:\n{question}',
            'Use exactly two words to answer:\n{question}',
            '{question}\nAnswer in exactly two words.',
            'Answer with exactly two words: {question}',
            'Give a two-word answer: {question}',
        ],
        'examples': [
            {'question': 'What do cats say?', 'answer': 'cats meow'},
            {'question': 'What do dogs do?', 'answer': 'dogs bark'},
            {'question': 'What do birds do?', 'answer': 'birds fly'},
            {'question': 'What do fish do?', 'answer': 'fish swim'},
            {'question': 'What does rain do?', 'answer': 'rain falls'},
            {'question': 'What do clocks do?', 'answer': 'clocks tick'},
            {'question': 'What do plants do?', 'answer': 'plants grow'},
            {'question': 'What does snow do?', 'answer': 'snow falls'},
            {'question': 'What does fire do?', 'answer': 'fire burns'},
            {'question': 'What do books do?', 'answer': 'books teach'},
            {'question': 'What does water do?', 'answer': 'water flows'},
            {'question': 'What do students do?', 'answer': 'students learn'},
        ],
    },
    'three_words': {
        'prompt_templates': [
            'Answer in exactly three words:\n{question}',
            'Use exactly three words to answer:\n{question}',
            '{question}\nAnswer in exactly three words.',
            'Answer with exactly three words: {question}',
            'Give a three-word answer: {question}',
        ],
        'examples': [
            {'question': 'What color is grass?', 'answer': 'grass is green'},
            {'question': 'What do bees make?', 'answer': 'bees make honey'},
            {'question': 'How does fire feel?', 'answer': 'fire feels hot'},
            {'question': 'How does ice feel?', 'answer': 'ice feels cold'},
            {'question': 'What do books do?', 'answer': 'books teach ideas'},
            {
                'question': 'What do plants need?',
                'answer': 'plants need water',
            },
            {
                'question': 'Why do people use umbrellas?',
                'answer': 'to stay dry',
            },
            {
                'question': 'What do libraries contain?',
                'answer': 'books and information',
            },
            {'question': 'What do maps show?', 'answer': 'maps show places'},
            {
                'question': 'Why do people sleep?',
                'answer': 'sleep restores energy',
            },
            {
                'question': 'What do teachers do?',
                'answer': 'teachers explain lessons',
            },
            {
                'question': 'What do phones need?',
                'answer': 'phones need power',
            },
        ],
    },
    'four_words': {
        'prompt_templates': [
            'Answer in exactly four words:\n{question}',
            'Use exactly four words to answer:\n{question}',
            '{question}\nAnswer in exactly four words.',
            'Answer with exactly four words: {question}',
            'Give a four-word answer: {question}',
        ],
        'examples': [
            {
                'question': 'What do bees make?',
                'answer': 'bees make sweet honey',
            },
            {
                'question': 'What do plants need?',
                'answer': 'plants need bright sunlight',
            },
            {
                'question': 'Why drink water?',
                'answer': 'water keeps people hydrated',
            },
            {
                'question': 'Why exercise?',
                'answer': 'exercise supports good health',
            },
            {'question': 'Why sleep?', 'answer': 'sleep helps bodies recover'},
            {
                'question': 'What does music do?',
                'answer': 'music can lift moods',
            },
            {
                'question': 'Why use umbrellas?',
                'answer': 'umbrellas block falling rain',
            },
            {'question': 'Why read books?', 'answer': 'books teach new ideas'},
            {
                'question': 'Why practice?',
                'answer': 'practice builds useful skills',
            },
            {
                'question': 'What do maps show?',
                'answer': 'maps show helpful directions',
            },
            {
                'question': 'Why wash hands?',
                'answer': 'washing hands removes germs',
            },
            {
                'question': 'Why save money?',
                'answer': 'saving money helps later',
            },
        ],
    },
    'five_words': {
        'prompt_templates': [
            'Answer in exactly five words:\n{question}',
            'Use exactly five words to answer:\n{question}',
            '{question}\nAnswer in exactly five words.',
            'Answer with exactly five words: {question}',
            'Give a five-word answer: {question}',
        ],
        'examples': [
            {
                'question': 'Why do people use umbrellas?',
                'answer': 'people use umbrellas for rain',
            },
            {
                'question': 'Why do people read books?',
                'answer': 'people read books to learn',
            },
            {
                'question': 'Why do phones need charging?',
                'answer': 'phones need power to work',
            },
            {
                'question': 'What do plants need to grow?',
                'answer': 'plants need sun and water',
            },
            {
                'question': 'Why is exercise useful?',
                'answer': 'exercise helps keep people healthy',
            },
            {
                'question': 'Why do people save money?',
                'answer': 'people save money for later',
            },
            {
                'question': 'What does a map show?',
                'answer': 'maps help people find places',
            },
            {
                'question': 'Why is sleep important?',
                'answer': 'sleep helps the body recover',
            },
            {
                'question': 'Why is rain useful?',
                'answer': 'rain gives water to plants',
            },
            {
                'question': 'What does a calendar show?',
                'answer': 'calendars show dates and events',
            },
            {
                'question': 'Why do students take notes?',
                'answer': 'notes help students remember ideas',
            },
            {
                'question': 'Why do people brush teeth?',
                'answer': 'brushing teeth helps prevent cavities',
            },
        ],
    },
    'six_words': {
        'prompt_templates': [
            'Answer in exactly six words:\n{question}',
            'Use exactly six words to answer:\n{question}',
            '{question}\nAnswer in exactly six words.',
            'Answer with exactly six words: {question}',
            'Give a six-word answer: {question}',
        ],
        'examples': [
            {
                'question': 'Why do people wear coats?',
                'answer': 'people wear coats to stay warm',
            },
            {
                'question': 'What does a keyboard do?',
                'answer': 'a keyboard helps people type words',
            },
            {
                'question': 'Why is rain useful?',
                'answer': 'rain gives plants water to grow',
            },
            {
                'question': 'What does a calendar show?',
                'answer': 'a calendar shows days and months',
            },
            {
                'question': 'Why is sleep useful?',
                'answer': 'good sleep can improve your focus',
            },
            {
                'question': 'What does a map do?',
                'answer': 'a map helps people find places',
            },
            {
                'question': 'Why do people use passwords?',
                'answer': 'passwords help protect private information online',
            },
            {
                'question': 'Why do people wear helmets?',
                'answer': 'helmets help protect heads from injury',
            },
            {
                'question': 'Why do people wash fruit?',
                'answer': 'washing fruit removes dirt and germs',
            },
            {
                'question': 'Why do people charge phones?',
                'answer': 'charging gives phones power to work',
            },
        ],
    },
    'seven_words': {
        'prompt_templates': [
            'Answer in exactly seven words:\n{question}',
            'Use exactly seven words to answer:\n{question}',
            '{question}\nAnswer in exactly seven words.',
            'Answer with exactly seven words: {question}',
            'Give a seven-word answer: {question}',
        ],
        'examples': [
            {
                'question': 'Why do people use umbrellas?',
                'answer': 'umbrellas help people stay dry in rain',
            },
            {
                'question': 'What does a map help with?',
                'answer': 'a map helps people find new places',
            },
            {
                'question': 'Why are notes useful?',
                'answer': 'good notes help students remember key ideas',
            },
            {
                'question': 'How do plants make food?',
                'answer': 'plants use sunlight to make their food',
            },
            {
                'question': 'Why is practice useful?',
                'answer': 'practice helps people improve difficult new skills',
            },
            {
                'question': 'What does a library provide?',
                'answer': 'libraries give people access to many books',
            },
            {
                'question': 'Why do people learn arithmetic?',
                'answer': 'arithmetic helps people solve everyday number problems',
            },
            {
                'question': 'Why do people use calendars?',
                'answer': 'calendars help people remember dates and events',
            },
            {
                'question': 'Why do people save documents?',
                'answer': 'saving documents prevents losing important written work',
            },
            {
                'question': 'Why do people drink water?',
                'answer': 'drinking water helps the body stay healthy',
            },
        ],
    },
}
