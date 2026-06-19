TEXT_CLASSIFICATION_FIXTURES = {
    'sentiment': {
        'examples': [
            {
                'prompt': 'Classify the sentiment as positive, negative, or neutral:\nI loved the movie.\nOnly provide the label.',
                'answer': 'positive',
            },
            {
                'prompt': 'Classify the sentiment as positive, negative, or neutral:\nThe package arrived yesterday.\nOnly provide the label.',
                'answer': 'neutral',
            },
            {
                'prompt': 'Classify the sentiment as positive, negative, or neutral:\nThe service was slow and rude.\nOnly provide the label.',
                'answer': 'negative',
            },
            {
                'prompt': 'Classify the sentiment as positive, negative, or neutral:\nThat was a wonderful surprise.\nOnly provide the label.',
                'answer': 'positive',
            },
            {
                'prompt': 'Classify the sentiment as positive, negative, or neutral:\nThe meeting starts at noon.\nOnly provide the label.',
                'answer': 'neutral',
            },
            {
                'prompt': 'Classify the sentiment as positive, negative, or neutral:\nI am disappointed with the result.\nOnly provide the label.',
                'answer': 'negative',
            },
            {
                'prompt': 'Classify the sentiment as positive, negative, or neutral:\nThis cake tastes amazing.\nOnly provide the label.',
                'answer': 'positive',
            },
            {
                'prompt': 'Classify the sentiment as positive, negative, or neutral:\nThe book is on the table.\nOnly provide the label.',
                'answer': 'neutral',
            },
            {
                'prompt': 'Classify the sentiment as positive, negative, or neutral:\nThe app keeps crashing.\nOnly provide the label.',
                'answer': 'negative',
            },
            {
                'prompt': 'Classify the sentiment as positive, negative, or neutral:\nI really enjoyed the concert.\nOnly provide the label.',
                'answer': 'positive',
            },
        ],
    },

    'topic': {
        'examples': [
            {
                'prompt': 'Classify the topic as food, travel, sports, or technology:\nThe laptop battery charges quickly.\nOnly provide the label.',
                'answer': 'technology',
            },
            {
                'prompt': 'Classify the topic as food, travel, sports, or technology:\nThe team won the final match.\nOnly provide the label.',
                'answer': 'sports',
            },
            {
                'prompt': 'Classify the topic as food, travel, sports, or technology:\nThe soup needs more salt.\nOnly provide the label.',
                'answer': 'food',
            },
            {
                'prompt': 'Classify the topic as food, travel, sports, or technology:\nThe train arrived in Lisbon.\nOnly provide the label.',
                'answer': 'travel',
            },
            {
                'prompt': 'Classify the topic as food, travel, sports, or technology:\nThe phone screen is very bright.\nOnly provide the label.',
                'answer': 'technology',
            },
            {
                'prompt': 'Classify the topic as food, travel, sports, or technology:\nThe player scored two goals.\nOnly provide the label.',
                'answer': 'sports',
            },
            {
                'prompt': 'Classify the topic as food, travel, sports, or technology:\nThe pasta is ready to serve.\nOnly provide the label.',
                'answer': 'food',
            },
            {
                'prompt': 'Classify the topic as food, travel, sports, or technology:\nThe flight leaves early tomorrow.\nOnly provide the label.',
                'answer': 'travel',
            },
            {
                'prompt': 'Classify the topic as food, travel, sports, or technology:\nThe software update fixed the bug.\nOnly provide the label.',
                'answer': 'technology',
            },
            {
                'prompt': 'Classify the topic as food, travel, sports, or technology:\nThe hotel room has a sea view.\nOnly provide the label.',
                'answer': 'travel',
            },
        ],
    },
}
