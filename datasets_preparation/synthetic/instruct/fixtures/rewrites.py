REWRITE_FIXTURES = {
    'redundancy_removal': {
        'examples': [
            {
                'prompt': 'Rewrite this sentence to remove repeated meaning:\nThe result was unclear because it was not clear.\nOnly provide the rewritten sentence.',
                'answer': 'The result was unclear.',
            },
            {
                'prompt': 'Rewrite this sentence to remove repeated meaning:\nThe plan failed because it did not work.\nOnly provide the rewritten sentence.',
                'answer': 'The plan was unsuccessful.',
            },
            {
                'prompt': 'Rewrite this sentence to remove repeated meaning:\nThe answer was wrong because it was not correct.\nOnly provide the rewritten sentence.',
                'answer': 'The answer was incorrect.',
            },
            {
                'prompt': 'Rewrite this sentence to remove repeated meaning:\nThe room was cold because it was not warm.\nOnly provide the rewritten sentence.',
                'answer': 'The room was cold.',
            },
            {
                'prompt': 'Rewrite this sentence to remove repeated meaning:\nThe task was easy because it was not hard.\nOnly provide the rewritten sentence.',
                'answer': 'The task was easy.',
            },
            {
                'prompt': 'Rewrite this sentence to remove repeated meaning:\nThe test was hard because it was difficult.\nOnly provide the rewritten sentence.',
                'answer': 'The test was difficult.',
            },
            {
                'prompt': 'Rewrite this sentence to remove repeated meaning:\nThe meeting was long because it took a lot of time.\nOnly provide the rewritten sentence.',
                'answer': 'The meeting took too long.',
            },
            {
                'prompt': 'Rewrite this sentence to remove repeated meaning:\nThe food was good because it tasted nice.\nOnly provide the rewritten sentence.',
                'answer': 'The food tasted good.',
            },
            {
                'prompt': 'Rewrite this sentence to remove repeated meaning:\nThe movie was bad because it was not enjoyable.\nOnly provide the rewritten sentence.',
                'answer': 'The movie was unenjoyable.',
            },
            {
                'prompt': 'Rewrite this sentence to remove repeated meaning:\nThe instructions were confusing because they were hard to understand.\nOnly provide the rewritten sentence.',
                'answer': 'The instructions were confusing.',
            },
            {
                'prompt': 'Rewrite this sentence to remove repeated meaning:\nThe device broke because it stopped working.\nOnly provide the rewritten sentence.',
                'answer': 'The device stopped working.',
            },
            {
                'prompt': 'Rewrite this sentence to remove repeated meaning:\nThe train was late because it arrived after the expected time.\nOnly provide the rewritten sentence.',
                'answer': 'The train arrived late.',
            },
            {
                'prompt': 'Rewrite this sentence to remove repeated meaning:\nThe message was unclear because it was hard to understand.\nOnly provide the rewritten sentence.',
                'answer': 'The message was unclear.',
            },
            {
                'prompt': 'Rewrite this sentence to remove repeated meaning:\nThe road was unsafe because it was dangerous.\nOnly provide the rewritten sentence.',
                'answer': 'The road was dangerous.',
            },
            {
                'prompt': 'Rewrite this sentence to remove repeated meaning:\nThe story was funny because it made people laugh.\nOnly provide the rewritten sentence.',
                'answer': 'The story made people laugh.',
            },
        ],
    },
    'concise_rewrite': {
        'prompt_templates': [
            'Make this sentence more concise:\n{bad}\nOnly provide the revised sentence.',
            'Rewrite this sentence to be shorter:\n{bad}\nOnly provide the rewritten sentence.',
            'Make the following sentence less wordy:\n{bad}\nOnly output the revised sentence.',
            'Rewrite this sentence in fewer words:\n{bad}\nDo not explain your answer.',
            'Replace this sentence with a concise version:\n{bad}\nOnly provide the replacement sentence.',
        ],
        'examples': [
            {
                'bad': 'Due to the fact that it was raining, we decided not to go outside.',
                'answer': 'Because it was raining, we stayed inside.',
            },
            {
                'bad': 'At this point in time, we are ready to begin.',
                'answer': 'We are ready to begin now.',
            },
            {
                'bad': 'The reason I was late was because I arrived after the time.',
                'answer': 'I arrived late.',
            },
            {
                'bad': 'The reason we left was because we needed to go.',
                'answer': 'We left because we needed to go.',
            },
            {
                'bad': 'She gave a reply after a short amount of time.',
                'answer': 'She replied quickly.',
            },
            {
                'bad': 'The train arrived later than the time it was supposed to arrive.',
                'answer': 'The train arrived late.',
            },
            {
                'bad': 'He was not able to find his keys.',
                'answer': 'He could not find his keys.',
            },
            {
                'bad': 'The shop is open during the hours of the morning.',
                'answer': 'The shop is open in the morning.',
            },
            {
                'bad': 'The project was completed before the time it was due.',
                'answer': 'The project was completed before the deadline.',
            },
            {
                'bad': 'She fixed the mistake that was in the document.',
                'answer': 'She corrected the document mistake.',
            },
            {
                'bad': 'The computer was slow and took a long time to respond.',
                'answer': 'The computer responded slowly.',
            },
            {
                'bad': 'The bag was heavy because it had many books inside.',
                'answer': 'The bag was heavy with books.',
            },
            {
                'bad': 'He used his phone to send a message to his friend.',
                'answer': 'He texted his friend.',
            },
            {
                'bad': 'The water was too hot to drink right away.',
                'answer': 'The water was too hot to drink immediately.',
            },
            {
                'bad': 'The city has many buildings that are very tall.',
                'answer': 'The city has many tall buildings.',
            },
            {
                'bad': 'The cake tasted sweet and was nice to eat.',
                'answer': 'The cake was sweet and delicious.',
            },
            {
                'bad': 'The task was easy and did not take much effort.',
                'answer': 'The task was easy.',
            },
            {
                'bad': 'The message was not clear and could be misunderstood.',
                'answer': 'The message was unclear.',
            },
            {
                'bad': 'She looked at the paper carefully to find mistakes.',
                'answer': 'She reviewed the paper for mistakes.',
            },
            {
                'bad': 'The phone stopped working and would not turn on.',
                'answer': 'The phone would not turn on.',
            },
        ],
    },
    'natural_paraphrase': {
        'prompt_templates': [
            'Rewrite this sentence so it sounds more natural:\n{bad}\nOnly provide the rewritten sentence.',
            'Make this sentence sound natural:\n{bad}\nOnly provide the improved sentence.',
            'Rewrite the following sentence naturally:\n{bad}\nDo not explain your answer.',
            'Improve the wording of this sentence:\n{bad}\nOnly output the improved sentence.',
            'Rewrite this sentence in a natural way:\n{bad}\nOnly provide the rewritten sentence.',
        ],
        'examples': [
            {
                'bad': 'I am writing to tell you that I am happy about the thing.',
                'answer': 'I am happy about it.',
            },
            {
                'bad': 'I want to say that the book was something I liked.',
                'answer': 'I liked the book.',
            },
            {
                'bad': 'The thing was bad because it was not good.',
                'answer': 'The item was poor quality.',
            },
            {
                'bad': 'He went to the place where the thing happened.',
                'answer': 'He went to the scene of the event.',
            },
            {
                'bad': 'The food was nice and I liked it a lot.',
                'answer': 'I really enjoyed the food.',
            },
            {
                'bad': 'This is a thing that people use to do work.',
                'answer': 'This is a tool people use for work.',
            },
            {
                'bad': 'She was happy because the result was good.',
                'answer': 'She was pleased with the result.',
            },
            {
                'bad': 'He said the same thing again and again many times.',
                'answer': 'He repeated himself many times.',
            },
            {
                'bad': 'I need help with the problem that I am having.',
                'answer': 'I need help with my problem.',
            },
            {
                'bad': 'The movie was interesting and kept my attention.',
                'answer': 'The movie was engaging.',
            },
            {
                'bad': 'She spoke in a way that was easy to understand.',
                'answer': 'She spoke clearly.',
            },
            {
                'bad': 'The house was big and had a lot of space.',
                'answer': 'The house was spacious.',
            },
            {
                'bad': 'The dog ran fast across the field.',
                'answer': 'The dog sprinted across the field.',
            },
            {
                'bad': 'The teacher explained the idea in a simple way.',
                'answer': 'The teacher explained the idea simply.',
            },
            {
                'bad': 'The river moved slowly through the valley.',
                'answer': 'The river flowed slowly through the valley.',
            },
            {
                'bad': 'The idea was new and different from the usual ideas.',
                'answer': 'The idea was original.',
            },
            {
                'bad': 'The report includes details about what happened.',
                'answer': 'The report describes what happened.',
            },
            {
                'bad': 'She was kind and helped the person who needed help.',
                'answer': 'She kindly helped the person in need.',
            },
            {
                'bad': 'He asked a question that was important.',
                'answer': 'He asked an important question.',
            },
            {
                'bad': 'They worked together to solve the problem.',
                'answer': 'They collaborated to solve the problem.',
            },
        ],
    },
    'high_edit_distance': {
        'prompt_templates': [
            'Rewrite this sentence. Do not copy the original wording:\n{bad}\nOnly provide the rewritten sentence.',
            'Paraphrase this sentence with different wording:\n{bad}\nOnly provide the paraphrase.',
            'Rewrite this sentence using a different structure:\n{bad}\nOnly output the rewritten sentence.',
            'Replace this sentence with a clearer version that uses different wording:\n{bad}\nOnly provide the replacement sentence.',
            'Rewrite the sentence below without copying its phrasing:\n{bad}\nOnly provide the rewritten sentence.',
        ],
        'examples': [
            {
                'bad': 'The issue happened because there was a problem with the system.',
                'answer': 'A system problem caused the issue.',
            },
            {
                'bad': 'The device stopped working because it had an issue.',
                'answer': 'A problem caused the device to stop working.',
            },
            {
                'bad': 'The weather was bad because it rained all day.',
                'answer': 'All-day rain made the weather unpleasant.',
            },
            {
                'bad': 'The child was scared because the noise was loud.',
                'answer': 'The loud noise frightened the child.',
            },
            {
                'bad': 'He was tired because he did not sleep enough.',
                'answer': 'Lack of sleep left him tired.',
            },
            {
                'bad': 'The path was hard to see because it was dark.',
                'answer': 'Darkness made the path difficult to see.',
            },
            {
                'bad': 'The company made changes to make the product better.',
                'answer': 'The company improved the product.',
            },
            {
                'bad': 'The book was about a person who went on a trip.',
                'answer': 'The book followed a traveler.',
            },
            {
                'bad': 'The car made a loud sound when it started.',
                'answer': 'The car started noisily.',
            },
            {
                'bad': 'She gave me information that was useful.',
                'answer': 'She gave me useful information.',
            },
            {
                'bad': 'He made a decision very quickly without thinking much.',
                'answer': 'He made a hasty decision.',
            },
            {
                'bad': 'The room was very cold and not warm at all.',
                'answer': 'The room felt freezing.',
            },
            {
                'bad': 'The game was fun and made people excited.',
                'answer': 'The exciting game was fun for everyone.',
            },
            {
                'bad': 'The instructions were confusing and hard to understand.',
                'answer': 'The instructions were unclear.',
            },
            {
                'bad': 'The answer was not correct and had mistakes.',
                'answer': 'The answer was incorrect.',
            },
            {
                'bad': 'The meeting was long and it took a lot of time.',
                'answer': 'The meeting dragged on.',
            },
            {
                'bad': 'The plan did not work because it failed.',
                'answer': 'The plan was unsuccessful.',
            },
            {
                'bad': 'The test was hard and difficult to finish.',
                'answer': 'The test was difficult to complete.',
            },
            {
                'bad': 'The food was good because it tasted nice.',
                'answer': 'The food tasted delicious.',
            },
            {
                'bad': 'The project was not finished because the team needed more time.',
                'answer': 'The team needed more time to finish the project.',
            },
        ],
    },
    'bad_because_not_good': {
        'prompt_templates': [
            'Rewrite this sentence to be clearer:\n{bad}\nOnly provide the rewritten sentence.',
            'Rewrite this sentence without copying it:\n{bad}\nOnly provide the rewritten sentence.',
            'Replace this weak sentence with a clearer version:\n{bad}\nOnly provide the replacement sentence.',
            'Rewrite this sentence to remove vague wording:\n{bad}\nOnly output the rewritten sentence.',
            'Improve this sentence so it sounds natural:\n{bad}\nOnly provide the improved sentence.',
        ],
        'examples': [
            {
                'bad': 'The thing was bad because it was not good.',
                'answer': 'The item was poor quality.',
            },
            {
                'bad': 'The movie was bad because it was not good.',
                'answer': 'The movie was poor.',
            },
            {
                'bad': 'The food was bad because it was not good.',
                'answer': 'The food tasted unpleasant.',
            },
            {
                'bad': 'The answer was bad because it was not good.',
                'answer': 'The answer was poor.',
            },
            {
                'bad': 'The idea was bad because it was not good.',
                'answer': 'The idea was weak.',
            },
            {
                'bad': 'The design was bad because it was not good.',
                'answer': 'The design was poor.',
            },
            {
                'bad': 'The result was bad because it was not good.',
                'answer': 'The result was disappointing.',
            },
            {
                'bad': 'The service was bad because it was not good.',
                'answer': 'The service was poor.',
            },
            {
                'bad': 'The explanation was bad because it was not good.',
                'answer': 'The explanation was unclear.',
            },
            {
                'bad': 'The performance was bad because it was not good.',
                'answer': 'The performance was poor.',
            },
            {
                'bad': 'The plan was bad because it was not good.',
                'answer': 'The plan was weak.',
            },
            {
                'bad': 'The writing was bad because it was not good.',
                'answer': 'The writing was poor.',
            },
            {
                'bad': 'The app was bad because it was not good.',
                'answer': 'The app was poorly made.',
            },
            {
                'bad': 'The lesson was bad because it was not good.',
                'answer': 'The lesson was ineffective.',
            },
            {
                'bad': 'The meeting was bad because it was not good.',
                'answer': 'The meeting was unproductive.',
            },
            {
                'bad': 'The tool was bad because it was not good.',
                'answer': 'The tool was poorly designed.',
            },
            {
                'bad': 'The choice was bad because it was not good.',
                'answer': 'The choice was unwise.',
            },
            {
                'bad': 'The experience was bad because it was not good.',
                'answer': 'The experience was unpleasant.',
            },
            {
                'bad': 'The code was bad because it was not good.',
                'answer': 'The code was poorly written.',
            },
            {
                'bad': 'The response was bad because it was not good.',
                'answer': 'The response was poor.',
            },
        ],
    },
}
