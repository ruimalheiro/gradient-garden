SENTENCE_TRANSFORM_FIXTURES = {
    'question_statement': {
        'prompt_templates': [
            'Turn this into a question:\n{sentence}\nOnly provide the question.',
            'Turn this statement into a question:\n{sentence}\nOnly provide the question.',
            'Rewrite this as a question:\n{sentence}\nOnly output the question.',
            'Change this sentence into a question:\n{sentence}\nDo not explain your answer.',
            'Make this a question:\n{sentence}\nOnly provide the question.',
        ],
        'examples': [
            {
                'sentence': 'You are coming to dinner.',
                'answer': 'Are you coming to dinner?',
            },
            {
                'sentence': 'She likes coffee.',
                'answer': 'Does she like coffee?',
            },
            {'sentence': 'They are ready.', 'answer': 'Are they ready?'},
            {'sentence': 'He can swim.', 'answer': 'Can he swim?'},
            {
                'sentence': 'The meeting starts at noon.',
                'answer': 'Does the meeting start at noon?',
            },
            {
                'sentence': 'You finished the report.',
                'answer': 'Did you finish the report?',
            },
            {
                'sentence': 'Maria is at school.',
                'answer': 'Is Maria at school?',
            },
            {
                'sentence': 'The train leaves soon.',
                'answer': 'Does the train leave soon?',
            },
            {
                'sentence': 'They can join the call.',
                'answer': 'Can they join the call?',
            },
            {'sentence': 'He likes apples.', 'answer': 'Does he like apples?'},
            {'sentence': 'The door is open.', 'answer': 'Is the door open?'},
            {
                'sentence': 'You have the notes.',
                'answer': 'Do you have the notes?',
            },
            {
                'sentence': 'She finished the task.',
                'answer': 'Did she finish the task?',
            },
            {
                'sentence': 'The class begins tomorrow.',
                'answer': 'Does the class begin tomorrow?',
            },
            {'sentence': 'They were late.', 'answer': 'Were they late?'},
            {
                'sentence': 'The dog is outside.',
                'answer': 'Is the dog outside?',
            },
            {'sentence': 'You want tea.', 'answer': 'Do you want tea?'},
            {'sentence': 'He needs help.', 'answer': 'Does he need help?'},
            {
                'sentence': 'The package arrived.',
                'answer': 'Did the package arrive?',
            },
            {'sentence': 'She can drive.', 'answer': 'Can she drive?'},
        ],
    },
    'statement_question': {
        'prompt_templates': [
            'Turn this into a statement:\n{sentence}\nOnly provide the statement.',
            'Turn this question into a statement:\n{sentence}\nOnly provide the statement.',
            'Rewrite this as a statement:\n{sentence}\nOnly output the statement.',
            'Change this question into a statement:\n{sentence}\nDo not explain your answer.',
            'Make this a statement:\n{sentence}\nOnly provide the statement.',
        ],
        'examples': [
            {
                'sentence': 'Are you coming to dinner?',
                'answer': 'You are coming to dinner.',
            },
            {
                'sentence': 'Does she like coffee?',
                'answer': 'She likes coffee.',
            },
            {'sentence': 'Are they ready?', 'answer': 'They are ready.'},
            {'sentence': 'Can he swim?', 'answer': 'He can swim.'},
            {
                'sentence': 'Does the meeting start at noon?',
                'answer': 'The meeting starts at noon.',
            },
            {
                'sentence': 'Did you finish the report?',
                'answer': 'You finished the report.',
            },
            {
                'sentence': 'Is Maria at school?',
                'answer': 'Maria is at school.',
            },
            {
                'sentence': 'Does the train leave soon?',
                'answer': 'The train leaves soon.',
            },
            {
                'sentence': 'Can they join the call?',
                'answer': 'They can join the call.',
            },
            {'sentence': 'Does he like apples?', 'answer': 'He likes apples.'},
            {'sentence': 'Is the door open?', 'answer': 'The door is open.'},
            {
                'sentence': 'Do you have the notes?',
                'answer': 'You have the notes.',
            },
            {
                'sentence': 'Did she finish the task?',
                'answer': 'She finished the task.',
            },
            {
                'sentence': 'Does the class begin tomorrow?',
                'answer': 'The class begins tomorrow.',
            },
            {'sentence': 'Were they late?', 'answer': 'They were late.'},
        ],
    },
    'tense': {
        'prompt_templates': [
            'Change this sentence to past tense:\n{present}\nOnly provide the changed sentence.',
            'Rewrite this in past tense:\n{present}\nOnly output the changed sentence.',
            'Change this sentence from present tense to past tense:\n{present}\nDo not explain your answer.',
        ],
        'examples': [
            {
                'present': 'They walk to school.',
                'answer': 'They walked to school.',
            },
            {
                'present': 'She opens the door.',
                'answer': 'She opened the door.',
            },
            {'present': 'I cook dinner.', 'answer': 'I cooked dinner.'},
            {
                'present': 'The dog runs outside.',
                'answer': 'The dog ran outside.',
            },
            {'present': 'He writes a letter.', 'answer': 'He wrote a letter.'},
            {
                'present': 'Maria reads the book.',
                'answer': 'Maria read the book.',
            },
            {'present': 'They play soccer.', 'answer': 'They played soccer.'},
            {'present': 'She drinks water.', 'answer': 'She drank water.'},
            {
                'present': 'The child draws a picture.',
                'answer': 'The child drew a picture.',
            },
            {
                'present': 'We visit the museum.',
                'answer': 'We visited the museum.',
            },
            {
                'present': 'He carries the bag.',
                'answer': 'He carried the bag.',
            },
            {
                'present': 'The teacher explains the lesson.',
                'answer': 'The teacher explained the lesson.',
            },
        ],
    },
    'present_tense': {
        'prompt_templates': [
            'Change this sentence to present tense:\n{past}\nOnly provide the changed sentence.',
            'Rewrite this in present tense:\n{past}\nOnly output the changed sentence.',
            'Change this sentence from past tense to present tense:\n{past}\nDo not explain your answer.',
        ],
        'examples': [
            {
                'past': 'They walked to school.',
                'answer': 'They walk to school.',
            },
            {'past': 'She opened the door.', 'answer': 'She opens the door.'},
            {'past': 'I cooked dinner.', 'answer': 'I cook dinner.'},
            {
                'past': 'The dog ran outside.',
                'answer': 'The dog runs outside.',
            },
            {'past': 'He wrote a letter.', 'answer': 'He writes a letter.'},
            {
                'past': 'Maria read the book.',
                'answer': 'Maria reads the book.',
            },
            {'past': 'They played soccer.', 'answer': 'They play soccer.'},
            {'past': 'She drank water.', 'answer': 'She drinks water.'},
            {
                'past': 'The child drew a picture.',
                'answer': 'The child draws a picture.',
            },
            {
                'past': 'We visited the museum.',
                'answer': 'We visit the museum.',
            },
        ],
    },
    'number': {
        'prompt_templates': [
            'Change this sentence to plural:\n{singular}\nOnly provide the changed sentence.',
            'Rewrite this sentence in plural form:\n{singular}\nOnly output the changed sentence.',
            'Make this sentence plural:\n{singular}\nDo not explain your answer.',
        ],
        'examples': [
            {
                'singular': 'The child is playing outside.',
                'answer': 'The children are playing outside.',
            },
            {
                'singular': 'The mouse is under the table.',
                'answer': 'The mice are under the table.',
            },
            {
                'singular': 'The box is on the shelf.',
                'answer': 'The boxes are on the shelf.',
            },
            {
                'singular': 'The dog is barking.',
                'answer': 'The dogs are barking.',
            },
            {
                'singular': 'The cat is sleeping.',
                'answer': 'The cats are sleeping.',
            },
            {
                'singular': 'The book is on the desk.',
                'answer': 'The books are on the desk.',
            },
            {
                'singular': 'The city is busy.',
                'answer': 'The cities are busy.',
            },
            {
                'singular': 'The baby is crying.',
                'answer': 'The babies are crying.',
            },
            {'singular': 'The bus is late.', 'answer': 'The buses are late.'},
            {
                'singular': 'The leaf is green.',
                'answer': 'The leaves are green.',
            },
        ],
    },
    'singular': {
        'prompt_templates': [
            'Change this sentence to singular:\n{plural}\nOnly provide the changed sentence.',
            'Rewrite this sentence in singular form:\n{plural}\nOnly output the changed sentence.',
            'Make this sentence singular:\n{plural}\nDo not explain your answer.',
        ],
        'examples': [
            {
                'plural': 'The children are playing outside.',
                'answer': 'The child is playing outside.',
            },
            {
                'plural': 'The mice are under the table.',
                'answer': 'The mouse is under the table.',
            },
            {
                'plural': 'The boxes are on the shelf.',
                'answer': 'The box is on the shelf.',
            },
            {
                'plural': 'The dogs are barking.',
                'answer': 'The dog is barking.',
            },
            {
                'plural': 'The cats are sleeping.',
                'answer': 'The cat is sleeping.',
            },
            {
                'plural': 'The books are on the desk.',
                'answer': 'The book is on the desk.',
            },
            {'plural': 'The cities are busy.', 'answer': 'The city is busy.'},
            {
                'plural': 'The babies are crying.',
                'answer': 'The baby is crying.',
            },
            {'plural': 'The buses are late.', 'answer': 'The bus is late.'},
            {
                'plural': 'The leaves are green.',
                'answer': 'The leaf is green.',
            },
        ],
    },
    'polarity': {
        'prompt_templates': [
            'Make this sentence negative:\n{positive}\nOnly provide the changed sentence.',
            'Rewrite this sentence in negative form:\n{positive}\nOnly output the changed sentence.',
            'Change this sentence to negative:\n{positive}\nDo not explain your answer.',
        ],
        'examples': [
            {'positive': 'She likes tea.', 'answer': 'She does not like tea.'},
            {'positive': 'They are ready.', 'answer': 'They are not ready.'},
            {'positive': 'He can drive.', 'answer': 'He cannot drive.'},
            {'positive': 'I want coffee.', 'answer': 'I do not want coffee.'},
            {
                'positive': 'The door is open.',
                'answer': 'The door is not open.',
            },
            {
                'positive': 'Maria finished the task.',
                'answer': 'Maria did not finish the task.',
            },
            {
                'positive': 'The dog likes food.',
                'answer': 'The dog does not like food.',
            },
            {
                'positive': 'They can join us.',
                'answer': 'They cannot join us.',
            },
            {
                'positive': 'He has a notebook.',
                'answer': 'He does not have a notebook.',
            },
            {
                'positive': 'The train arrived.',
                'answer': 'The train did not arrive.',
            },
        ],
    },
    'positive': {
        'prompt_templates': [
            'Make this sentence positive:\n{negative}\nOnly provide the changed sentence.',
            'Rewrite this sentence in positive form:\n{negative}\nOnly output the changed sentence.',
            'Change this sentence to positive:\n{negative}\nDo not explain your answer.',
        ],
        'examples': [
            {'negative': 'She does not like tea.', 'answer': 'She likes tea.'},
            {'negative': 'They are not ready.', 'answer': 'They are ready.'},
            {'negative': 'He cannot drive.', 'answer': 'He can drive.'},
            {'negative': 'I do not want coffee.', 'answer': 'I want coffee.'},
            {
                'negative': 'The door is not open.',
                'answer': 'The door is open.',
            },
            {
                'negative': 'Maria did not finish the task.',
                'answer': 'Maria finished the task.',
            },
            {
                'negative': 'The dog does not like food.',
                'answer': 'The dog likes food.',
            },
            {
                'negative': 'They cannot join us.',
                'answer': 'They can join us.',
            },
            {
                'negative': 'He does not have a notebook.',
                'answer': 'He has a notebook.',
            },
            {
                'negative': 'The train did not arrive.',
                'answer': 'The train arrived.',
            },
        ],
    },
    'style': {
        'prompt_templates': [
            'Make this sentence more formal:\n{casual}\nOnly provide the rewritten sentence.',
            'Rewrite this sentence in a more formal style:\n{casual}\nOnly output the rewritten sentence.',
            'Make this sound more formal:\n{casual}\nDo not explain your answer.',
        ],
        'examples': [
            {
                'casual': 'Can you help me out?',
                'answer': 'Could you please help me?',
            },
            {
                'casual': 'Thanks for the info.',
                'answer': 'Thank you for the information.',
            },
            {
                'casual': 'I need this soon.',
                'answer': 'I would appreciate receiving this soon.',
            },
            {
                'casual': 'Can you send it over?',
                'answer': 'Could you please send it to me?',
            },
            {
                'casual': 'Sorry for the mix-up.',
                'answer': 'I apologize for the confusion.',
            },
            {
                'casual': 'Let me know what you think.',
                'answer': 'Please let me know your thoughts.',
            },
            {
                'casual': 'I got your message.',
                'answer': 'I received your message.',
            },
            {
                'casual': 'This looks good to me.',
                'answer': 'This looks acceptable to me.',
            },
        ],
    },
    'casual_style': {
        'prompt_templates': [
            'Make this sentence more casual:\n{formal}\nOnly provide the rewritten sentence.',
            'Rewrite this sentence in a more casual style:\n{formal}\nOnly output the rewritten sentence.',
            'Make this sound more casual:\n{formal}\nDo not explain your answer.',
        ],
        'examples': [
            {
                'formal': 'Could you please help me?',
                'answer': 'Can you help me?',
            },
            {
                'formal': 'Thank you for the information.',
                'answer': 'Thanks for the info.',
            },
            {
                'formal': 'I would appreciate receiving this soon.',
                'answer': 'I need this soon.',
            },
            {
                'formal': 'Could you please send it to me?',
                'answer': 'Can you send it over?',
            },
            {
                'formal': 'I apologize for the confusion.',
                'answer': 'Sorry for the mix-up.',
            },
            {
                'formal': 'Please let me know your thoughts.',
                'answer': 'Let me know what you think.',
            },
            {
                'formal': 'I received your message.',
                'answer': 'I got your message.',
            },
            {
                'formal': 'This looks acceptable to me.',
                'answer': 'This looks good to me.',
            },
        ],
    },
    'combine_split': {
        'prompt_templates': [
            'Combine these sentences into one sentence:\n{first} {second}\nOnly provide the combined sentence.',
            'Combine these two sentences into one sentence:\n{first} {second}\nOnly output the combined sentence.',
            'Rewrite these as one sentence:\n{first} {second}\nDo not explain your answer.',
        ],
        'examples': [
            {
                'first': 'The sun was setting.',
                'second': 'The sky turned orange.',
                'answer': 'The sky turned orange as the sun was setting.',
            },
            {
                'first': 'Maria missed the bus.',
                'second': 'She walked to school.',
                'answer': 'Maria missed the bus, so she walked to school.',
            },
            {
                'first': 'The room was cold.',
                'second': 'I closed the window.',
                'answer': 'The room was cold, so I closed the window.',
            },
            {
                'first': 'The laptop was slow.',
                'second': 'Too many programs were open.',
                'answer': 'The laptop was slow because too many programs were open.',
            },
            {
                'first': 'The cake smelled sweet.',
                'second': 'Everyone wanted a slice.',
                'answer': 'The cake smelled sweet, and everyone wanted a slice.',
            },
            {
                'first': 'The rain stopped.',
                'second': 'The children went outside.',
                'answer': 'The children went outside after the rain stopped.',
            },
            {
                'first': 'The train was late.',
                'second': 'Many people waited.',
                'answer': 'Many people waited because the train was late.',
            },
            {
                'first': 'She studied hard.',
                'second': 'She passed the exam.',
                'answer': 'She passed the exam because she studied hard.',
            },
        ],
    },
    'split': {
        'prompt_templates': [
            'Split this sentence into two shorter sentences:\n{sentence}\nOnly provide the two sentences.',
            'Rewrite this as two shorter sentences:\n{sentence}\nOnly output the two sentences.',
            'Separate this into two sentences:\n{sentence}\nDo not explain your answer.',
        ],
        'examples': [
            {
                'sentence': 'The rain stopped and the children went outside to play.',
                'answer': 'The rain stopped. The children went outside to play.',
            },
            {
                'sentence': 'The laptop was slow because too many programs were open.',
                'answer': 'The laptop was slow. Too many programs were open.',
            },
            {
                'sentence': 'The cake smelled sweet and everyone wanted a slice.',
                'answer': 'The cake smelled sweet. Everyone wanted a slice.',
            },
            {
                'sentence': 'Maria missed the bus, so she walked to school.',
                'answer': 'Maria missed the bus. She walked to school.',
            },
            {
                'sentence': 'The room was cold, so I closed the window.',
                'answer': 'The room was cold. I closed the window.',
            },
            {
                'sentence': 'The sun was setting and the sky turned orange.',
                'answer': 'The sun was setting. The sky turned orange.',
            },
            {
                'sentence': 'The dog barked because someone knocked on the door.',
                'answer': 'The dog barked. Someone knocked on the door.',
            },
            {
                'sentence': 'The train was late, so many people waited.',
                'answer': 'The train was late. Many people waited.',
            },
        ],
    },
}
