SUMMARY_FIXTURES = {
    'one_sentence': {
        'examples': [
            {
                'prompt': 'Summarize this in one sentence:\nPenguins are birds that cannot fly but are excellent swimmers.\nOnly provide the summary.',
                'answer': 'Penguins are flightless birds that swim very well.',
            },
            {
                'prompt': 'Summarize this in one sentence:\nThe library closes at six, so we need to return the books before then.\nOnly provide the summary.',
                'answer': 'We need to return the books before the library closes.',
            },
            {
                'prompt': 'Summarize this in one sentence:\nSolar panels turn sunlight into electricity that people can use in homes and buildings.\nOnly provide the summary.',
                'answer': 'Solar panels convert sunlight into usable electricity.',
            },
            {
                'prompt': 'Summarize this in one sentence:\nMaria missed the bus, so she walked to school and arrived ten minutes late.\nOnly provide the summary.',
                'answer': 'Maria arrived late after missing the bus.',
            },
            {
                'prompt': 'Summarize this in one sentence:\nPlants need sunlight, water, and nutrients from the soil to grow.\nOnly provide the summary.',
                'answer': 'Plants need sunlight, water, and soil nutrients to grow.',
            },
            {
                'prompt': 'Summarize this in one sentence:\nThe team practiced every day and improved enough to win the final match.\nOnly provide the summary.',
                'answer': 'Daily practice helped the team win the final match.',
            },
            {
                'prompt': 'Summarize this in one sentence:\nA password manager stores your passwords securely so you do not have to remember each one.\nOnly provide the summary.',
                'answer': 'A password manager securely stores your passwords.',
            },
            {
                'prompt': 'Summarize this in one sentence:\nThe storm brought heavy rain and strong winds, causing several roads to flood.\nOnly provide the summary.',
                'answer': 'The storm caused road flooding.',
            },
            {
                'prompt': 'Summarize this in one sentence:\nExercise can strengthen muscles, improve mood, and support long-term health.\nOnly provide the summary.',
                'answer': 'Exercise improves physical and mental health.',
            },
            {
                'prompt': 'Summarize this in one sentence:\nThe new train route will make travel between the two cities faster and easier.\nOnly provide the summary.',
                'answer': 'The new route will improve intercity travel.',
            },
            {
                'prompt': 'Summarize this in one sentence:\nThe recipe uses flour, eggs, milk, and butter to make soft pancakes.\nOnly provide the summary.',
                'answer': 'The recipe makes soft pancakes from simple ingredients.',
            },
            {
                'prompt': 'Summarize this in one sentence:\nThe company delayed the product launch because it found a bug during final testing.\nOnly provide the summary.',
                'answer': 'A final testing bug delayed the product launch.',
            },
            {
                'prompt': 'Summarize this in one sentence:\nThe museum added a new exhibit about ancient tools, clothing, and daily life.\nOnly provide the summary.',
                'answer': 'The museum opened an exhibit about ancient daily life.',
            },
            {
                'prompt': 'Summarize this in one sentence:\nThe student revised her essay after receiving feedback from her teacher.\nOnly provide the summary.',
                'answer': 'The student improved her essay using teacher feedback.',
            },
            {
                'prompt': 'Summarize this in one sentence:\nThe city planted more trees to provide shade and improve air quality.\nOnly provide the summary.',
                'answer': 'The city planted trees to improve shade and air quality.',
            },
            {
                'prompt': 'Summarize this in one sentence:\nThe phone battery drained quickly because several apps were running in the background.\nOnly provide the summary.',
                'answer': 'Background apps drained the phone battery.',
            },
            {
                'prompt': 'Summarize this in one sentence:\nThe chef changed the menu after customers asked for more vegetarian options.\nOnly provide the summary.',
                'answer': 'Customer requests led the chef to add vegetarian options.',
            },
            {
                'prompt': 'Summarize this in one sentence:\nThe researcher repeated the experiment to check whether the results were reliable.\nOnly provide the summary.',
                'answer': 'The researcher repeated the experiment to verify the results.',
            },
            {
                'prompt': 'Summarize this in one sentence:\nThe school closed early because snow made the roads unsafe for buses.\nOnly provide the summary.',
                'answer': 'Snowy roads caused the school to close early.',
            },
            {
                'prompt': 'Summarize this in one sentence:\nThe app update fixed several crashes and made the search feature faster.\nOnly provide the summary.',
                'answer': 'The app update improved stability and search speed.',
            },
        ],
    },
    'short_summary': {
        'prompt_templates': [
            'Write a short summary:\n{text}\nOnly provide the summary.',
            'Summarize this briefly:\n{text}\nOnly provide the summary.',
            'Give a brief summary of this text:\n{text}\nDo not explain your answer.',
            'Summarize the following text in a short phrase:\n{text}\nOnly output the summary.',
            'Compress this text into a short summary:\n{text}\nOnly provide the summary.',
        ],
        'examples': [
            {
                'text': 'A storm hit the coast overnight, bringing heavy rain, strong winds, and flooding in several neighborhoods.',
                'answer': 'A coastal storm caused flooding.',
            },
            {
                'text': 'The team lost its first three games but improved after changing its training routine.',
                'answer': 'New training helped the team improve.',
            },
            {
                'text': 'Maria planned to take the bus, but it was delayed, so she walked to school instead.',
                'answer': 'Maria walked after missing the bus.',
            },
            {
                'text': 'The laptop became faster after old files were removed and unnecessary programs were closed.',
                'answer': 'Cleaning up improved laptop speed.',
            },
            {
                'text': 'A local bakery added gluten-free bread after many customers asked for more options.',
                'answer': 'Customer demand led to gluten-free bread.',
            },
            {
                'text': 'The teacher gave extra practice problems because many students struggled with fractions.',
                'answer': 'The teacher added fraction practice.',
            },
            {
                'text': 'The company paused the release after testers found a serious problem in the payment system.',
                'answer': 'A payment bug delayed release.',
            },
            {
                'text': 'The train service added more evening trips to reduce crowding during rush hour.',
                'answer': 'Extra trips reduced train crowding.',
            },
            {
                'text': 'The garden grew well because it received steady sunlight, regular watering, and rich soil.',
                'answer': 'Good conditions helped the garden grow.',
            },
            {
                'text': 'The robot vacuum cleaned the kitchen, hallway, and living room before returning to its charger.',
                'answer': 'The robot vacuum cleaned several rooms.',
            },
            {
                'text': 'The candidate answered the questions clearly and gave examples from previous projects.',
                'answer': 'The candidate gave strong interview answers.',
            },
            {
                'text': 'The library extended its weekend hours so more students could study before exams.',
                'answer': 'The library added exam study hours.',
            },
            {
                'text': 'The cyclist stopped to fix a flat tire before continuing the race.',
                'answer': 'A flat tire briefly delayed the cyclist.',
            },
            {
                'text': 'The museum lowered ticket prices for students and families during the summer.',
                'answer': 'The museum reduced summer ticket prices.',
            },
            {
                'text': 'The new software tool organizes tasks, tracks deadlines, and sends reminders.',
                'answer': 'The software helps manage tasks.',
            },
            {
                'text': 'The concert was moved indoors because rain was expected in the evening.',
                'answer': 'Rain moved the concert indoors.',
            },
            {
                'text': 'The doctor advised rest, fluids, and warm tea while the patient recovered from a cold.',
                'answer': 'The doctor recommended simple cold care.',
            },
            {
                'text': 'The football match ended in a draw after both teams scored in the final ten minutes.',
                'answer': 'Late goals led to a draw.',
            },
            {
                'text': 'The author rewrote the final chapter to make the ending clearer and more emotional.',
                'answer': 'The author improved the ending.',
            },
            {
                'text': 'The startup hired more engineers to speed up development of its mobile app.',
                'answer': 'The startup expanded its engineering team.',
            },
        ],
    },
    'five_words_or_fewer': {
        'prompt_templates': [
            'Summarize this in five words or fewer:\n{text}\nOnly provide the summary.',
            'Write a summary using at most five words:\n{text}\nOnly output the summary.',
            'Compress this into five words or fewer:\n{text}\nDo not explain your answer.',
            'Give a five-word-or-fewer summary:\n{text}\nOnly provide the summary.',
            'Summarize briefly, using no more than five words:\n{text}\nOnly provide the summary.',
        ],
        'examples': [
            {
                'text': 'Maria missed the bus, walked to school, and arrived ten minutes late.',
                'answer': 'Maria arrived late after walking.',
            },
            {
                'text': 'The company delayed the product launch because engineers found a serious bug during final testing.',
                'answer': 'A bug delayed the launch.',
            },
            {
                'text': 'The storm brought heavy rain and strong winds, causing several roads to flood.',
                'answer': 'Storm floods several roads.',
            },
            {
                'text': 'Solar panels turn sunlight into electricity for homes and buildings.',
                'answer': 'Solar panels generate electricity.',
            },
            {
                'text': 'The team practiced every day and improved enough to win the final match.',
                'answer': 'Practice helped the team win.',
            },
            {
                'text': 'The school closed early because snow made the roads unsafe for buses.',
                'answer': 'Snow closed school early.',
            },
            {
                'text': 'The app update fixed several crashes and made search faster.',
                'answer': 'Update fixed crashes and search.',
            },
            {
                'text': 'The bakery added gluten-free bread after customers asked for more options.',
                'answer': 'Bakery adds gluten-free bread.',
            },
            {
                'text': 'The train route will make travel between the two cities faster and easier.',
                'answer': 'New route improves travel.',
            },
            {
                'text': 'The phone battery drained quickly because several apps were running in the background.',
                'answer': 'Background apps drained battery.',
            },
            {
                'text': 'The museum opened a new exhibit about ancient tools, clothing, and daily life.',
                'answer': 'Museum exhibit shows ancient life.',
            },
            {
                'text': 'The chef changed the menu after customers requested more vegetarian meals.',
                'answer': 'Menu adds vegetarian options.',
            },
            {
                'text': 'The cyclist fixed a flat tire before continuing the race.',
                'answer': 'Cyclist fixes flat tire.',
            },
            {
                'text': 'The library extended weekend hours to help students study before exams.',
                'answer': 'Library extends exam hours.',
            },
            {
                'text': 'The researcher repeated the experiment to check whether the results were reliable.',
                'answer': 'Researcher verifies experiment results.',
            },
        ],
    },
    'headline': {
        'prompt_templates': [
            'Write a short headline for this text:\n{text}\nOnly provide the headline.',
            'Turn this text into a concise headline:\n{text}\nOnly provide the headline.',
            'Write a headline that summarizes this text:\n{text}\nDo not explain your answer.',
            'Create a brief headline:\n{text}\nOnly output the headline.',
            'Summarize this as a headline:\n{text}\nOnly provide the headline.',
        ],
        'examples': [
            {
                'text': 'The storm brought heavy rain and strong winds, causing several roads to flood.',
                'answer': 'Storm Floods Roads After Heavy Rain',
            },
            {
                'text': 'The company delayed the product launch because it found a bug during final testing.',
                'answer': 'Testing Bug Delays Product Launch',
            },
            {
                'text': 'The city planted more trees to provide shade and improve air quality.',
                'answer': 'City Plants Trees to Improve Air',
            },
            {
                'text': 'The new train route will make travel between the two cities faster and easier.',
                'answer': 'New Train Route Speeds City Travel',
            },
            {
                'text': 'The school closed early because snow made the roads unsafe for buses.',
                'answer': 'Snow Forces School to Close Early',
            },
            {
                'text': 'The app update fixed several crashes and made the search feature faster.',
                'answer': 'App Update Fixes Crashes',
            },
            {
                'text': 'The museum added a new exhibit about ancient tools, clothing, and daily life.',
                'answer': 'Museum Opens Ancient Life Exhibit',
            },
            {
                'text': 'The library extended its weekend hours so more students could study before exams.',
                'answer': 'Library Extends Hours Before Exams',
            },
            {
                'text': 'The bakery added gluten-free bread after many customers asked for more options.',
                'answer': 'Bakery Adds Gluten-Free Bread',
            },
            {
                'text': 'The concert was moved indoors because rain was expected in the evening.',
                'answer': 'Rain Moves Concert Indoors',
            },
            {
                'text': 'The startup hired more engineers to speed up development of its mobile app.',
                'answer': 'Startup Hires Engineers for App',
            },
            {
                'text': 'The football match ended in a draw after both teams scored in the final ten minutes.',
                'answer': 'Late Goals End Match in Draw',
            },
            {
                'text': 'The teacher gave extra practice problems because many students struggled with fractions.',
                'answer': 'Teacher Adds Extra Fraction Practice',
            },
            {
                'text': 'The phone battery drained quickly because several apps were running in the background.',
                'answer': 'Background Apps Drain Phone Battery',
            },
            {
                'text': 'The author rewrote the final chapter to make the ending clearer and more emotional.',
                'answer': 'Author Rewrites Final Chapter',
            },
        ],
    },
    'key_point': {
        'prompt_templates': [
            'What is the key point of this text?\n{text}\nOnly provide the key point.',
            'State the main point of this text:\n{text}\nOnly provide the answer.',
            'Identify the main idea:\n{text}\nDo not explain your answer.',
            'Give the central point of this text:\n{text}\nOnly output the central point.',
            'Summarize the main idea:\n{text}\nOnly provide the main idea.',
        ],
        'examples': [
            {
                'text': 'Plants need sunlight, water, and nutrients from the soil to grow.',
                'answer': 'Plants need basic resources to grow.',
            },
            {
                'text': 'A password manager stores your passwords securely so you do not have to remember each one.',
                'answer': 'Password managers make storing passwords easier and safer.',
            },
            {
                'text': 'Exercise can strengthen muscles, improve mood, and support long-term health.',
                'answer': 'Exercise benefits both body and mind.',
            },
            {
                'text': 'The recipe uses flour, eggs, milk, and butter to make soft pancakes.',
                'answer': 'The recipe explains how to make pancakes.',
            },
            {
                'text': 'The student revised her essay after receiving feedback from her teacher.',
                'answer': 'Feedback helped the student improve her essay.',
            },
            {
                'text': 'The laptop became faster after old files were removed and unnecessary programs were closed.',
                'answer': 'Cleaning up the laptop improved its performance.',
            },
            {
                'text': 'The doctor advised rest, fluids, and warm tea while the patient recovered from a cold.',
                'answer': 'The patient was advised to recover with simple care.',
            },
            {
                'text': 'The robot vacuum cleaned the kitchen, hallway, and living room before returning to its charger.',
                'answer': 'The robot vacuum cleaned several rooms.',
            },
            {
                'text': 'The candidate answered the questions clearly and gave examples from previous projects.',
                'answer': 'The candidate gave a strong interview.',
            },
            {
                'text': 'The researcher repeated the experiment to check whether the results were reliable.',
                'answer': 'The researcher checked the reliability of the results.',
            },
            {
                'text': 'The train service added more evening trips to reduce crowding during rush hour.',
                'answer': 'The train service added trips to reduce crowding.',
            },
            {
                'text': 'The city planted more trees to provide shade and improve air quality.',
                'answer': 'The city used trees to improve the environment.',
            },
            {
                'text': 'The company paused the release after testers found a serious problem in the payment system.',
                'answer': 'A payment problem delayed the release.',
            },
            {
                'text': 'The garden grew well because it received steady sunlight, regular watering, and rich soil.',
                'answer': 'Good growing conditions helped the garden.',
            },
            {
                'text': 'The new software tool organizes tasks, tracks deadlines, and sends reminders.',
                'answer': 'The tool helps people manage work.',
            },
        ],
    },
    'two_sentence_summary': {
        'prompt_templates': [
            'Summarize this in two short sentences:\n{text}\nOnly provide the summary.',
            'Write a two-sentence summary:\n{text}\nOnly provide the summary.',
            'Summarize the following text in exactly two sentences:\n{text}\nDo not explain your answer.',
            'Give a brief two-sentence summary:\n{text}\nOnly output the summary.',
            'Compress this into two short sentences:\n{text}\nOnly provide the summary.',
        ],
        'examples': [
            {
                'text': 'The town opened a new community center with a library, gym, and study rooms. Local leaders said the center will give families a safe place to learn, exercise, and meet.',
                'answer': 'The town opened a new community center. It will give families space to learn, exercise, and meet.',
            },
            {
                'text': 'A small software team released an update that fixed login errors and improved page loading speed. Users had reported both issues for several weeks.',
                'answer': 'The software team fixed login and speed problems. Users had reported those issues for weeks.',
            },
            {
                'text': 'The school garden produced tomatoes, carrots, and herbs this spring. Students used the harvest in a cooking lesson about healthy meals.',
                'answer': 'The school garden produced fresh vegetables and herbs. Students used them to learn about healthy cooking.',
            },
            {
                'text': 'The airport added clearer signs and more staff near security checkpoints. Officials said the changes should help passengers move through the airport faster.',
                'answer': 'The airport improved signs and staffing. The changes should help passengers move faster.',
            },
            {
                'text': 'A local animal shelter held an adoption event over the weekend. By Sunday evening, twenty dogs and cats had found new homes.',
                'answer': 'The animal shelter held an adoption event. Twenty pets found new homes.',
            },
            {
                'text': 'The science class built small bridges from paper and tested how much weight each one could hold. The activity taught students about design, strength, and testing.',
                'answer': 'Students built and tested paper bridges. The activity taught engineering concepts.',
            },
            {
                'text': 'The city repaired the broken traffic lights at the main intersection. Drivers had experienced long delays there during the morning commute.',
                'answer': 'The city fixed broken traffic lights. The repair should reduce commute delays.',
            },
            {
                'text': 'A musician released a new album inspired by childhood memories and old family stories. Critics praised its honest lyrics and simple acoustic sound.',
                'answer': 'The musician released a personal new album. Critics praised its honest lyrics and acoustic style.',
            },
            {
                'text': 'The hiking trail reopened after workers cleared fallen trees and repaired damaged signs. Park officials reminded visitors to stay on marked paths.',
                'answer': 'The hiking trail reopened after repairs. Visitors were reminded to stay on marked paths.',
            },
            {
                'text': 'The company introduced a four-day workweek for a three-month trial. Managers will compare productivity and employee satisfaction before deciding whether to keep it.',
                'answer': 'The company is testing a four-day workweek. It will review productivity and employee satisfaction before deciding.',
            },
        ],
    },
}
