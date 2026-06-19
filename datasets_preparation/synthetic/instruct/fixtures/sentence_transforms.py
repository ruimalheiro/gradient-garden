SENTENCE_TRANSFORM_FIXTURES = {
    'question_statement': {
        'examples': [
            {
                'prompt': 'Turn this into a question:\nYou are coming to dinner.\nOnly provide the question.',
                'answer': 'Are you coming to dinner?',
            },
            {
                'prompt': 'Turn this into a question:\nShe likes coffee.\nOnly provide the question.',
                'answer': 'Does she like coffee?',
            },
            {
                'prompt': 'Turn this into a question:\nThey are ready.\nOnly provide the question.',
                'answer': 'Are they ready?',
            },
            {
                'prompt': 'Turn this into a question:\nHe can swim.\nOnly provide the question.',
                'answer': 'Can he swim?',
            },
            {
                'prompt': 'Turn this into a question:\nThe meeting starts at noon.\nOnly provide the question.',
                'answer': 'Does the meeting start at noon?',
            },
            {
                'prompt': 'Turn this into a question:\nYou finished the report.\nOnly provide the question.',
                'answer': 'Did you finish the report?',
            },
            {
                'prompt': 'Turn this into a statement:\nAre you coming to dinner?\nOnly provide the statement.',
                'answer': 'You are coming to dinner.',
            },
            {
                'prompt': 'Turn this into a statement:\nDoes she like coffee?\nOnly provide the statement.',
                'answer': 'She likes coffee.',
            },
            {
                'prompt': 'Turn this into a statement:\nCan he swim?\nOnly provide the statement.',
                'answer': 'He can swim.',
            },
            {
                'prompt': 'Turn this into a statement:\nDid you finish the report?\nOnly provide the statement.',
                'answer': 'You finished the report.',
            },
        ],
    },

    'tense': {
        'examples': [
            {
                'prompt': 'Change this sentence to past tense:\nThey walk to school.\nOnly provide the changed sentence.',
                'answer': 'They walked to school.',
            },
            {
                'prompt': 'Change this sentence to past tense:\nShe opens the door.\nOnly provide the changed sentence.',
                'answer': 'She opened the door.',
            },
            {
                'prompt': 'Change this sentence to past tense:\nI cook dinner.\nOnly provide the changed sentence.',
                'answer': 'I cooked dinner.',
            },
            {
                'prompt': 'Change this sentence to past tense:\nThe dog runs outside.\nOnly provide the changed sentence.',
                'answer': 'The dog ran outside.',
            },
            {
                'prompt': 'Change this sentence to present tense:\nThey walked to school.\nOnly provide the changed sentence.',
                'answer': 'They walk to school.',
            },
            {
                'prompt': 'Change this sentence to present tense:\nShe opened the door.\nOnly provide the changed sentence.',
                'answer': 'She opens the door.',
            },
            {
                'prompt': 'Change this sentence to present tense:\nI cooked dinner.\nOnly provide the changed sentence.',
                'answer': 'I cook dinner.',
            },
            {
                'prompt': 'Change this sentence to present tense:\nThe dog ran outside.\nOnly provide the changed sentence.',
                'answer': 'The dog runs outside.',
            },
        ],
    },

    'number': {
        'examples': [
            {
                'prompt': 'Change this sentence to plural:\nThe child is playing outside.\nOnly provide the changed sentence.',
                'answer': 'The children are playing outside.',
            },
            {
                'prompt': 'Change this sentence to plural:\nThe mouse is under the table.\nOnly provide the changed sentence.',
                'answer': 'The mice are under the table.',
            },
            {
                'prompt': 'Change this sentence to plural:\nThe box is on the shelf.\nOnly provide the changed sentence.',
                'answer': 'The boxes are on the shelf.',
            },
            {
                'prompt': 'Change this sentence to plural:\nThe dog is barking.\nOnly provide the changed sentence.',
                'answer': 'The dogs are barking.',
            },
            {
                'prompt': 'Change this sentence to singular:\nThe children are playing outside.\nOnly provide the changed sentence.',
                'answer': 'The child is playing outside.',
            },
            {
                'prompt': 'Change this sentence to singular:\nThe mice are under the table.\nOnly provide the changed sentence.',
                'answer': 'The mouse is under the table.',
            },
            {
                'prompt': 'Change this sentence to singular:\nThe boxes are on the shelf.\nOnly provide the changed sentence.',
                'answer': 'The box is on the shelf.',
            },
        ],
    },

    'polarity': {
        'examples': [
            {
                'prompt': 'Make this sentence negative:\nShe likes tea.\nOnly provide the changed sentence.',
                'answer': 'She does not like tea.',
            },
            {
                'prompt': 'Make this sentence negative:\nThey are ready.\nOnly provide the changed sentence.',
                'answer': 'They are not ready.',
            },
            {
                'prompt': 'Make this sentence negative:\nHe can drive.\nOnly provide the changed sentence.',
                'answer': 'He cannot drive.',
            },
            {
                'prompt': 'Make this sentence positive:\nShe does not like tea.\nOnly provide the changed sentence.',
                'answer': 'She likes tea.',
            },
            {
                'prompt': 'Make this sentence positive:\nThey are not ready.\nOnly provide the changed sentence.',
                'answer': 'They are ready.',
            },
            {
                'prompt': 'Make this sentence positive:\nHe cannot drive.\nOnly provide the changed sentence.',
                'answer': 'He can drive.',
            },
        ],
    },

    'style': {
        'examples': [
            {
                'prompt': 'Make this sentence more formal:\nCan you help me out?\nOnly provide the rewritten sentence.',
                'answer': 'Could you please help me?',
            },
            {
                'prompt': 'Make this sentence more formal:\nThanks for the info.\nOnly provide the rewritten sentence.',
                'answer': 'Thank you for the information.',
            },
            {
                'prompt': 'Make this sentence more formal:\nI need this soon.\nOnly provide the rewritten sentence.',
                'answer': 'I would appreciate receiving this soon.',
            },
            {
                'prompt': 'Make this sentence more casual:\nCould you please help me?\nOnly provide the rewritten sentence.',
                'answer': 'Can you help me?',
            },
            {
                'prompt': 'Make this sentence more casual:\nThank you for the information.\nOnly provide the rewritten sentence.',
                'answer': 'Thanks for the info.',
            },
            {
                'prompt': 'Make this sentence more casual:\nI would appreciate receiving this soon.\nOnly provide the rewritten sentence.',
                'answer': 'I need this soon.',
            },
        ],
    },

    'combine_split': {
        'examples': [
            {
                'prompt': 'Combine these sentences into one sentence:\nThe sun was setting. The sky turned orange.\nOnly provide the combined sentence.',
                'answer': 'The sky turned orange as the sun was setting.',
            },
            {
                'prompt': 'Combine these sentences into one sentence:\nMaria missed the bus. She walked to school.\nOnly provide the combined sentence.',
                'answer': 'Maria missed the bus, so she walked to school.',
            },
            {
                'prompt': 'Combine these sentences into one sentence:\nThe room was cold. I closed the window.\nOnly provide the combined sentence.',
                'answer': 'The room was cold, so I closed the window.',
            },
            {
                'prompt': 'Split this sentence into two shorter sentences:\nThe rain stopped and the children went outside to play.\nOnly provide the two sentences.',
                'answer': 'The rain stopped. The children went outside to play.',
            },
            {
                'prompt': 'Split this sentence into two shorter sentences:\nThe laptop was slow because too many programs were open.\nOnly provide the two sentences.',
                'answer': 'The laptop was slow. Too many programs were open.',
            },
            {
                'prompt': 'Split this sentence into two shorter sentences:\nThe cake smelled sweet and everyone wanted a slice.\nOnly provide the two sentences.',
                'answer': 'The cake smelled sweet. Everyone wanted a slice.',
            },
        ],
    },
}
