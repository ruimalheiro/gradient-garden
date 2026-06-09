LIST_CATEGORIES = {
    'fruits': [
        'apple',
        'banana',
        'orange',
        'pear',
        'grape',
        'mango',
        'peach',
        'plum',
        'kiwi',
        'pineapple',
        'melon',
        'cherry',
    ],
    'colors': [
        'red',
        'blue',
        'green',
        'yellow',
        'purple',
        'orange',
        'black',
        'white',
        'pink',
        'brown',
    ],
    'animals': [
        'cat',
        'dog',
        'horse',
        'rabbit',
        'lion',
        'tiger',
        'zebra',
        'bear',
        'fox',
        'elephant',
    ],
    'tools': [
        'hammer',
        'screwdriver',
        'wrench',
        'drill',
        'saw',
        'pliers',
        'level',
        'tape measure',
    ],
}

COMMA_LIST_PROMPTS = {
    'three': [
        'List exactly three {category}, separated by commas.',
        'Name exactly three {category}, separated by commas.',
        'Give exactly three {category}. Use commas and no extra text.',
        'Provide exactly three {category}, separated only by commas.'
    ]
}

ONE_SENTENCE_TOPICS = {
    'rain': [
        'Rain falls from clouds and helps plants grow.',
        'Rain brings water to rivers, lakes, and soil.',
        'Rain is water that falls from clouds to the ground.',
    ],
    'snow': [
        'Snow is frozen water that falls from clouds in cold weather.',
        'Snow can cover the ground when the air is cold enough.',
        'Snow often makes the world look quiet and bright.',
    ],
    'sleep': [
        'Sleep helps the body rest, recover, and store memories.',
        'Sleep gives the brain and body time to recharge.',
        'Good sleep can help people feel more focused and healthy.',
    ],
    'music': [
        'Music uses sound and rhythm to express feelings.',
        'Music can make people feel calm, happy, or excited.',
        'Music is a creative way to share emotion and ideas.',
    ],
    'books': [
        'Books can teach facts, tell stories, and spark imagination.',
        'Reading books helps people learn new ideas.',
        'Books let readers explore places and thoughts beyond their own lives.',
    ],
    'dogs': [
        'Dogs are loyal animals that often enjoy spending time with people.',
        'Dogs can be playful, friendly, and protective companions.',
        'Many dogs like walking, running, and playing with their owners.',
    ],
    'cats': [
        'Cats are curious animals that often enjoy quiet places.',
        'Cats can be independent, playful, and affectionate.',
        'Many cats like to climb, nap, and explore their surroundings.',
    ],
    'trees': [
        'Trees provide shade, oxygen, and homes for many animals.',
        'Trees grow from roots and reach upward toward sunlight.',
        'Trees are important because they support life in many environments.',
    ],
    'flowers': [
        'Flowers often have bright colors and pleasant smells.',
        'Flowers help some plants reproduce by attracting pollinators.',
        'Flowers can make gardens and parks look beautiful.',
    ],
    'the ocean': [
        'The ocean is a vast body of salt water filled with life.',
        'The ocean covers much of Earth and affects weather around the world.',
        'The ocean is home to fish, whales, coral, and many other living things.',
    ],
    'mountains': [
        'Mountains rise high above the land and can shape the weather.',
        'Mountains are large landforms that often have steep slopes.',
        'Mountains can be beautiful places for hiking and exploration.',
    ],
    'the sun': [
        'The sun gives Earth light and warmth.',
        'The sun is the star at the center of our solar system.',
        'Sunlight helps plants grow and keeps Earth warm enough for life.',
    ],
    'the moon': [
        'The moon orbits Earth and reflects sunlight at night.',
        'The moon changes appearance as it moves around Earth.',
        'The moon affects ocean tides through its gravity.',
    ],
    'stars': [
        'Stars are huge balls of hot gas that shine in space.',
        'Stars give off light because of powerful reactions in their cores.',
        'Stars can help people understand the history of the universe.',
    ],
    'space': [
        'Space is the vast area beyond Earth and its atmosphere.',
        'Space contains stars, planets, moons, galaxies, and dust.',
        'Space exploration helps people learn more about the universe.',
    ],
    'school': [
        'School is a place where people learn skills and ideas.',
        'School helps students practice reading, writing, math, and teamwork.',
        'A good school can help students grow in knowledge and confidence.',
    ],
    'friendship': [
        'Friendship is built on kindness, trust, and shared time.',
        'A good friendship can make people feel supported and understood.',
        'Friendship grows when people listen to and care for each other.',
    ],
    'kindness': [
        'Kindness means treating others with care and respect.',
        'Small acts of kindness can make someone’s day better.',
        'Kindness helps people feel valued and supported.',
    ],
    'cooking': [
        'Cooking turns ingredients into meals people can enjoy.',
        'Cooking can be practical, creative, and fun.',
        'Good cooking often depends on timing, heat, and simple ingredients.',
    ],
    'exercise': [
        'Exercise helps keep the body strong and healthy.',
        'Regular exercise can improve energy, mood, and fitness.',
        'Exercise includes activities like walking, running, swimming, and stretching.',
    ],
    'water': [
        'Water is essential for life on Earth.',
        'Water helps people, animals, and plants survive.',
        'Clean water is important for drinking, cooking, and health.',
    ],
    'fire': [
        'Fire gives heat and light but must be handled carefully.',
        'Fire can cook food, warm homes, and also cause danger.',
        'Fire needs heat, fuel, and oxygen to keep burning.',
    ],
    'computers': [
        'Computers are machines that process information and run programs.',
        'Computers help people write, calculate, communicate, and create.',
        'A computer follows instructions to store and transform data.',
    ],
    'robots': [
        'Robots are machines designed to perform tasks automatically.',
        'Robots can help with work that is repetitive, difficult, or dangerous.',
        'Some robots move through the world while others work inside computers.',
    ],
    'GPUs': [
        'A GPU is a chip that can perform many calculations at the same time.',
        'GPUs are useful for graphics, games, and machine learning.',
        'A GPU helps computers process large amounts of data quickly.',
    ],
    'bicycles': [
        'A bicycle is a vehicle with two wheels powered by pedaling.',
        'Bicycles are useful for exercise, travel, and recreation.',
        'Riding a bicycle can be a simple and efficient way to move around.',
    ],
    'gardens': [
        'Gardens are places where people grow plants, flowers, or food.',
        'A garden can provide beauty, fresh air, and quiet enjoyment.',
        'Gardens need sunlight, water, soil, and care.',
    ],
    'coffee': [
        'Coffee is a drink made from roasted coffee beans.',
        'Many people drink coffee because it tastes rich and contains caffeine.',
        'Coffee can be served hot, cold, black, or with milk.',
    ],
    'tea': [
        'Tea is a drink made by steeping leaves or herbs in hot water.',
        'Tea can taste calming, bitter, sweet, or floral depending on the type.',
        'Many people drink tea for comfort, flavor, or relaxation.',
    ],
    'penguins': [
        'Penguins are birds that cannot fly but swim very well.',
        'Penguins use their wings like flippers to move through water.',
        'Many penguins live in cold places and eat fish or krill.',
    ],
}

ONE_SENTENCE_PROMPTS = [
    'Write exactly one sentence about {topic}.',
    'Describe {topic} in exactly one sentence.',
    'Give one short sentence about {topic}.',
    'Write one sentence only about {topic}.',
    'In exactly one sentence, explain {topic}.',
]

REWRITES = [
    (
        'The thing was bad because it was not good.',
        'The item was poor quality.',
    ),
    (
        'He went to the place where the thing happened.',
        'He went to the location where the event occurred.',
    ),
    (
        'The food was nice and I liked it a lot.',
        'I really enjoyed the food.',
    ),
    (
        'This is a thing that people use to do work.',
        'This is a tool people use for work.',
    ),
    (
        'The meeting was long and it took a lot of time.',
        'The meeting took too long.',
    ),
    (
        'She was happy because the result was good.',
        'She was pleased with the result.',
    ),
    (
        'The instructions were confusing and hard to understand.',
        'The instructions were unclear.',
    ),
    (
        'The plan did not work because it failed.',
        'The plan was unsuccessful.',
    ),
    (
        'He said the same thing again and again many times.',
        'He repeated himself many times.',
    ),
    (
        'The room was very cold and not warm at all.',
        'The room was very cold.',
    ),
    (
        'I need help with the problem that I am having.',
        'I need help with my problem.',
    ),
    (
        'The movie was interesting and kept my attention.',
        'The movie was engaging.',
    ),
    (
        'The answer was not correct and had mistakes.',
        'The answer was incorrect.',
    ),
    (
        'She spoke in a way that was easy to understand.',
        'She spoke clearly.',
    ),
    (
        'The house was big and had a lot of space.',
        'The house was spacious.',
    ),
    (
        'He made a decision very quickly without thinking much.',
        'He made a hasty decision.',
    ),
    (
        'The weather was bad because it rained all day.',
        'It rained all day, making the weather unpleasant.',
    ),
    (
        'The test was hard and difficult to finish.',
        'The test was difficult to finish.',
    ),
    (
        'The dog ran fast across the field.',
        'The dog sprinted across the field.',
    ),
    (
        'The car made a loud sound when it started.',
        'The car made a loud noise when it started.',
    ),
    (
        'She gave me information that was useful.',
        'She gave me useful information.',
    ),
    (
        'The book was about a person who went on a trip.',
        'The book was about a traveler.',
    ),
    (
        'The company made changes to make the product better.',
        'The company improved the product.',
    ),
    (
        'The phone stopped working and would not turn on.',
        'The phone stopped working and would not power on.',
    ),
    (
        'He was tired because he did not sleep enough.',
        'He was tired from lack of sleep.',
    ),
    (
        'The project was completed before the time it was due.',
        'The project was completed before the deadline.',
    ),
    (
        'The teacher explained the idea in a simple way.',
        'The teacher explained the idea simply.',
    ),
    (
        'The path was hard to see because it was dark.',
        'The path was difficult to see in the dark.',
    ),
    (
        'She fixed the mistake that was in the document.',
        'She corrected the mistake in the document.',
    ),
    (
        'The game was fun and made people excited.',
        'The game was exciting and fun.',
    ),
    (
        'The water was too hot to drink right away.',
        'The water was too hot to drink immediately.',
    ),
    (
        'He asked a question that was important.',
        'He asked an important question.',
    ),
    (
        'The computer was slow and took a long time to respond.',
        'The computer responded slowly.',
    ),
    (
        'The message was not clear and could be misunderstood.',
        'The message was unclear.',
    ),
    (
        'They worked together to solve the problem.',
        'They collaborated to solve the problem.',
    ),
    (
        'The shop is open during the hours of the morning.',
        'The shop is open in the morning.',
    ),
    (
        'She looked at the paper carefully to find mistakes.',
        'She reviewed the paper carefully for mistakes.',
    ),
    (
        'The train arrived later than the time it was supposed to arrive.',
        'The train arrived late.',
    ),
    (
        'He was not able to find his keys.',
        'He could not find his keys.',
    ),
    (
        'The city has many buildings that are very tall.',
        'The city has many tall buildings.',
    ),
    (
        'The cake tasted sweet and was nice to eat.',
        'The cake was sweet and delicious.',
    ),
    (
        'The task was easy and did not take much effort.',
        'The task was easy.',
    ),
    (
        'She gave a reply after a short amount of time.',
        'She replied quickly.',
    ),
    (
        'The river moved slowly through the valley.',
        'The river flowed slowly through the valley.',
    ),
    (
        'He used his phone to send a message to his friend.',
        'He texted his friend.',
    ),
    (
        'The idea was new and different from the usual ideas.',
        'The idea was original.',
    ),
    (
        'The child was scared because the noise was loud.',
        'The loud noise frightened the child.',
    ),
    (
        'The report includes details about what happened.',
        'The report describes what happened.',
    ),
    (
        'She was kind and helped the person who needed help.',
        'She kindly helped the person in need.',
    ),
    (
        'The bag was heavy because it had many books inside.',
        'The bag was heavy with books.',
    ),
]

REWRITE_PROMPTS = [
    (
        'Rewrite this sentence to be clearer:\n'
        '{bad}\n'
        'Only provide the rewritten sentence.'
    ),
    (
        'Make this sentence clearer:\n'
        '{bad}\n'
        'Only provide the improved sentence.'
    ),
    (
        'Rewrite the following sentence clearly:\n'
        '{bad}\n'
        'Do not explain your answer.'
    ),
    (
        'Improve this sentence:\n'
        '{bad}\n'
        'Only output the improved sentence.'
    ),
    (
        'Make the following sentence more concise:\n'
        '{bad}\n'
        'Only provide the revised sentence.'
    ),
]

GRAMMAR_CORRECTIONS = [
    ("He don't like apples.", "He doesn't like apples."),
    ('She go to school every day.', 'She goes to school every day.'),
    ('They was happy.', 'They were happy.'),
    ('I has a book.', 'I have a book.'),
    ('The cats is sleeping.', 'The cats are sleeping.'),

    ('He have a red bicycle.', 'He has a red bicycle.'),
    ("She don't want any tea.", "She doesn't want any tea."),
    ('We was at the park yesterday.', 'We were at the park yesterday.'),
    ('They is ready to leave.', 'They are ready to leave.'),
    ('I were tired after work.', 'I was tired after work.'),

    ('The dog run fast.', 'The dog runs fast.'),
    ('The birds sings every morning.', 'The birds sing every morning.'),
    ('My friends likes pizza.', 'My friends like pizza.'),
    ('This books are heavy.', 'These books are heavy.'),
    ('Those car is expensive.', 'That car is expensive.'),

    ('She have finished her homework.', 'She has finished her homework.'),
    ('He were going to the store.', 'He was going to the store.'),
    ('They has three cats.', 'They have three cats.'),
    ('We goes there often.', 'We go there often.'),
    ('I likes this song.', 'I like this song.'),

    ('There is many reasons to try.', 'There are many reasons to try.'),
    ('There are a problem with the file.', 'There is a problem with the file.'),
    ('There is two chairs in the room.', 'There are two chairs in the room.'),
    ('There are one answer left.', 'There is one answer left.'),
    ('There was many people outside.', 'There were many people outside.'),

    ('Me and John went to the store.', 'John and I went to the store.'),
    ('Her and I are friends.', 'She and I are friends.'),
    ('Him and Sarah finished the project.', 'He and Sarah finished the project.'),
    ('Us are going to the beach.', 'We are going to the beach.'),
    ('Them are waiting outside.', 'They are waiting outside.'),

    ('I seen the movie yesterday.', 'I saw the movie yesterday.'),
    ('She seen him at school.', 'She saw him at school.'),
    ('They wented to the park.', 'They went to the park.'),
    ('He eated breakfast early.', 'He ate breakfast early.'),
    ('We runned home quickly.', 'We ran home quickly.'),

    ('I have went there before.', 'I have gone there before.'),
    ('She has wrote the letter.', 'She has written the letter.'),
    ('They have ate lunch already.', 'They have eaten lunch already.'),
    ('He has saw that show.', 'He has seen that show.'),
    ('We have ran this route before.', 'We have run this route before.'),

    ('The child are playing outside.', 'The child is playing outside.'),
    ('The children is playing outside.', 'The children are playing outside.'),
    ('The mouse are under the table.', 'The mouse is under the table.'),
    ('The mice is under the table.', 'The mice are under the table.'),
    ('The person are waiting.', 'The person is waiting.'),

    ('Each student have a notebook.', 'Each student has a notebook.'),
    ('Everyone are invited.', 'Everyone is invited.'),
    ('Somebody have left their bag.', 'Somebody has left their bag.'),
    ('Nobody know the answer.', 'Nobody knows the answer.'),
    ('Every book are on the shelf.', 'Every book is on the shelf.'),

    ('She is more taller than me.', 'She is taller than me.'),
    ('This is the most easiest question.', 'This is the easiest question.'),
    ('He is more faster than his brother.', 'He is faster than his brother.'),
    ('That was the most worst day.', 'That was the worst day.'),
    ('This bag is more heavier than that one.', 'This bag is heavier than that one.'),

    ('I did not went to school.', 'I did not go to school.'),
    ('She does not likes coffee.', 'She does not like coffee.'),
    ('He did not saw the sign.', 'He did not see the sign.'),
    ('They do not wants help.', 'They do not want help.'),
    ('We did not knew the answer.', 'We did not know the answer.'),

    ('Can you helps me?', 'Can you help me?'),
    ('She can sings well.', 'She can sing well.'),
    ('He should goes home.', 'He should go home.'),
    ('They must finishes today.', 'They must finish today.'),
    ('We will eats soon.', 'We will eat soon.'),

    ('I am good at to swim.', 'I am good at swimming.'),
    ('She enjoys to read books.', 'She enjoys reading books.'),
    ('He avoided to answer the question.', 'He avoided answering the question.'),
    ('They finished to clean the room.', 'They finished cleaning the room.'),
    ('We discussed about the plan.', 'We discussed the plan.'),

    ('I am interested on science.', 'I am interested in science.'),
    ('She is afraid from spiders.', 'She is afraid of spiders.'),
    ('He is good in math.', 'He is good at math.'),
    ('They arrived to the station.', 'They arrived at the station.'),
    ('We listened the song.', 'We listened to the song.'),

    ('The keys is on the table.', 'The keys are on the table.'),
    ('The news are surprising.', 'The news is surprising.'),
    ('My glasses is broken.', 'My glasses are broken.'),
    ('The scissors is sharp.', 'The scissors are sharp.'),
    ('The team are winning the game.', 'The team is winning the game.'),

    ('This are my shoes.', 'These are my shoes.'),
    ('These is my jacket.', 'This is my jacket.'),
    ('That are your bag.', 'That is your bag.'),
    ('Those is their books.', 'Those are their books.'),
    ('This apples taste sweet.', 'These apples taste sweet.'),

    ('She speaks very good English.', 'She speaks English very well.'),
    ('He did the test good.', 'He did well on the test.'),
    ('The car runs smooth.', 'The car runs smoothly.'),
    ('She sings beautiful.', 'She sings beautifully.'),
    ('He answered the question correct.', 'He answered the question correctly.'),

    ('I have less books than you.', 'I have fewer books than you.'),
    ('There are less people here today.', 'There are fewer people here today.'),
    ('She made fewer progress than expected.', 'She made less progress than expected.'),
    ('He drank fewer water than usual.', 'He drank less water than usual.'),
    ('We need less chairs for the room.', 'We need fewer chairs for the room.'),

    ('Its raining outside.', "It's raining outside."),
    ('Your going to like this.', "You're going to like this."),
    ('Their coming over later.', "They're coming over later."),
    ("The dog wagged it's tail.", 'The dog wagged its tail.'),
    ("I don't know weather to go.", "I don't know whether to go."),

    ('She bought too apples.', 'She bought two apples.'),
    ('I want to much food.', 'I want too much food.'),
    ('He is taller then me.', 'He is taller than me.'),
    ('Please sit over their.', 'Please sit over there.'),
    ('They went too the store.', 'They went to the store.'),

    ('The sentence need a period', 'The sentence needs a period.'),
    ('where are you going?', 'Where are you going?'),
    ('i like apples.', 'I like apples.'),
    ('She said, i am ready.', 'She said, I am ready.'),
    ('my name is tendril.', 'My name is Tendril.'),
]

GRAMMAR_PROMPTS = [
    (
        'Correct the grammar of this sentence:\n'
        '{bad}\n'
        'Only provide the corrected sentence.'
    ),
    (
        'Fix the grammar:\n'
        '{bad}\n'
        'Only provide the corrected sentence.'
    ),
    (
        'Correct this sentence and provide only the corrected version:\n'
        '{bad}'
    ),
    (
        'Rewrite this sentence with correct grammar:\n'
        '{bad}\n'
        'Do not explain your answer.'
    ),
    (
        'Fix the grammatical error in this sentence:\n'
        '{bad}\n'
        'Only output the fixed sentence.'
    ),
]

PROCEDURES = [
    (
        'cooking a boiled egg',
        [
            'Place the egg in a pot and cover it with water.',
            'Bring the water to a boil, then simmer for 9 to 12 minutes.',
            'Cool the egg in cold water, then peel it.',
        ],
    ),
    (
        'brushing your teeth',
        [
            'Put toothpaste on a toothbrush.',
            'Brush all sides of your teeth for about two minutes.',
            'Rinse your mouth and toothbrush with water.',
        ],
    ),
    (
        'making toast',
        [
            'Place a slice of bread in the toaster.',
            'Toast it until it is golden brown.',
            'Remove it carefully and add butter or another topping.',
        ],
    ),
    (
        'making a cup of tea',
        [
            'Boil fresh water.',
            'Steep the tea bag or leaves in the hot water.',
            'Remove the tea and serve it.',
        ],
    ),
    (
        'making instant coffee',
        [
            'Add instant coffee to a mug.',
            'Pour in hot water and stir.',
            'Add milk or sugar if desired.',
        ],
    ),
    (
        'washing your hands',
        [
            'Wet your hands with clean water and apply soap.',
            'Scrub your hands for at least 20 seconds.',
            'Rinse and dry your hands.',
        ],
    ),
    (
        'charging a phone',
        [
            'Plug the charger into a power outlet.',
            'Connect the cable to the phone.',
            'Wait until the battery has enough charge.',
        ],
    ),
    (
        'sending an email',
        [
            'Write the recipient, subject, and message.',
            'Review the email for mistakes.',
            'Click send.',
        ],
    ),
    (
        'saving a document',
        [
            'Open the file menu or save command.',
            'Choose a folder and file name.',
            'Confirm the save action.',
        ],
    ),
    (
        'packing a school bag',
        [
            'Check which books and supplies you need.',
            'Place the items neatly in the bag.',
            'Close the bag and make sure nothing is missing.',
        ],
    ),
    (
        'planting a seed',
        [
            'Fill a small pot with soil.',
            'Place the seed in the soil and cover it lightly.',
            'Water the soil and put the pot in a suitable place.',
        ],
    ),
    (
        'watering a houseplant',
        [
            'Check whether the soil feels dry.',
            'Pour water slowly onto the soil.',
            'Stop when the soil is moist but not flooded.',
        ],
    ),
    (
        'cleaning a desk',
        [
            'Remove items that do not belong on the desk.',
            'Wipe the surface with a clean cloth.',
            'Put the useful items back neatly.',
        ],
    ),
    (
        'making a sandwich',
        [
            'Place your chosen filling between two slices of bread.',
            'Add any sauce or vegetables you want.',
            'Cut the sandwich if desired and serve it.',
        ],
    ),
    (
        'making a bowl of cereal',
        [
            'Pour cereal into a bowl.',
            'Add milk or another drink of your choice.',
            'Eat it with a spoon.',
        ],
    ),
    (
        'tying your shoes',
        [
            'Cross the laces and pull them tight.',
            'Make a loop with one lace and wrap the other lace around it.',
            'Pull the second lace through to form a knot.',
        ],
    ),
    (
        'folding a shirt',
        [
            'Lay the shirt flat with the front facing down.',
            'Fold the sides inward toward the center.',
            'Fold the shirt from bottom to top.',
        ],
    ),
    (
        'washing a cup',
        [
            'Rinse the cup with warm water.',
            'Scrub it with soap and a sponge.',
            'Rinse off the soap and let the cup dry.',
        ],
    ),
    (
        'taking a screenshot',
        [
            'Open the screen you want to capture.',
            'Press the screenshot shortcut on your device.',
            'Save or share the captured image.',
        ],
    ),
    (
        'setting an alarm',
        [
            'Open the clock or alarm app.',
            'Choose the time you want the alarm to ring.',
            'Save or turn on the alarm.',
        ],
    ),
    (
        'joining a video call',
        [
            'Open the meeting link or app.',
            'Check your camera and microphone settings.',
            'Join the call at the scheduled time.',
        ],
    ),
    (
        'printing a document',
        [
            'Open the document you want to print.',
            'Choose the printer and print settings.',
            'Start the print job.',
        ],
    ),
    (
        'changing a password',
        [
            'Open the account security settings.',
            'Enter your current password and a new password.',
            'Save the change.',
        ],
    ),
    (
        'creating a new folder',
        [
            'Open the location where you want the folder.',
            'Choose the option to create a new folder.',
            'Name the folder and save it.',
        ],
    ),
    (
        'renaming a file',
        [
            'Select the file you want to rename.',
            'Choose the rename option.',
            'Type the new name and confirm it.',
        ],
    ),
    (
        'checking the weather',
        [
            'Open a weather app or website.',
            'Enter your location if needed.',
            'Read the forecast for the time you need.',
        ],
    ),
    (
        'planning a short walk',
        [
            'Choose a safe route and destination.',
            'Check the weather and wear suitable shoes.',
            'Bring anything you need and start walking.',
        ],
    ),
    (
        'feeding a pet',
        [
            'Check the correct food and portion size.',
            'Place the food in a clean bowl.',
            'Give the bowl to the pet and provide fresh water.',
        ],
    ),
    (
        'cleaning your glasses',
        [
            'Rinse the lenses with clean water.',
            'Apply lens cleaner or mild soap.',
            'Dry them gently with a microfiber cloth.',
        ],
    ),
    (
        'making a simple salad',
        [
            'Wash and chop the vegetables.',
            'Place them in a bowl.',
            'Add dressing and toss the salad.',
        ],
    ),
    (
        'boiling pasta',
        [
            'Bring a pot of salted water to a boil.',
            'Add the pasta and cook until tender.',
            'Drain the pasta and serve it.',
        ],
    ),
    (
        'heating soup',
        [
            'Pour the soup into a pot or microwave-safe bowl.',
            'Heat it until it is hot throughout.',
            'Stir carefully and serve it.',
        ],
    ),
    (
        'making scrambled eggs',
        [
            'Beat the eggs in a bowl.',
            'Cook them in a heated pan while stirring.',
            'Remove them when they are soft and fully cooked.',
        ],
    ),
    (
        'preparing rice',
        [
            'Rinse the rice if needed.',
            'Cook it with the correct amount of water.',
            'Let it rest briefly before serving.',
        ],
    ),
    (
        'washing fruit',
        [
            'Hold the fruit under clean running water.',
            'Rub the surface gently with your hands.',
            'Dry the fruit before eating or cutting it.',
        ],
    ),
    (
        'making lemonade',
        [
            'Squeeze fresh lemon juice into a pitcher.',
            'Add water and sugar to taste.',
            'Stir well and serve chilled.',
        ],
    ),
    (
        'organizing a bookshelf',
        [
            'Remove books that do not belong there.',
            'Group the remaining books by size, topic, or author.',
            'Place the books neatly back on the shelf.',
        ],
    ),
    (
        'cleaning a mirror',
        [
            'Spray glass cleaner onto the mirror or cloth.',
            'Wipe the mirror in smooth strokes.',
            'Dry any streaks with a clean cloth.',
        ],
    ),
    (
        'making a grocery list',
        [
            'Check what food and supplies you already have.',
            'Write down the items you need.',
            'Group similar items together before shopping.',
        ],
    ),
    (
        'preparing for bed',
        [
            'Brush your teeth and wash your face.',
            'Set an alarm if you need one.',
            'Turn off distractions and get into bed.',
        ],
    ),
    (
        'studying for a quiz',
        [
            'Review the main notes or textbook sections.',
            'Practice questions about the topic.',
            'Rest briefly and review mistakes.',
        ],
    ),
    (
        'writing a short paragraph',
        [
            'Choose the main idea you want to explain.',
            'Write a few sentences that support the idea.',
            'Read it again and fix unclear wording.',
        ],
    ),
    (
        'summarizing an article',
        [
            'Read the article carefully.',
            'Identify the main point and key details.',
            'Write a shorter version in your own words.',
        ],
    ),
    (
        'checking a math answer',
        [
            'Review each step of your calculation.',
            'Look for arithmetic or copying mistakes.',
            'Compare the result with the original question.',
        ],
    ),
    (
        'backing up files',
        [
            'Choose the files you want to protect.',
            'Copy them to cloud storage or an external drive.',
            'Check that the backup was saved correctly.',
        ],
    ),
    (
        'cleaning a keyboard',
        [
            'Turn off or unplug the keyboard.',
            'Remove loose dust and crumbs carefully.',
            'Wipe the keys with a slightly damp cloth.',
        ],
    ),
    (
        'setting up a workspace',
        [
            'Choose a clean and comfortable place to work.',
            'Arrange the tools and materials you need.',
            'Remove distractions before you begin.',
        ],
    ),
    (
        'starting a simple workout',
        [
            'Warm up with light movement.',
            'Do a few basic exercises at a safe pace.',
            'Cool down and stretch gently.',
        ],
    ),
    (
        'washing a car window',
        [
            'Spray the window with glass cleaner.',
            'Wipe the glass with a clean cloth.',
            'Dry the window to remove streaks.',
        ],
    ),
    (
        'preparing a backpack for travel',
        [
            'Choose the items you need for the trip.',
            'Pack heavy items first and lighter items on top.',
            'Check the bag before leaving.',
        ],
    ),
]

PROCEDURE_PROMPTS = [
    'Give exactly three numbered steps for {task}.',
    'Explain {task} in exactly three numbered steps.',
    'Provide exactly three numbered steps for {task}. Do not add extra text.',
    'List exactly three numbered steps for {task}.',
    'Describe how to do {task} in exactly three numbered steps.',
]

ANCHOR_CONSTRAINT_EXAMPLES = [
    (
        'Who are you? Answer in one short sentence.',
        'I am Tendril, a helpful AI assistant.'
    ),
    (
        'What is the capital of France? Answer in one short sentence.',
        'The capital of France is Paris.'
    ),
    (
        'Give exactly three numbered steps for cooking a boiled egg.',
        '1. Place the egg in a pot and cover it with water.\n'
        '2. Bring the water to a boil, then simmer for 9 to 12 minutes.\n'
        '3. Cool the egg in cold water, then peel it.'
    ),
    (
        'Write exactly one sentence about rain.',
        'Rain falls from clouds and helps plants grow.'
    ),
    (
        'Rewrite this sentence to be clearer:\n'
        'The thing was bad because it was not good.\n'
        'Only provide the rewritten sentence.',
        'The item was poor quality.'
    ),
    (
        'List exactly three fruits, separated by commas.',
        'apple, banana, orange'
    ),
    (
        'Explain what a GPU is in simple words. Use at most two short sentences.',
        'A GPU is a computer chip that handles many calculations at once. It is useful for graphics and AI.'
    ),
    (
        'Write one short friendly reply to this message:\n'
        'Can we meet tomorrow?',
        'Sure, tomorrow works for me.'
    ),
    (
        'Summarize this in one sentence:\n'
        'Penguins are birds that cannot fly but are excellent swimmers.',
        'Penguins are flightless birds that swim very well.'
    ),
    (
        'Correct the grammar of this sentence:\n'
        "He don't like apples.\n"
        'Only provide the corrected sentence.',
        "He doesn't like apples."
    ),
]

FRIENDLY_REPLIES = [
    (
        'Can we meet tomorrow?',
        'Sure, tomorrow works for me.'
    ),
    (
        'Thanks for your help!',
        "You're welcome, happy to help!"
    ),
    (
        'I might be a few minutes late.',
        'No worries, thanks for letting me know.'
    ),
    (
        'Can you send me the notes later?',
        'Sure, I can send them later.'
    ),
    (
        'I finished the task.',
        'Great work, thanks for finishing it.'
    ),
    (
        'Sorry, I forgot to reply earlier.',
        'No problem, thanks for getting back to me.'
    ),
    (
        'Do you want to grab coffee this afternoon?',
        'Sure, coffee this afternoon sounds good.'
    ),
    (
        'I am feeling nervous about the meeting.',
        "You've got this, and I hope it goes well."
    ),
    (
        'Can we move the call to Friday?',
        'Sure, Friday works for me.'
    ),
    (
        'Happy birthday!',
        'Thank you, that is very kind of you.'
    ),
    (
        'I passed the exam!',
        "That's wonderful news, congratulations!"
    ),
    (
        'Can you check this when you have time?',
        'Of course, I will take a look when I can.'
    ),
    (
        'I need to cancel today.',
        'No problem, we can find another time.'
    ),
    (
        'Good luck with your presentation.',
        'Thank you, I really appreciate it.'
    ),
    (
        'Are you free this weekend?',
        'Yes, I should be free this weekend.'
    ),
]

ONE_SENTENCE_SUMMARIES = [
    (
        'Penguins are birds that cannot fly but are excellent swimmers.',
        'Penguins are flightless birds that swim very well.'
    ),
    (
        'The library closes at six, so we need to return the books before then.',
        'We need to return the books before the library closes at six.'
    ),
    (
        'Solar panels turn sunlight into electricity that people can use in homes and buildings.',
        'Solar panels convert sunlight into usable electricity.'
    ),
    (
        'Maria missed the bus, so she walked to school and arrived ten minutes late.',
        'Maria walked to school and arrived late after missing the bus.'
    ),
    (
        'Plants need sunlight, water, and nutrients from the soil to grow.',
        'Plants need sunlight, water, and soil nutrients to grow.'
    ),
    (
        'The team practiced every day and improved enough to win the final match.',
        'Daily practice helped the team improve and win the final match.'
    ),
    (
        'A password manager stores your passwords securely so you do not have to remember each one.',
        'A password manager securely stores passwords for you.'
    ),
    (
        'The storm brought heavy rain and strong winds, causing several roads to flood.',
        'The storm caused flooding with heavy rain and strong winds.'
    ),
    (
        'Exercise can strengthen muscles, improve mood, and support long-term health.',
        'Exercise supports health by strengthening the body and improving mood.'
    ),
    (
        'The new train route will make travel between the two cities faster and easier.',
        'The new train route will make city-to-city travel faster and easier.'
    ),
    (
        'The recipe uses flour, eggs, milk, and butter to make soft pancakes.',
        'The recipe combines simple ingredients to make soft pancakes.'
    ),
    (
        'The company delayed the product launch because it found a bug during final testing.',
        'The company delayed the launch after finding a final testing bug.'
    ),
]

SIMPLE_EXPLANATIONS = [
    (
        'Explain what a GPU is in simple words. Use at most two short sentences.',
        'A GPU is a computer chip that handles many calculations at once. It is useful for graphics and AI.'
    ),
    (
        'Explain what a CPU is in simple words. Use at most two short sentences.',
        'A CPU is the main chip that runs instructions in a computer. It helps control what the computer does.'
    ),
    (
        'Explain what RAM is in simple words. Use at most two short sentences.',
        'RAM is short-term memory a computer uses while it is working. It helps programs run quickly.'
    ),
    (
        'Explain what the internet is in simple words. Use at most two short sentences.',
        'The internet is a huge network that connects computers around the world. It lets people share information.'
    ),
    (
        'Explain what a database is in simple words. Use at most two short sentences.',
        'A database is an organized place to store information. It helps people find and update data easily.'
    ),
    (
        'Explain what an algorithm is in simple words. Use at most two short sentences.',
        'An algorithm is a set of steps for solving a problem. A computer can follow those steps to do a task.'
    ),
    (
        'Explain what a token is in simple words. Use at most two short sentences.',
        'A token is a small piece of text, like a word or part of a word. Language models read and write tokens.'
    ),
    (
        'Explain what a neural network is in simple words. Use at most two short sentences.',
        'A neural network is a computer system that learns patterns from data. It can use those patterns to make predictions.'
    ),
    (
        'Explain what machine learning is in simple words. Use at most two short sentences.',
        'Machine learning teaches computers to learn patterns from examples. It helps them make predictions or decisions.'
    ),
    (
        'Explain what an app is in simple words. Use at most two short sentences.',
        'An app is a program you use on a phone or computer. It helps you do a specific task.'
    ),
    (
        'Explain what cloud storage is in simple words. Use at most two short sentences.',
        'Cloud storage keeps your files on remote computers. You can access them through the internet.'
    ),
    (
        'Explain what electricity is in simple words. Use at most two short sentences.',
        'Electricity is energy that moves through wires. It powers lights, machines, and devices.'
    ),
]
