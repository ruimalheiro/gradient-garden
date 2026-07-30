NON_REPETITION_FIXTURES = {
    'numbered_two_reasons': {
        'messages': [
            {
                'role': 'user',
                'content': '{question}',
            },
            {
                'role': 'assistant',
                'content': '{answer}',
            },
        ],
        'examples': [
            {
                'question': 'Give exactly two different reasons to drink water. Use a numbered list.',
                'answer': '1. It helps keep the body hydrated.\n2. It supports normal body temperature.',
            },
            {
                'question': 'Give exactly two different reasons to sleep well. Use a numbered list.',
                'answer': '1. Sleep helps the body recover.\n2. Sleep supports memory and focus.',
            },
            {
                'question': 'Give exactly two different reasons to exercise. Use a numbered list.',
                'answer': '1. Exercise strengthens muscles.\n2. Exercise can improve mood.',
            },
            {
                'question': 'Give exactly two different reasons to read books. Use a numbered list.',
                'answer': '1. Books can teach new ideas.\n2. Books can be entertaining.',
            },
            {
                'question': 'Give exactly two different reasons to save money. Use a numbered list.',
                'answer': '1. Savings can help in emergencies.\n2. Savings can support future plans.',
            },
            {
                'question': 'Give exactly two different reasons to wash your hands. Use a numbered list.',
                'answer': '1. Washing removes dirt from your skin.\n2. Washing can reduce the spread of germs.',
            },
            {
                'question': 'Give exactly two different reasons to wear a coat in winter. Use a numbered list.',
                'answer': '1. A coat helps keep the body warm.\n2. A coat can protect against wind.',
            },
            {
                'question': 'Give exactly two different reasons to learn math. Use a numbered list.',
                'answer': '1. Math helps solve everyday problems.\n2. Math supports many technical skills.',
            },
            {
                'question': 'Give exactly two different reasons to eat vegetables. Use a numbered list.',
                'answer': '1. Vegetables provide useful nutrients.\n2. Vegetables can support digestion.',
            },
            {
                'question': 'Give exactly two different reasons to back up files. Use a numbered list.',
                'answer': '1. Backups protect against data loss.\n2. Backups make recovery easier.',
            },
            {
                'question': 'Give exactly two different reasons to plan ahead. Use a numbered list.',
                'answer': '1. Planning makes tasks clearer.\n2. Planning helps avoid forgotten steps.',
            },
            {
                'question': 'Give exactly two different reasons to practice a skill. Use a numbered list.',
                'answer': '1. Practice builds confidence.\n2. Practice improves performance over time.',
            },
        ],
    },
    'numbered_three_reasons': {
        'messages': [
            {
                'role': 'user',
                'content': '{question}',
            },
            {
                'role': 'assistant',
                'content': '{answer}',
            },
        ],
        'examples': [
            {
                'question': 'Give exactly three different benefits of exercise. Use a numbered list.',
                'answer': '1. It strengthens muscles.\n2. It can improve mood.\n3. It supports heart health.',
            },
            {
                'question': 'Give exactly three different benefits of reading. Use a numbered list.',
                'answer': '1. Reading can build vocabulary.\n2. Reading can teach new facts.\n3. Reading can improve focus.',
            },
            {
                'question': 'Give exactly three different ways to stay healthy. Use a numbered list.',
                'answer': '1. Eat balanced meals.\n2. Exercise regularly.\n3. Sleep enough each night.',
            },
            {
                'question': 'Give exactly three different ways to be polite. Use a numbered list.',
                'answer': "1. Say please and thank you.\n2. Listen when others speak.\n3. Respect other people's time.",
            },
            {
                'question': 'Give exactly three different reasons to learn programming. Use a numbered list.',
                'answer': '1. It helps solve problems.\n2. It can build useful tools.\n3. It can support many careers.',
            },
            {
                'question': 'Give exactly three different reasons to learn a language. Use a numbered list.',
                'answer': '1. It helps people communicate.\n2. It makes travel easier.\n3. It can open job opportunities.',
            },
            {
                'question': 'Give exactly three different benefits of teamwork. Use a numbered list.',
                'answer': '1. Teamwork lets people share ideas.\n2. Teamwork divides difficult tasks.\n3. Teamwork helps people support each other.',
            },
            {
                'question': 'Give exactly three different reasons to keep a schedule. Use a numbered list.',
                'answer': '1. A schedule organizes time.\n2. A schedule reduces missed tasks.\n3. A schedule makes priorities clearer.',
            },
            {
                'question': 'Give exactly three different ways to save energy at home. Use a numbered list.',
                'answer': '1. Turn off unused lights.\n2. Unplug idle devices.\n3. Use efficient appliances.',
            },
            {
                'question': 'Give exactly three different reasons to ask questions. Use a numbered list.',
                'answer': '1. Questions clarify confusing ideas.\n2. Questions reveal missing information.\n3. Questions help people learn.',
            },
            {
                'question': 'Give exactly three different benefits of drinking water. Use a numbered list.',
                'answer': '1. Water helps hydration.\n2. Water supports body temperature.\n3. Water helps the body function.',
            },
            {
                'question': 'Give exactly three different reasons to write notes. Use a numbered list.',
                'answer': '1. Notes preserve important details.\n2. Notes make review easier.\n3. Notes support better memory.',
            },
        ],
    },
    'bullet_points': {
        'messages': [
            {
                'role': 'user',
                'content': '{question}',
            },
            {
                'role': 'assistant',
                'content': '{answer}',
            },
        ],
        'examples': [
            {
                'question': 'Give exactly two non-repeating bullet points about why sleep matters.',
                'answer': '- Sleep helps the body recover.\n- Sleep supports memory and focus.',
            },
            {
                'question': 'Give exactly two non-repeating bullet points about why water matters.',
                'answer': '- Water keeps the body hydrated.\n- Water helps regulate body temperature.',
            },
            {
                'question': 'Give exactly two non-repeating bullet points about why exercise matters.',
                'answer': '- Exercise strengthens the body.\n- Exercise can improve mood.',
            },
            {
                'question': 'Give exactly three non-repeating bullet points about why teamwork matters.',
                'answer': '- Teamwork lets people share ideas.\n- Teamwork can divide difficult tasks.\n- Teamwork helps people support each other.',
            },
            {
                'question': 'Give exactly three non-repeating bullet points about why planning matters.',
                'answer': '- Planning makes goals clearer.\n- Planning helps avoid missed steps.\n- Planning can save time.',
            },
            {
                'question': 'Give exactly two non-repeating bullet points about why reading matters.',
                'answer': '- Reading can teach new information.\n- Reading can improve vocabulary.',
            },
            {
                'question': 'Give exactly two non-repeating bullet points about why saving money matters.',
                'answer': '- Saving money helps with emergencies.\n- Saving money supports future goals.',
            },
            {
                'question': 'Give exactly three non-repeating bullet points about why schools matter.',
                'answer': '- Schools teach useful skills.\n- Schools help students practice teamwork.\n- Schools can support personal growth.',
            },
            {
                'question': 'Give exactly three non-repeating bullet points about why libraries matter.',
                'answer': '- Libraries provide access to books.\n- Libraries offer quiet study space.\n- Libraries can support community learning.',
            },
            {
                'question': 'Give exactly three non-repeating bullet points about why clean water matters.',
                'answer': '- Clean water is safe to drink.\n- Clean water helps prevent illness.\n- Clean water supports cooking and hygiene.',
            },
        ],
    },
    'comma_lists_four': {
        'messages': [
            {
                'role': 'user',
                'content': '{question}',
            },
            {
                'role': 'assistant',
                'content': '{answer}',
            },
        ],
        'examples': [
            {
                'question': 'List exactly four different animals, separated by commas.',
                'answer': 'cat, dog, horse, rabbit',
            },
            {
                'question': 'List exactly four different fruits, separated by commas.',
                'answer': 'apple, banana, orange, pear',
            },
            {
                'question': 'List exactly four different colors, separated by commas.',
                'answer': 'red, blue, green, yellow',
            },
            {
                'question': 'List exactly four different vegetables, separated by commas.',
                'answer': 'carrot, onion, broccoli, spinach',
            },
            {
                'question': 'List exactly four different programming languages, separated by commas.',
                'answer': 'Python, JavaScript, Rust, Java',
            },
            {
                'question': 'List exactly four different countries, separated by commas.',
                'answer': 'Portugal, France, Japan, Canada',
            },
            {
                'question': 'List exactly four different cities, separated by commas.',
                'answer': 'London, Lisbon, Paris, Tokyo',
            },
            {
                'question': 'List exactly four different tools, separated by commas.',
                'answer': 'hammer, wrench, drill, saw',
            },
            {
                'question': 'List exactly four different sports, separated by commas.',
                'answer': 'soccer, tennis, basketball, swimming',
            },
            {
                'question': 'List exactly four different drinks, separated by commas.',
                'answer': 'water, tea, coffee, juice',
            },
            {
                'question': 'List exactly four unique animals. Do not repeat any item. Use commas only.',
                'answer': 'lion, zebra, fox, bear',
            },
            {
                'question': 'List exactly four unique fruits. Do not repeat any item. Use commas only.',
                'answer': 'mango, peach, grape, plum',
            },
            {
                'question': 'List exactly four unique colors. Do not repeat any item. Use commas only.',
                'answer': 'black, white, purple, orange',
            },
            {
                'question': 'List exactly four unique vehicles. Do not repeat any item. Use commas only.',
                'answer': 'car, bus, train, bicycle',
            },
            {
                'question': 'List exactly four unique planets. Do not repeat any item. Use commas only.',
                'answer': 'Mercury, Venus, Earth, Mars',
            },
        ],
    },
    'comma_lists_five': {
        'messages': [
            {
                'role': 'user',
                'content': '{question}',
            },
            {
                'role': 'assistant',
                'content': '{answer}',
            },
        ],
        'examples': [
            {
                'question': 'List exactly five different household objects, separated by commas.',
                'answer': 'chair, table, lamp, spoon, towel',
            },
            {
                'question': 'List exactly five different school supplies, separated by commas.',
                'answer': 'pencil, notebook, ruler, eraser, folder',
            },
            {
                'question': 'List exactly five different modes of transport, separated by commas.',
                'answer': 'car, train, bicycle, bus, plane',
            },
            {
                'question': 'List exactly five different weather words, separated by commas.',
                'answer': 'rain, snow, wind, fog, sunshine',
            },
            {
                'question': 'List exactly five different body parts, separated by commas.',
                'answer': 'hand, foot, arm, leg, head',
            },
            {
                'question': 'List exactly five different musical instruments, separated by commas.',
                'answer': 'piano, guitar, violin, drums, flute',
            },
            {
                'question': 'List exactly five different desserts, separated by commas.',
                'answer': 'cake, pie, pudding, brownie, cookie',
            },
            {
                'question': 'List exactly five different jobs, separated by commas.',
                'answer': 'teacher, doctor, engineer, nurse, chef',
            },
            {
                'question': 'List exactly five different flowers, separated by commas.',
                'answer': 'rose, tulip, daisy, lily, orchid',
            },
            {
                'question': 'List exactly five different kitchen utensils, separated by commas.',
                'answer': 'spoon, fork, knife, whisk, spatula',
            },
            {
                'question': 'List exactly five unique household objects. Do not repeat any item. Use commas only.',
                'answer': 'mirror, blanket, pillow, plate, cup',
            },
            {
                'question': 'List exactly five unique school supplies. Do not repeat any item. Use commas only.',
                'answer': 'pen, marker, backpack, glue, scissors',
            },
            {
                'question': 'List exactly five unique weather words. Do not repeat any item. Use commas only.',
                'answer': 'cloud, thunder, lightning, drizzle, hail',
            },
            {
                'question': 'List exactly five unique body parts. Do not repeat any item. Use commas only.',
                'answer': 'eye, ear, nose, mouth, shoulder',
            },
            {
                'question': 'List exactly five unique emotions. Do not repeat any item. Use commas only.',
                'answer': 'joy, sadness, anger, fear, surprise',
            },
        ],
    },
    'comma_examples_three': {
        'messages': [
            {
                'role': 'user',
                'content': '{question}',
            },
            {
                'role': 'assistant',
                'content': '{answer}',
            },
        ],
        'examples': [
            {
                'question': 'Give exactly three different examples of healthy foods, separated by commas.',
                'answer': 'apples, carrots, beans',
            },
            {
                'question': 'Give exactly three different examples of warm clothing, separated by commas.',
                'answer': 'coat, scarf, gloves',
            },
            {
                'question': 'Give exactly three different examples of things in a kitchen, separated by commas.',
                'answer': 'pan, plate, spoon',
            },
            {
                'question': 'Give exactly three different examples of things in a classroom, separated by commas.',
                'answer': 'desk, board, pencil',
            },
            {
                'question': 'Give exactly three different examples of things in a garden, separated by commas.',
                'answer': 'flowers, soil, seeds',
            },
            {
                'question': 'Give exactly three different examples of breakfast foods, separated by commas.',
                'answer': 'eggs, toast, cereal',
            },
            {
                'question': 'Give exactly three different examples of outdoor activities, separated by commas.',
                'answer': 'hiking, cycling, running',
            },
            {
                'question': 'Give exactly three different examples of computer parts, separated by commas.',
                'answer': 'CPU, GPU, RAM',
            },
            {
                'question': 'Give exactly three different examples of writing tools, separated by commas.',
                'answer': 'pen, pencil, marker',
            },
            {
                'question': 'Give exactly three different examples of things people recycle, separated by commas.',
                'answer': 'paper, glass, plastic',
            },
            {
                'question': 'Give exactly three unique examples of fruits. Do not repeat any item. Use commas only.',
                'answer': 'apple, mango, pear',
            },
            {
                'question': 'Give exactly three unique examples of animals. Do not repeat any item. Use commas only.',
                'answer': 'cat, rabbit, horse',
            },
            {
                'question': 'Give exactly three unique examples of colors. Do not repeat any item. Use commas only.',
                'answer': 'red, green, purple',
            },
            {
                'question': 'Give exactly three unique examples of sports. Do not repeat any item. Use commas only.',
                'answer': 'tennis, rugby, cricket',
            },
            {
                'question': 'Give exactly three unique examples of tools. Do not repeat any item. Use commas only.',
                'answer': 'hammer, pliers, level',
            },
        ],
    },
}
