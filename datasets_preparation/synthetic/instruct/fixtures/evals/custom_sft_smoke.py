CUSTOM_SFT_SMOKE_EVAL = [
    {
        'key': 'yes_no_001',
        'category': 'exact_yes_no',
        'prompt': 'Answer exactly yes or no: Is the sky usually blue on a clear day?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['yes'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'yes_no_002',
        'category': 'exact_yes_no',
        'prompt': 'Answer exactly yes or no: Is 9 smaller than 4?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['no'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'yes_no_003',
        'category': 'exact_yes_no',
        'prompt': 'Answer exactly yes or no: Can a triangle have three sides?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['yes'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'yes_no_004',
        'category': 'exact_yes_no',
        'prompt': 'Answer exactly yes or no: Is ice usually hot?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['no'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'yes_no_005',
        'category': 'exact_yes_no',
        'prompt': 'Answer exactly yes or no: Does a week have seven days?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['yes'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'yes_no_006',
        'category': 'exact_yes_no',
        'prompt': 'Answer exactly yes or no: Is the letter B a vowel?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['no'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'yes_no_007',
        'category': 'exact_yes_no',
        'prompt': 'Answer exactly yes or no: Is 12 an even number?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['yes'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'yes_no_008',
        'category': 'exact_yes_no',
        'prompt': 'Answer exactly yes or no: Can fish live underwater?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['yes'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'yes_no_009',
        'category': 'exact_yes_no',
        'prompt': 'Answer exactly yes or no: Is midnight the same as noon?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['no'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'yes_no_010',
        'category': 'exact_yes_no',
        'prompt': 'Answer exactly yes or no: Is a square a type of rectangle?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['yes'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'one_word_001',
        'category': 'one_word',
        'prompt': 'Answer with exactly one word: What color is fresh snow usually?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['white'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'one_word_002',
        'category': 'one_word',
        'prompt': 'Answer with exactly one word: What animal says meow?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['cat'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'one_word_003',
        'category': 'one_word',
        'prompt': 'Answer with exactly one word: What do bees make?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['honey'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'one_word_004',
        'category': 'one_word',
        'prompt': 'Answer with exactly one word: What planet do humans live on?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['earth'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'one_word_005',
        'category': 'one_word',
        'prompt': 'Answer with exactly one word: What do you use to write on a chalkboard?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['chalk'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'one_word_006',
        'category': 'one_word',
        'prompt': 'Answer with exactly one word: What season comes after winter?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['spring'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'one_word_007',
        'category': 'one_word',
        'prompt': 'Answer with exactly one word: What shape has three sides?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['triangle'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'one_word_008',
        'category': 'one_word',
        'prompt': 'Answer with exactly one word: What fruit is commonly used to make lemonade?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['lemon'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'one_word_009',
        'category': 'one_word',
        'prompt': 'Answer with exactly one word: What is the opposite of cold?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['hot'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'one_word_010',
        'category': 'one_word',
        'prompt': 'Answer with exactly one word: What do birds use to fly?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['wings'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'sentiment_001',
        'category': 'sentiment',
        'prompt': 'Classify the sentiment as positive, negative, or neutral: I absolutely loved the '
        'concert.',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['positive'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'sentiment_002',
        'category': 'sentiment',
        'prompt': 'Classify the sentiment as positive, negative, or neutral: The package arrived late '
        'and the box was damaged.',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['negative'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'sentiment_003',
        'category': 'sentiment',
        'prompt': 'Classify the sentiment as positive, negative, or neutral: The meeting starts at 3 PM.',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['neutral'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'sentiment_004',
        'category': 'sentiment',
        'prompt': 'Classify the sentiment as positive, negative, or neutral: This was the best meal I '
        'have had all week.',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['positive'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'sentiment_005',
        'category': 'sentiment',
        'prompt': 'Classify the sentiment as positive, negative, or neutral: I am disappointed with the '
        'poor service.',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['negative'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'sentiment_006',
        'category': 'sentiment',
        'prompt': 'Classify the sentiment as positive, negative, or neutral: The report contains five '
        'sections.',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['neutral'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'sentiment_007',
        'category': 'sentiment',
        'prompt': 'Classify the sentiment as positive, negative, or neutral: The update made the app '
        'faster and easier to use.',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['positive'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'sentiment_008',
        'category': 'sentiment',
        'prompt': 'Classify the sentiment as positive, negative, or neutral: I regret buying this noisy '
        'vacuum cleaner.',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['negative'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'sentiment_009',
        'category': 'sentiment',
        'prompt': 'Classify the sentiment as positive, negative, or neutral: The door is closed.',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['neutral'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'sentiment_010',
        'category': 'sentiment',
        'prompt': 'Classify the sentiment as positive, negative, or neutral: I am thrilled with the '
        'final result.',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['positive'], 'normalize': ['strip', 'lower', 'strip_punct']},
            {},
            {},
        ],
    },
    {
        'key': 'simple_math_001',
        'category': 'simple_math',
        'prompt': 'Answer with only the number: What is 17 + 25?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [{'targets': ['42'], 'normalize': ['strip', 'strip_punct']}, {}, {}],
    },
    {
        'key': 'simple_math_002',
        'category': 'simple_math',
        'prompt': 'Answer with only the number: What is 9 * 6?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [{'targets': ['54'], 'normalize': ['strip', 'strip_punct']}, {}, {}],
    },
    {
        'key': 'simple_math_003',
        'category': 'simple_math',
        'prompt': 'Answer with only the number: What is 100 - 37?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [{'targets': ['63'], 'normalize': ['strip', 'strip_punct']}, {}, {}],
    },
    {
        'key': 'simple_math_004',
        'category': 'simple_math',
        'prompt': 'Answer with only the number: What is 81 / 9?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [{'targets': ['9'], 'normalize': ['strip', 'strip_punct']}, {}, {}],
    },
    {
        'key': 'simple_math_005',
        'category': 'simple_math',
        'prompt': 'Answer with only the number: What is 14 + 8 + 3?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [{'targets': ['25'], 'normalize': ['strip', 'strip_punct']}, {}, {}],
    },
    {
        'key': 'simple_math_006',
        'category': 'simple_math',
        'prompt': 'Answer with only the number: What is 7 * 8?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [{'targets': ['56'], 'normalize': ['strip', 'strip_punct']}, {}, {}],
    },
    {
        'key': 'simple_math_007',
        'category': 'simple_math',
        'prompt': 'Answer with only the number: What is 45 - 19?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [{'targets': ['26'], 'normalize': ['strip', 'strip_punct']}, {}, {}],
    },
    {
        'key': 'simple_math_008',
        'category': 'simple_math',
        'prompt': 'Answer with only the number: What is 12 * 4?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [{'targets': ['48'], 'normalize': ['strip', 'strip_punct']}, {}, {}],
    },
    {
        'key': 'simple_math_009',
        'category': 'simple_math',
        'prompt': 'Answer with only the number: What is 72 / 8?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [{'targets': ['9'], 'normalize': ['strip', 'strip_punct']}, {}, {}],
    },
    {
        'key': 'simple_math_010',
        'category': 'simple_math',
        'prompt': 'Answer with only the number: What is 30 + 15 - 5?',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [{'targets': ['40'], 'normalize': ['strip', 'strip_punct']}, {}, {}],
    },
    {
        'key': 'grammar_correction_001',
        'category': 'grammar_correction',
        'prompt': 'Correct the grammar only: She go to school yesterday.',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['She went to school yesterday.'], 'normalize': ['strip']},
            {},
            {},
        ],
    },
    {
        'key': 'grammar_correction_002',
        'category': 'grammar_correction',
        'prompt': 'Correct the grammar only: They was playing outside.',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['They were playing outside.'], 'normalize': ['strip']},
            {},
            {},
        ],
    },
    {
        'key': 'grammar_correction_003',
        'category': 'grammar_correction',
        'prompt': 'Correct the grammar only: I has a red bicycle.',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['I have a red bicycle.'], 'normalize': ['strip']},
            {},
            {},
        ],
    },
    {
        'key': 'grammar_correction_004',
        'category': 'grammar_correction',
        'prompt': "Correct the grammar only: He don't like carrots.",
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {
                'targets': ["He doesn't like carrots.", 'He does not like carrots.'],
                'normalize': ['strip'],
            },
            {},
            {},
        ],
    },
    {
        'key': 'grammar_correction_005',
        'category': 'grammar_correction',
        'prompt': 'Correct the grammar only: We is ready for the test.',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['We are ready for the test.'], 'normalize': ['strip']},
            {},
            {},
        ],
    },
    {
        'key': 'grammar_correction_006',
        'category': 'grammar_correction',
        'prompt': 'Correct the grammar only: The cats is sleeping.',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['The cats are sleeping.'], 'normalize': ['strip']},
            {},
            {},
        ],
    },
    {
        'key': 'grammar_correction_007',
        'category': 'grammar_correction',
        'prompt': 'Correct the grammar only: Her and I went to the store.',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['She and I went to the store.'], 'normalize': ['strip']},
            {},
            {},
        ],
    },
    {
        'key': 'grammar_correction_008',
        'category': 'grammar_correction',
        'prompt': 'Correct the grammar only: This are my favorite shoes.',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['These are my favorite shoes.'], 'normalize': ['strip']},
            {},
            {},
        ],
    },
    {
        'key': 'grammar_correction_009',
        'category': 'grammar_correction',
        'prompt': 'Correct the grammar only: I seen that movie before.',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {
                'targets': [
                    'I have seen that movie before.',
                    'I saw that movie before.',
                ],
                'normalize': ['strip'],
            },
            {},
            {},
        ],
    },
    {
        'key': 'grammar_correction_010',
        'category': 'grammar_correction',
        'prompt': 'Correct the grammar only: The book belong to Maria.',
        'instruction_id_list': ['exact_match', 'non_empty', 'no_role_leak'],
        'kwargs': [
            {'targets': ['The book belongs to Maria.'], 'normalize': ['strip']},
            {},
            {},
        ],
    },
    {
        'key': 'comma_list_001',
        'category': 'comma_list',
        'prompt': 'List exactly 3 fruits separated by commas. Do not number them.',
        'instruction_id_list': ['comma_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 3}, {}, {}],
    },
    {
        'key': 'comma_list_002',
        'category': 'comma_list',
        'prompt': 'List exactly 4 colors separated by commas. Do not add any extra text.',
        'instruction_id_list': ['comma_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 4}, {}, {}],
    },
    {
        'key': 'comma_list_003',
        'category': 'comma_list',
        'prompt': 'List exactly 5 animals separated by commas. Do not use bullet points.',
        'instruction_id_list': ['comma_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 5}, {}, {}],
    },
    {
        'key': 'comma_list_004',
        'category': 'comma_list',
        'prompt': 'List exactly 3 programming languages separated by commas. Do not number them.',
        'instruction_id_list': ['comma_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 3}, {}, {}],
    },
    {
        'key': 'comma_list_005',
        'category': 'comma_list',
        'prompt': 'List exactly 4 kitchen tools separated by commas. Do not add a sentence.',
        'instruction_id_list': ['comma_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 4}, {}, {}],
    },
    {
        'key': 'comma_list_006',
        'category': 'comma_list',
        'prompt': 'List exactly 5 countries separated by commas. Do not use bullet points.',
        'instruction_id_list': ['comma_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 5}, {}, {}],
    },
    {
        'key': 'comma_list_007',
        'category': 'comma_list',
        'prompt': 'List exactly 3 musical instruments separated by commas. Do not number them.',
        'instruction_id_list': ['comma_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 3}, {}, {}],
    },
    {
        'key': 'comma_list_008',
        'category': 'comma_list',
        'prompt': 'List exactly 4 sports separated by commas. Do not add any extra text.',
        'instruction_id_list': ['comma_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 4}, {}, {}],
    },
    {
        'key': 'comma_list_009',
        'category': 'comma_list',
        'prompt': 'List exactly 5 vegetables separated by commas. Do not use bullet points.',
        'instruction_id_list': ['comma_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 5}, {}, {}],
    },
    {
        'key': 'comma_list_010',
        'category': 'comma_list',
        'prompt': 'List exactly 3 school subjects separated by commas. Do not add a sentence.',
        'instruction_id_list': ['comma_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 3}, {}, {}],
    },
    {
        'key': 'numbered_list_001',
        'category': 'numbered_list',
        'prompt': 'Give exactly 3 numbered steps for brushing teeth. Keep each step short.',
        'instruction_id_list': ['numbered_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 3}, {}, {}],
    },
    {
        'key': 'numbered_list_002',
        'category': 'numbered_list',
        'prompt': 'Give exactly 4 numbered steps for making tea. Keep each step short.',
        'instruction_id_list': ['numbered_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 4}, {}, {}],
    },
    {
        'key': 'numbered_list_003',
        'category': 'numbered_list',
        'prompt': 'Give exactly 3 numbered tips for staying organized. Keep each tip short.',
        'instruction_id_list': ['numbered_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 3}, {}, {}],
    },
    {
        'key': 'numbered_list_004',
        'category': 'numbered_list',
        'prompt': 'Give exactly 5 numbered steps for washing hands. Keep each step short.',
        'instruction_id_list': ['numbered_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 5}, {}, {}],
    },
    {
        'key': 'numbered_list_005',
        'category': 'numbered_list',
        'prompt': 'Give exactly 4 numbered tips for saving money. Keep each tip short.',
        'instruction_id_list': ['numbered_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 4}, {}, {}],
    },
    {
        'key': 'numbered_list_006',
        'category': 'numbered_list',
        'prompt': 'Give exactly 3 numbered steps for planting a seed. Keep each step short.',
        'instruction_id_list': ['numbered_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 3}, {}, {}],
    },
    {
        'key': 'numbered_list_007',
        'category': 'numbered_list',
        'prompt': 'Give exactly 5 numbered steps for preparing for a test. Keep each step short.',
        'instruction_id_list': ['numbered_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 5}, {}, {}],
    },
    {
        'key': 'numbered_list_008',
        'category': 'numbered_list',
        'prompt': 'Give exactly 4 numbered rules for safe cycling. Keep each rule short.',
        'instruction_id_list': ['numbered_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 4}, {}, {}],
    },
    {
        'key': 'numbered_list_009',
        'category': 'numbered_list',
        'prompt': 'Give exactly 3 numbered ways to be polite in a meeting. Keep each item short.',
        'instruction_id_list': ['numbered_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 3}, {}, {}],
    },
    {
        'key': 'numbered_list_010',
        'category': 'numbered_list',
        'prompt': 'Give exactly 5 numbered steps for cleaning a desk. Keep each step short.',
        'instruction_id_list': ['numbered_list_count', 'non_empty', 'no_role_leak'],
        'kwargs': [{'n': 5}, {}, {}],
    },
    {
        'key': 'summarization_001',
        'category': 'summarization',
        'prompt': 'Summarize in one sentence: Mia packed her bag, walked to the train station, missed '
        'the first train, and caught the next one ten minutes later.',
        'instruction_id_list': [
            'contains_all',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [{'must_contain': ['Mia', 'train']}, {'max_words': 30}, {}, {}],
    },
    {
        'key': 'summarization_002',
        'category': 'summarization',
        'prompt': 'Summarize in one sentence: The bakery opened early, sold out of bread before noon, '
        'and decided to bake a second batch for the afternoon.',
        'instruction_id_list': [
            'contains_all',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [{'must_contain': ['bakery', 'bread']}, {'max_words': 30}, {}, {}],
    },
    {
        'key': 'summarization_003',
        'category': 'summarization',
        'prompt': 'Summarize in one sentence: Liam forgot his umbrella, got caught in the rain, and '
        'borrowed a dry jacket from his friend.',
        'instruction_id_list': [
            'contains_all',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [{'must_contain': ['Liam', 'rain']}, {'max_words': 30}, {}, {}],
    },
    {
        'key': 'summarization_004',
        'category': 'summarization',
        'prompt': 'Summarize in one sentence: The team tested the new app, found two bugs, fixed them, '
        'and released the update on Friday.',
        'instruction_id_list': [
            'contains_all',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [{'must_contain': ['app', 'bugs']}, {'max_words': 30}, {}, {}],
    },
    {
        'key': 'summarization_005',
        'category': 'summarization',
        'prompt': 'Summarize in one sentence: Nora watered the plants, moved them closer to the window, '
        'and noticed new leaves a week later.',
        'instruction_id_list': [
            'contains_all',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [{'must_contain': ['Nora', 'plants']}, {'max_words': 30}, {}, {}],
    },
    {
        'key': 'summarization_006',
        'category': 'summarization',
        'prompt': 'Summarize in one sentence: The museum extended its hours because the new dinosaur '
        'exhibit attracted more visitors than expected.',
        'instruction_id_list': [
            'contains_all',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [{'must_contain': ['museum', 'dinosaur']}, {'max_words': 30}, {}, {}],
    },
    {
        'key': 'summarization_007',
        'category': 'summarization',
        'prompt': 'Summarize in one sentence: Omar saved his notes, printed the slides, and arrived '
        'early for his presentation.',
        'instruction_id_list': [
            'contains_all',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [
            {'must_contain': ['Omar', 'presentation']},
            {'max_words': 30},
            {},
            {},
        ],
    },
    {
        'key': 'summarization_008',
        'category': 'summarization',
        'prompt': 'Summarize in one sentence: The city repaired the bridge after heavy rain damaged the '
        'road and delayed traffic.',
        'instruction_id_list': [
            'contains_all',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [{'must_contain': ['city', 'bridge']}, {'max_words': 30}, {}, {}],
    },
    {
        'key': 'summarization_009',
        'category': 'summarization',
        'prompt': 'Summarize in one sentence: Ava practiced piano every evening and performed her song '
        'confidently at the school concert.',
        'instruction_id_list': [
            'contains_all',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [{'must_contain': ['Ava', 'piano']}, {'max_words': 30}, {}, {}],
    },
    {
        'key': 'summarization_010',
        'category': 'summarization',
        'prompt': 'Summarize in one sentence: The library added more study tables because students '
        'needed quiet places to work after school.',
        'instruction_id_list': [
            'contains_all',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [
            {'must_contain': ['library', 'students']},
            {'max_words': 30},
            {},
            {},
        ],
    },
    {
        'key': 'rewrite_clarity_001',
        'category': 'rewrite_clarity',
        'prompt': 'Rewrite this clearly in one sentence: The thing was kind of bad because the parts did '
        'not work together well.',
        'instruction_id_list': [
            'not_near_copy',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [
            {
                'source': 'The thing was kind of bad because the parts did not work together well.'
            },
            {'max_words': 25},
            {},
            {},
        ],
    },
    {
        'key': 'rewrite_clarity_002',
        'category': 'rewrite_clarity',
        'prompt': 'Rewrite this clearly in one sentence: I need the stuff from the place before the '
        'thing starts.',
        'instruction_id_list': [
            'not_near_copy',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [
            {'source': 'I need the stuff from the place before the thing starts.'},
            {'max_words': 25},
            {},
            {},
        ],
    },
    {
        'key': 'rewrite_clarity_003',
        'category': 'rewrite_clarity',
        'prompt': 'Rewrite this clearly in one sentence: The meeting about the project was confusing and '
        'people talked over each other.',
        'instruction_id_list': [
            'not_near_copy',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [
            {
                'source': 'The meeting about the project was confusing and people talked over each '
                'other.'
            },
            {'max_words': 25},
            {},
            {},
        ],
    },
    {
        'key': 'rewrite_clarity_004',
        'category': 'rewrite_clarity',
        'prompt': 'Rewrite this clearly in one sentence: The instructions were not good so I did not '
        'know what to do next.',
        'instruction_id_list': [
            'not_near_copy',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [
            {
                'source': 'The instructions were not good so I did not know what to do next.'
            },
            {'max_words': 25},
            {},
            {},
        ],
    },
    {
        'key': 'rewrite_clarity_005',
        'category': 'rewrite_clarity',
        'prompt': 'Rewrite this clearly in one sentence: The app is weird and sometimes it does not do '
        'the right thing.',
        'instruction_id_list': [
            'not_near_copy',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [
            {
                'source': 'The app is weird and sometimes it does not do the right thing.'
            },
            {'max_words': 25},
            {},
            {},
        ],
    },
    {
        'key': 'rewrite_clarity_006',
        'category': 'rewrite_clarity',
        'prompt': 'Rewrite this clearly in one sentence: We should fix the problem soon because it is '
        'making work harder.',
        'instruction_id_list': [
            'not_near_copy',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [
            {
                'source': 'We should fix the problem soon because it is making work harder.'
            },
            {'max_words': 25},
            {},
            {},
        ],
    },
    {
        'key': 'rewrite_clarity_007',
        'category': 'rewrite_clarity',
        'prompt': 'Rewrite this clearly in one sentence: The email was too long and I could not find the '
        'main point.',
        'instruction_id_list': [
            'not_near_copy',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [
            {'source': 'The email was too long and I could not find the main point.'},
            {'max_words': 25},
            {},
            {},
        ],
    },
    {
        'key': 'rewrite_clarity_008',
        'category': 'rewrite_clarity',
        'prompt': 'Rewrite this clearly in one sentence: The room setup was not ideal because everyone '
        'had trouble seeing the screen.',
        'instruction_id_list': [
            'not_near_copy',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [
            {
                'source': 'The room setup was not ideal because everyone had trouble seeing the '
                'screen.'
            },
            {'max_words': 25},
            {},
            {},
        ],
    },
    {
        'key': 'rewrite_clarity_009',
        'category': 'rewrite_clarity',
        'prompt': 'Rewrite this clearly in one sentence: The plan needs more detail so the team knows '
        'what to build first.',
        'instruction_id_list': [
            'not_near_copy',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [
            {
                'source': 'The plan needs more detail so the team knows what to build first.'
            },
            {'max_words': 25},
            {},
            {},
        ],
    },
    {
        'key': 'rewrite_clarity_010',
        'category': 'rewrite_clarity',
        'prompt': 'Rewrite this clearly in one sentence: The customer was upset because the delivery '
        'came late and nobody explained why.',
        'instruction_id_list': [
            'not_near_copy',
            'max_words',
            'non_empty',
            'no_role_leak',
        ],
        'kwargs': [
            {
                'source': 'The customer was upset because the delivery came late and nobody '
                'explained why.'
            },
            {'max_words': 25},
            {},
            {},
        ],
    },
    {
        'key': 'stop_role_leak_001',
        'category': 'stop_role_leak',
        'prompt': 'Write one friendly sentence thanking someone for their help.',
        'instruction_id_list': ['no_role_leak', 'max_words', 'non_empty'],
        'kwargs': [{}, {'max_words': 25}, {}],
    },
    {
        'key': 'stop_role_leak_002',
        'category': 'stop_role_leak',
        'prompt': 'Write one polite sentence asking for more time to finish a task.',
        'instruction_id_list': ['no_role_leak', 'max_words', 'non_empty'],
        'kwargs': [{}, {'max_words': 25}, {}],
    },
    {
        'key': 'stop_role_leak_003',
        'category': 'stop_role_leak',
        'prompt': 'Write one encouraging sentence for a friend who is nervous about an exam.',
        'instruction_id_list': ['no_role_leak', 'max_words', 'non_empty'],
        'kwargs': [{}, {'max_words': 25}, {}],
    },
    {
        'key': 'stop_role_leak_004',
        'category': 'stop_role_leak',
        'prompt': 'Write one concise sentence apologizing for being late.',
        'instruction_id_list': ['no_role_leak', 'max_words', 'non_empty'],
        'kwargs': [{}, {'max_words': 25}, {}],
    },
    {
        'key': 'stop_role_leak_005',
        'category': 'stop_role_leak',
        'prompt': 'Write one cheerful sentence inviting a teammate to join lunch.',
        'instruction_id_list': ['no_role_leak', 'max_words', 'non_empty'],
        'kwargs': [{}, {'max_words': 25}, {}],
    },
    {
        'key': 'stop_role_leak_006',
        'category': 'stop_role_leak',
        'prompt': 'Write one professional sentence confirming that you received a document.',
        'instruction_id_list': ['no_role_leak', 'max_words', 'non_empty'],
        'kwargs': [{}, {'max_words': 25}, {}],
    },
    {
        'key': 'stop_role_leak_007',
        'category': 'stop_role_leak',
        'prompt': 'Write one kind sentence wishing someone a quick recovery.',
        'instruction_id_list': ['no_role_leak', 'max_words', 'non_empty'],
        'kwargs': [{}, {'max_words': 25}, {}],
    },
    {
        'key': 'stop_role_leak_008',
        'category': 'stop_role_leak',
        'prompt': 'Write one brief sentence asking a colleague to review a draft.',
        'instruction_id_list': ['no_role_leak', 'max_words', 'non_empty'],
        'kwargs': [{}, {'max_words': 25}, {}],
    },
    {
        'key': 'stop_role_leak_009',
        'category': 'stop_role_leak',
        'prompt': 'Write one warm sentence congratulating someone on a promotion.',
        'instruction_id_list': ['no_role_leak', 'max_words', 'non_empty'],
        'kwargs': [{}, {'max_words': 25}, {}],
    },
    {
        'key': 'stop_role_leak_010',
        'category': 'stop_role_leak',
        'prompt': 'Write one calm sentence explaining that you need to reschedule a meeting.',
        'instruction_id_list': ['no_role_leak', 'max_words', 'non_empty'],
        'kwargs': [{}, {'max_words': 25}, {}],
    },
]
