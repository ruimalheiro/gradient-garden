YES_NO_FIXTURES = {
    'default': {
        'messages': [
            {
                'role': 'user',
                'content': 'Answer with only yes or no: {question}',
            },
            {
                'role': 'assistant',
                'content': '{answer}',
            },
        ],
        'examples': [
            {
                'question': 'Is Paris the capital of France?',
                'answer': 'Yes',
            },
            {
                'question': 'Is London the capital of Portugal?',
                'answer': 'No',
            },
            {
                'question': 'Is water a liquid at room temperature?',
                'answer': 'Yes',
            },
            {
                'question': 'Do birds usually have feathers?',
                'answer': 'Yes',
            },
            {
                'question': 'Can cats usually fly?',
                'answer': 'No',
            },
            {
                'question': 'Is the sun a star?',
                'answer': 'Yes',
            },
            {
                'question': 'Is fire usually cold?',
                'answer': 'No',
            },
            {
                'question': 'Is two greater than five?',
                'answer': 'No',
            },
            {
                'question': 'Is ten greater than three?',
                'answer': 'Yes',
            },
            {
                'question': 'Is a triangle a shape?',
                'answer': 'Yes',
            },
            {
                'question': 'Is a banana usually blue?',
                'answer': 'No',
            },
            {
                'question': 'Can people read books?',
                'answer': 'Yes',
            },
            {
                'question': 'Is snow made of fire?',
                'answer': 'No',
            },
            {
                'question': 'Does a standard hour have sixty minutes?',
                'answer': 'Yes',
            },
            {
                'question': 'Is the moon larger than Earth?',
                'answer': 'No',
            },
        ],
    },
}
