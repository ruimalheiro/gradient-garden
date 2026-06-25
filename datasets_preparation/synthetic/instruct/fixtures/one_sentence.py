ONE_SENTENCE_FIXTURES = {
    'topics': {
        'prompt_templates': [
            'Write exactly one sentence about {topic}.',
            'Write exactly one sentence about {topic}.\nOnly provide the sentence.',
            'Write one short sentence about {topic}.',
            'Write one short sentence about {topic}.\nDo not write a second sentence.',
            'Describe {topic} in exactly one sentence.',
            'Give one short sentence about {topic}.',
            'Write one sentence only about {topic}.',
            'In exactly one sentence, explain {topic}.',
            'Write a single sentence about {topic}. Stop after that sentence.',
            'Answer with one sentence only: {topic}.',
        ],
        'examples': [
            {
                'topic': 'rain',
                'answers': [
                    'Rain falls from clouds and helps plants grow.',
                    'Rain brings water to rivers, lakes, and soil.',
                    'Rain is water that falls from clouds to the ground.',
                ],
            },
            {
                'topic': 'snow',
                'answers': [
                    'Snow is frozen water that falls from clouds in cold weather.',
                    'Snow can cover the ground when the air is cold enough.',
                    'Snow often makes the world look quiet and bright.',
                ],
            },
            {
                'topic': 'sleep',
                'answers': [
                    'Sleep helps the body rest, recover, and store memories.',
                    'Sleep gives the brain and body time to recharge.',
                    'Good sleep can help people feel more focused and healthy.',
                ],
            },
            {
                'topic': 'music',
                'answers': [
                    'Music uses sound and rhythm to express feelings.',
                    'Music can make people feel calm, happy, or excited.',
                    'Music is a creative way to share emotion and ideas.',
                ],
            },
            {
                'topic': 'books',
                'answers': [
                    'Books can teach facts, tell stories, and spark imagination.',
                    'Reading books helps people learn new ideas.',
                    'Books let readers explore new places and ideas.',
                ],
            },
            {
                'topic': 'dogs',
                'answers': [
                    'Dogs are loyal animals that often enjoy spending time with people.',
                    'Dogs can be playful, friendly, and protective companions.',
                    'Many dogs like walking, running, and playing with people.',
                ],
            },
            {
                'topic': 'cats',
                'answers': [
                    'Cats are curious animals that often enjoy quiet places.',
                    'Cats can be independent, playful, and affectionate.',
                    'Many cats like to climb, nap, and explore.',
                ],
            },
            {
                'topic': 'trees',
                'answers': [
                    'Trees provide shade, oxygen, and homes for many animals.',
                    'Trees grow from roots and reach upward toward sunlight.',
                    'Trees support life in many environments.',
                ],
            },
            {
                'topic': 'flowers',
                'answers': [
                    'Flowers often have bright colors and pleasant smells.',
                    'Flowers help some plants reproduce by attracting pollinators.',
                    'Flowers can make gardens and parks look beautiful.',
                ],
            },
            {
                'topic': 'the ocean',
                'answers': [
                    'The ocean is a vast body of salt water filled with life.',
                    'The ocean covers much of Earth and affects the weather.',
                    'The ocean is home to fish, whales, coral, and many other living things.',
                ],
            },
            {
                'topic': 'mountains',
                'answers': [
                    'Mountains rise high above the land.',
                    'Mountains are large landforms with steep slopes.',
                    'Mountains can be beautiful places for hiking and exploration.',
                ],
            },
            {
                'topic': 'the sun',
                'answers': [
                    'The sun gives Earth light and warmth.',
                    'The sun is the star at the center of our solar system.',
                    'Sunlight helps plants grow and keeps Earth warm.',
                ],
            },
            {
                'topic': 'the moon',
                'answers': [
                    'The moon orbits Earth and reflects sunlight at night.',
                    'The moon changes appearance as it moves around Earth.',
                    'The moon affects ocean tides through its gravity.',
                ],
            },
            {
                'topic': 'stars',
                'answers': [
                    'Stars are huge balls of hot gas that shine in space.',
                    'Stars give off light from powerful reactions in their cores.',
                    'Stars help people understand the universe.',
                ],
            },
            {
                'topic': 'space',
                'answers': [
                    'Space is the vast area beyond Earth and its atmosphere.',
                    'Space contains stars, planets, moons, galaxies, and dust.',
                    'Space exploration helps people learn about the universe.',
                ],
            },
            {
                'topic': 'school',
                'answers': [
                    'School is a place where people learn skills and ideas.',
                    'School helps students practice reading, writing, math, and teamwork.',
                    'A good school can help students grow in knowledge and confidence.',
                ],
            },
            {
                'topic': 'friendship',
                'answers': [
                    'Friendship is built on kindness, trust, and shared time.',
                    'A good friendship can make people feel supported and understood.',
                    'Friendship grows when people listen to and care for each other.',
                ],
            },
            {
                'topic': 'kindness',
                'answers': [
                    'Kindness means treating others with care and respect.',
                    'Small acts of kindness can make someone’s day better.',
                    'Kindness helps people feel valued and supported.',
                ],
            },
            {
                'topic': 'cooking',
                'answers': [
                    'Cooking turns ingredients into meals people can enjoy.',
                    'Cooking can be practical, creative, and fun.',
                    'Good cooking often depends on timing, heat, and simple ingredients.',
                ],
            },
            {
                'topic': 'exercise',
                'answers': [
                    'Exercise helps keep the body strong and healthy.',
                    'Regular exercise can improve energy, mood, and fitness.',
                    'Exercise includes activities like walking, running, swimming, and stretching.',
                ],
            },
            {
                'topic': 'water',
                'answers': [
                    'Water is essential for life on Earth.',
                    'Water helps people, animals, and plants survive.',
                    'Clean water is important for drinking, cooking, and health.',
                ],
            },
            {
                'topic': 'fire',
                'answers': [
                    'Fire gives heat and light but must be handled carefully.',
                    'Fire can cook food, warm homes, and also cause danger.',
                    'Fire needs heat, fuel, and oxygen to keep burning.',
                ],
            },
            {
                'topic': 'computers',
                'answers': [
                    'Computers are machines that process information and run programs.',
                    'Computers help people write, calculate, communicate, and create.',
                    'A computer follows instructions to store and transform data.',
                ],
            },
            {
                'topic': 'robots',
                'answers': [
                    'Robots are machines designed to perform tasks automatically.',
                    'Robots can help with repetitive, difficult, or dangerous work.',
                    'Some robots move through the world while others work inside computers.',
                ],
            },
            {
                'topic': 'GPUs',
                'answers': [
                    'A GPU is a chip that can perform many calculations at the same time.',
                    'GPUs are useful for graphics, games, and machine learning.',
                    'A GPU helps computers process large amounts of data quickly.',
                ],
            },
            {
                'topic': 'bicycles',
                'answers': [
                    'A bicycle is a vehicle with two wheels powered by pedaling.',
                    'Bicycles are useful for exercise, travel, and recreation.',
                    'Riding a bicycle can be a simple and efficient way to move around.',
                ],
            },
            {
                'topic': 'gardens',
                'answers': [
                    'Gardens are places where people grow plants, flowers, or food.',
                    'A garden can provide beauty, fresh air, and quiet enjoyment.',
                    'Gardens need sunlight, water, soil, and care.',
                ],
            },
            {
                'topic': 'coffee',
                'answers': [
                    'Coffee is a drink made from roasted coffee beans.',
                    'Many people drink coffee because it tastes rich and contains caffeine.',
                    'Coffee can be served hot, cold, black, or with milk.',
                ],
            },
            {
                'topic': 'tea',
                'answers': [
                    'Tea is a drink made by steeping leaves or herbs in hot water.',
                    'Tea can taste calming, bitter, sweet, or floral depending on the type.',
                    'Many people drink tea for comfort, flavor, or relaxation.',
                ],
            },
            {
                'topic': 'penguins',
                'answers': [
                    'Penguins are birds that cannot fly but swim very well.',
                    'Penguins use their wings like flippers to move through water.',
                    'Many penguins live in cold places and eat fish or krill.',
                ],
            },
            {
                'topic': 'chocolate',
                'answers': [
                    'Chocolate is a sweet food made from cocoa beans.',
                    'Chocolate can be eaten alone or used in desserts.',
                    'Many people enjoy chocolate for its rich, sweet taste.',
                ],
            },
            {
                'topic': 'soccer',
                'answers': [
                    'Soccer is a team sport played by kicking a ball into a goal.',
                    'Soccer players try to score goals while defending their own net.',
                    'Soccer is played around the world by teams of many ages.',
                ],
            },
            {
                'topic': 'electric cars',
                'answers': [
                    'Electric cars use batteries to power their motors.',
                    'Electric cars run on electricity instead of gasoline.',
                    'Electric cars can reduce fuel use and tailpipe pollution.',
                ],
            },
            {
                'topic': 'cloud storage',
                'answers': [
                    'Cloud storage lets people save files on remote servers.',
                    'Cloud storage helps people access files from different devices.',
                    'Cloud storage keeps data online instead of only on one computer.',
                ],
            },
            {
                'topic': 'machine learning',
                'answers': [
                    'Machine learning helps computers find patterns in data.',
                    'Machine learning lets computers improve from examples.',
                    'Machine learning is used to make predictions from data.',
                ],
            },
            {
                'topic': 'neural networks',
                'answers': [
                    'Neural networks are computer models that learn patterns from data.',
                    'Neural networks are inspired by connected layers of simple units.',
                    'Neural networks can help with tasks like prediction and classification.',
                ],
            },
            {
                'topic': 'databases',
                'answers': [
                    'Databases store information so it can be found and updated.',
                    'A database organizes data for quick access.',
                    'Databases help applications save and retrieve structured information.',
                ],
            },
            {
                'topic': 'algorithms',
                'answers': [
                    'An algorithm is a set of steps for solving a problem.',
                    'Algorithms tell computers how to complete tasks.',
                    'A good algorithm solves a problem clearly and efficiently.',
                ],
            },
            {
                'topic': 'umbrellas',
                'answers': [
                    'Umbrellas help keep people dry in the rain.',
                    'An umbrella is used for protection from rain or sun.',
                    'Umbrellas provide portable shelter in wet weather.',
                ],
            },
            {
                'topic': 'healthy breakfast',
                'answers': [
                    'A healthy breakfast can include fruit, grains, and protein.',
                    'A healthy breakfast gives the body energy for the day.',
                    'A healthy breakfast can help people feel focused in the morning.',
                ],
            },
        ],
    },
    'must_include_words': {
        'prompt_templates': [
            'Write a sentence that contains the words "{word1}" and "{word2}".',
            'Write exactly one sentence that contains the words "{word1}" and "{word2}".',
            'Write one short sentence using both "{word1}" and "{word2}".',
            'Use "{word1}" and "{word2}" in one sentence only.',
            'Write a single sentence that includes both "{word1}" and "{word2}".',
            'Write one sentence containing both "{word1}" and "{word2}".\nOnly provide the sentence.',
        ],
        'examples': [
            {
                'word1': 'river',
                'word2': 'stone',
                'answer': 'The river flowed around a smooth stone.',
            },
            {
                'word1': 'stone',
                'word2': 'river',
                'answer': 'A small stone rested beside the river.',
            },
            {
                'word1': 'garden',
                'word2': 'rain',
                'answer': 'The rain watered the garden overnight.',
            },
            {
                'word1': 'book',
                'word2': 'window',
                'answer': 'She read a book beside the window.',
            },
            {
                'word1': 'cat',
                'word2': 'chair',
                'answer': 'The cat slept under the chair.',
            },
            {
                'word1': 'music',
                'word2': 'room',
                'answer': 'Music filled the room during the party.',
            },
            {
                'word1': 'tree',
                'word2': 'bird',
                'answer': 'A bird landed in the tree.',
            },
            {
                'word1': 'coffee',
                'word2': 'morning',
                'answer': 'Coffee helped brighten the morning.',
            },
            {
                'word1': 'computer',
                'word2': 'desk',
                'answer': 'The computer sat on the desk.',
            },
            {
                'word1': 'ocean',
                'word2': 'wind',
                'answer': 'The wind moved across the ocean.',
            },
            {
                'word1': 'school',
                'word2': 'bus',
                'answer': 'The bus stopped outside the school.',
            },
            {
                'word1': 'mountain',
                'word2': 'snow',
                'answer': 'Snow covered the top of the mountain.',
            },
            {
                'word1': 'flower',
                'word2': 'sun',
                'answer': 'The flower turned toward the sun.',
            },
            {
                'word1': 'phone',
                'word2': 'pocket',
                'answer': 'He kept his phone in his pocket.',
            },
            {
                'word1': 'bread',
                'word2': 'table',
                'answer': 'Fresh bread was on the table.',
            },
            {
                'word1': 'train',
                'word2': 'station',
                'answer': 'The train arrived at the station.',
            },
            {
                'word1': 'dog',
                'word2': 'park',
                'answer': 'The dog ran through the park.',
            },
            {
                'word1': 'cloud',
                'word2': 'sky',
                'answer': 'A white cloud crossed the sky.',
            },
            {
                'word1': 'pencil',
                'word2': 'paper',
                'answer': 'She wrote on the paper with a pencil.',
            },
            {
                'word1': 'lamp',
                'word2': 'bed',
                'answer': 'The lamp stood beside the bed.',
            },
        ],
    },
}
