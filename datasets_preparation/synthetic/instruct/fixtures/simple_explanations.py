SIMPLE_EXPLANATION_FIXTURES = {
    'technology': {
        'prompt_templates': [
            'Explain what {concept} is in simple words. Use at most two short sentences.',
            'Explain {concept} in simple words. Use at most two short sentences.',
            'What is {concept}? Explain in simple words using at most two short sentences.',
            'Explain {concept} simply. Do not use more than two short sentences.',
            'Give a simple explanation of {concept}. Stop after two short sentences.',
            'Explain {concept} for a beginner. Use simple words and no more than two sentences.',
        ],
        'examples': [
            {
                'concept': 'a GPU',
                'answer': 'A GPU is a computer chip that handles many calculations at once. It is useful for graphics and AI.',
            },
            {
                'concept': 'a CPU',
                'answer': 'A CPU is the main chip that runs instructions in a computer. It helps control what the computer does.',
            },
            {
                'concept': 'RAM',
                'answer': 'RAM is short-term memory a computer uses while it is working. It helps programs run quickly.',
            },
            {
                'concept': 'the internet',
                'answer': 'The internet is a huge network that connects computers around the world. It lets people share information.',
            },
            {
                'concept': 'a database',
                'answer': 'A database is an organized place to store information. It helps people find and update data easily.',
            },
            {
                'concept': 'an algorithm',
                'answer': 'An algorithm is a set of steps for solving a problem. A computer can follow those steps to do a task.',
            },
            {
                'concept': 'a token',
                'answer': 'A token is a small piece of text, like a word or part of a word. Language models read and write tokens.',
            },
            {
                'concept': 'a neural network',
                'answer': 'A neural network is a computer system that learns patterns from data. It can use those patterns to make predictions.',
            },
            {
                'concept': 'machine learning',
                'answer': 'Machine learning teaches computers to learn patterns from examples. It helps them make predictions or decisions.',
            },
            {
                'concept': 'an app',
                'answer': 'An app is a program you use on a phone or computer. It helps you do a specific task.',
            },
            {
                'concept': 'cloud storage',
                'answer': 'Cloud storage keeps your files on remote computers. You can access them through the internet.',
            },
            {
                'concept': 'a web browser',
                'answer': 'A web browser is an app for visiting websites. It shows pages, images, videos, and links.',
            },
            {
                'concept': 'an operating system',
                'answer': 'An operating system is the main software that manages a computer. It helps apps, files, and hardware work together.',
            },
            {
                'concept': 'a file',
                'answer': 'A file is a saved piece of information on a computer. It can hold text, pictures, music, or other data.',
            },
            {
                'concept': 'a folder',
                'answer': 'A folder is a place to organize files. It helps you keep related things together.',
            },
            {
                'concept': 'Wi-Fi',
                'answer': 'Wi-Fi lets devices connect to the internet without cables. It uses radio signals to send data.',
            },
            {
                'concept': 'Bluetooth',
                'answer': 'Bluetooth lets nearby devices connect wirelessly. It is often used for headphones, keyboards, and speakers.',
            },
            {
                'concept': 'a password',
                'answer': 'A password is a secret word or phrase used to protect an account. It helps stop other people from getting in.',
            },
            {
                'concept': 'two-factor authentication',
                'answer': 'Two-factor authentication adds a second check when you sign in. It makes accounts harder to steal.',
            },
            {
                'concept': 'encryption',
                'answer': 'Encryption turns information into a secret form. Only someone with the right key can read it.',
            },
            {
                'concept': 'a server',
                'answer': 'A server is a computer that provides data or services to other computers. Websites and apps often use servers.',
            },
            {
                'concept': 'an API',
                'answer': 'An API is a way for programs to talk to each other. It lets one app request information or actions from another.',
            },
            {
                'concept': 'a battery',
                'answer': 'A battery stores energy for later use. It powers devices when they are not plugged in.',
            },
            {
                'concept': 'a charger',
                'answer': 'A charger sends electrical energy into a battery. It helps a device regain power.',
            },
            {
                'concept': 'a search engine',
                'answer': 'A search engine helps people find information online. It looks through many pages and returns useful results.',
            },
            {
                'concept': 'a computer program',
                'answer': 'A computer program is a set of instructions. It tells a computer what to do.',
            },
            {
                'concept': 'a bug in software',
                'answer': 'A bug is a mistake in a computer program. It can make the program behave incorrectly.',
            },
            {
                'concept': 'a software update',
                'answer': 'A software update changes a program after it is installed. It can fix bugs, add features, or improve security.',
            },
            {
                'concept': 'artificial intelligence',
                'answer': 'Artificial intelligence is software that can do tasks that seem to require thinking. It can help with things like language, images, and predictions.',
            },
            {
                'concept': 'a language model',
                'answer': 'A language model is software that learns patterns in text. It uses those patterns to read and write language.',
            },
        ],
    },
    'general_science': {
        'prompt_templates': [
            'Explain what {concept} is in simple words. Use at most two short sentences.',
            'Explain {concept} in simple words. Use at most two short sentences.',
            'What is {concept}? Explain in simple words using at most two short sentences.',
            'Explain {concept} simply. Do not use more than two short sentences.',
            'Give a simple explanation of {concept}. Stop after two short sentences.',
            'Explain {concept} for a beginner. Use simple words and no more than two sentences.',
        ],
        'examples': [
            {
                'concept': 'electricity',
                'answer': 'Electricity is energy that moves through wires. It powers lights, machines, and devices.',
            },
            {
                'concept': 'gravity',
                'answer': 'Gravity is a force that pulls objects toward each other. On Earth, it pulls things toward the ground.',
            },
            {
                'concept': 'photosynthesis',
                'answer': 'Photosynthesis is how plants use sunlight to make food. They use water, carbon dioxide, and light.',
            },
            {
                'concept': 'evaporation',
                'answer': 'Evaporation happens when liquid turns into gas. For example, water can become vapor when it warms up.',
            },
            {
                'concept': 'condensation',
                'answer': 'Condensation happens when gas cools and becomes liquid. It is why water drops can form on a cold glass.',
            },
            {
                'concept': 'the water cycle',
                'answer': 'The water cycle is how water moves around Earth. Water evaporates, forms clouds, and falls as rain or snow.',
            },
            {
                'concept': 'a planet',
                'answer': 'A planet is a large object that moves around a star. Earth is a planet that orbits the Sun.',
            },
            {
                'concept': 'a star',
                'answer': 'A star is a huge ball of hot gas that gives off light. The Sun is the closest star to Earth.',
            },
            {
                'concept': 'the Moon',
                'answer': 'The Moon is a natural object that orbits Earth. It reflects light from the Sun.',
            },
            {
                'concept': 'an orbit',
                'answer': 'An orbit is the path one object takes around another object in space. Earth orbits the Sun.',
            },
            {
                'concept': 'a magnet',
                'answer': 'A magnet is an object that can pull some metals toward it. It has invisible forces around it.',
            },
            {
                'concept': 'friction',
                'answer': 'Friction is a force that slows things down when surfaces rub together. It helps shoes grip the ground.',
            },
            {
                'concept': 'sound',
                'answer': 'Sound is made by vibrations. Those vibrations travel through air, water, or other materials to your ears.',
            },
            {
                'concept': 'light',
                'answer': 'Light is energy that lets us see. It can come from the Sun, lamps, or fire.',
            },
            {
                'concept': 'heat',
                'answer': 'Heat is energy that makes things warmer. It can move from warmer objects to cooler ones.',
            },
            {
                'concept': 'air',
                'answer': 'Air is the mixture of gases around Earth. People and animals breathe oxygen from it.',
            },
            {
                'concept': 'oxygen',
                'answer': 'Oxygen is a gas that people and many animals need to live. We breathe it in from the air.',
            },
            {
                'concept': 'carbon dioxide',
                'answer': 'Carbon dioxide is a gas in the air. Plants use it during photosynthesis.',
            },
            {
                'concept': 'a cell',
                'answer': 'A cell is a tiny living unit. Plants, animals, and people are made of cells.',
            },
            {
                'concept': 'a habitat',
                'answer': 'A habitat is the place where a living thing naturally lives. It provides food, water, shelter, and space.',
            },
            {
                'concept': 'an ecosystem',
                'answer': 'An ecosystem is a group of living things and their environment. Plants, animals, water, soil, and air all interact in it.',
            },
            {
                'concept': 'recycling',
                'answer': 'Recycling turns used materials into something that can be used again. It helps reduce waste.',
            },
            {
                'concept': 'climate',
                'answer': 'Climate is the usual weather pattern of a place over a long time. It is different from the weather on one day.',
            },
            {
                'concept': 'weather',
                'answer': 'Weather is what the air is like at a certain time and place. It includes rain, wind, temperature, and clouds.',
            },
        ],
    },
    'everyday_concepts': {
        'prompt_templates': [
            'Explain what {concept} is in simple words. Use at most two short sentences.',
            'Explain {concept} in simple words. Use at most two short sentences.',
            'What is {concept}? Explain in simple words using at most two short sentences.',
            'Explain {concept} simply. Do not use more than two short sentences.',
            'Give a simple explanation of {concept}. Stop after two short sentences.',
            'Explain {concept} for a beginner. Use simple words and no more than two sentences.',
        ],
        'examples': [
            {
                'concept': 'a bank account',
                'answer': 'A bank account is a place to keep money at a bank. You can use it to save, receive, or spend money.',
            },
            {
                'concept': 'a budget',
                'answer': 'A budget is a plan for how to use money. It helps you track spending and saving.',
            },
            {
                'concept': 'interest',
                'answer': 'Interest is extra money paid for borrowing or saving money. A bank may charge it or pay it.',
            },
            {
                'concept': 'a receipt',
                'answer': 'A receipt is proof that you paid for something. It usually shows the item, price, and date.',
            },
            {
                'concept': 'a schedule',
                'answer': 'A schedule is a plan for when things happen. It helps people organize time.',
            },
            {
                'concept': 'a deadline',
                'answer': 'A deadline is the latest time something should be finished. Missing it can cause problems.',
            },
            {
                'concept': 'a calendar',
                'answer': 'A calendar shows days, weeks, and months. It helps people remember dates and events.',
            },
            {
                'concept': 'a recipe',
                'answer': 'A recipe is a set of instructions for making food. It lists ingredients and steps.',
            },
            {
                'concept': 'a map',
                'answer': 'A map shows places and how they connect. It helps people find where to go.',
            },
            {
                'concept': 'a library',
                'answer': 'A library is a place where people can read or borrow books. Many libraries also offer computers and study space.',
            },
            {
                'concept': 'exercise',
                'answer': 'Exercise is movement that helps keep the body healthy. Walking, running, and stretching are examples.',
            },
            {
                'concept': 'sleep',
                'answer': 'Sleep is a time when the body and brain rest. It helps people recover and feel ready for the next day.',
            },
            {
                'concept': 'healthy food',
                'answer': 'Healthy food gives the body useful nutrients. It helps people grow, move, and stay well.',
            },
            {
                'concept': 'teamwork',
                'answer': 'Teamwork means people work together toward a shared goal. It often makes hard tasks easier.',
            },
            {
                'concept': 'practice',
                'answer': 'Practice means doing something again to get better. It helps build skill over time.',
            },
            {
                'concept': 'feedback',
                'answer': 'Feedback is advice about how something went. It can help someone improve their work.',
            },
            {
                'concept': 'a summary',
                'answer': 'A summary is a shorter version of a longer text. It keeps the main idea and removes extra details.',
            },
            {
                'concept': 'a question',
                'answer': 'A question asks for information. It often needs an answer.',
            },
        ],
    },
}
