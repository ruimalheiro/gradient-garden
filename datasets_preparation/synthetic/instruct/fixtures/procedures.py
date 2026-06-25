PROCEDURE_FIXTURES = {
    'three_step': {
        'prompt_templates': [
            'Give exactly three numbered steps for {task}.',
            'Give exactly three numbered steps for {task}. Stop after step 3.',
            'Give exactly three numbered steps for {task}. Do not add extra text.',
            'Explain {task} in exactly three numbered steps. Stop after step 3.',
            'Provide exactly three numbered steps for {task}. Do not add extra text.',
            'List exactly three numbered steps for {task}. Do not include anything after step 3.',
            'Describe {task} in exactly three numbered steps. Only provide the steps.',
            'Answer with exactly three numbered steps for {task}.',
        ],
        'examples': [
            {
                'task': 'cooking a boiled egg',
                'steps': [
                    'Place the egg in a pot and cover it with water.',
                    'Bring the water to a boil, then simmer for 9 to 12 minutes.',
                    'Cool the egg in cold water, then peel it.',
                ],
            },
            {
                'task': 'brushing your teeth',
                'steps': [
                    'Put toothpaste on a toothbrush.',
                    'Brush all sides of your teeth for about two minutes.',
                    'Rinse your mouth and toothbrush with water.',
                ],
            },
            {
                'task': 'making toast',
                'steps': [
                    'Place a slice of bread in the toaster.',
                    'Toast it until it is golden brown.',
                    'Remove it carefully and add butter or another topping.',
                ],
            },
            {
                'task': 'making a cup of tea',
                'steps': [
                    'Boil fresh water.',
                    'Steep the tea bag or leaves in the hot water.',
                    'Remove the tea and serve it.',
                ],
            },
            {
                'task': 'making instant coffee',
                'steps': [
                    'Add instant coffee to a mug.',
                    'Pour in hot water and stir.',
                    'Add milk or sugar if desired.',
                ],
            },
            {
                'task': 'washing your hands',
                'steps': [
                    'Wet your hands with clean water and apply soap.',
                    'Scrub your hands for at least 20 seconds.',
                    'Rinse and dry your hands.',
                ],
            },
            {
                'task': 'charging a phone',
                'steps': [
                    'Plug the charger into a power outlet.',
                    'Connect the cable to the phone.',
                    'Wait until the battery has enough charge.',
                ],
            },
            {
                'task': 'sending an email',
                'steps': [
                    'Write the recipient, subject, and message.',
                    'Review the email for mistakes.',
                    'Click send.',
                ],
            },
            {
                'task': 'saving a document',
                'steps': [
                    'Open the file menu or save command.',
                    'Choose a folder and file name.',
                    'Confirm the save action.',
                ],
            },
            {
                'task': 'packing a school bag',
                'steps': [
                    'Check which books and supplies you need.',
                    'Place the items neatly in the bag.',
                    'Close the bag and make sure nothing is missing.',
                ],
            },
            {
                'task': 'planting a seed',
                'steps': [
                    'Fill a small pot with soil.',
                    'Place the seed in the soil and cover it lightly.',
                    'Water the soil and put the pot in a suitable place.',
                ],
            },
            {
                'task': 'watering a houseplant',
                'steps': [
                    'Check whether the soil feels dry.',
                    'Pour water slowly onto the soil.',
                    'Stop when the soil is moist but not flooded.',
                ],
            },
            {
                'task': 'cleaning a desk',
                'steps': [
                    'Remove items that do not belong on the desk.',
                    'Wipe the surface with a clean cloth.',
                    'Put the useful items back neatly.',
                ],
            },
            {
                'task': 'making a sandwich',
                'steps': [
                    'Place your chosen filling between two slices of bread.',
                    'Add any sauce or vegetables you want.',
                    'Cut the sandwich if desired and serve it.',
                ],
            },
            {
                'task': 'making a bowl of cereal',
                'steps': [
                    'Pour cereal into a bowl.',
                    'Add milk or another drink of your choice.',
                    'Eat it with a spoon.',
                ],
            },
            {
                'task': 'tying your shoes',
                'steps': [
                    'Cross the laces and pull them tight.',
                    'Make a loop with one lace and wrap the other lace around it.',
                    'Pull the second lace through to form a knot.',
                ],
            },
            {
                'task': 'folding a shirt',
                'steps': [
                    'Lay the shirt flat with the front facing down.',
                    'Fold the sides inward toward the center.',
                    'Fold the shirt from bottom to top.',
                ],
            },
            {
                'task': 'washing a cup',
                'steps': [
                    'Rinse the cup with warm water.',
                    'Scrub it with soap and a sponge.',
                    'Rinse off the soap and let the cup dry.',
                ],
            },
            {
                'task': 'taking a screenshot',
                'steps': [
                    'Open the screen you want to capture.',
                    'Press the screenshot shortcut on your device.',
                    'Save or share the captured image.',
                ],
            },
            {
                'task': 'setting an alarm',
                'steps': [
                    'Open the clock or alarm app.',
                    'Choose the time you want the alarm to ring.',
                    'Save or turn on the alarm.',
                ],
            },
            {
                'task': 'joining a video call',
                'steps': [
                    'Open the meeting link or app.',
                    'Check your camera and microphone settings.',
                    'Join the call at the scheduled time.',
                ],
            },
            {
                'task': 'printing a document',
                'steps': [
                    'Open the document you want to print.',
                    'Choose the printer and print settings.',
                    'Start the print job.',
                ],
            },
            {
                'task': 'changing a password',
                'steps': [
                    'Open the account security settings.',
                    'Enter your current password and a new password.',
                    'Save the change.',
                ],
            },
            {
                'task': 'creating a new folder',
                'steps': [
                    'Open the location where you want the folder.',
                    'Choose the option to create a new folder.',
                    'Name the folder and save it.',
                ],
            },
            {
                'task': 'renaming a file',
                'steps': [
                    'Select the file you want to rename.',
                    'Choose the rename option.',
                    'Type the new name and confirm it.',
                ],
            },
            {
                'task': 'checking the weather',
                'steps': [
                    'Open a weather app or website.',
                    'Enter your location if needed.',
                    'Read the forecast for the time you need.',
                ],
            },
            {
                'task': 'planning a short walk',
                'steps': [
                    'Choose a safe route and destination.',
                    'Check the weather and wear suitable shoes.',
                    'Bring anything you need and start walking.',
                ],
            },
            {
                'task': 'feeding a pet',
                'steps': [
                    'Check the correct food and portion size.',
                    'Place the food in a clean bowl.',
                    'Give the bowl to the pet and provide fresh water.',
                ],
            },
            {
                'task': 'cleaning your glasses',
                'steps': [
                    'Rinse the lenses with clean water.',
                    'Apply lens cleaner or mild soap.',
                    'Dry them gently with a microfiber cloth.',
                ],
            },
            {
                'task': 'making a simple salad',
                'steps': [
                    'Wash and chop the vegetables.',
                    'Place them in a bowl.',
                    'Add dressing and toss the salad.',
                ],
            },
            {
                'task': 'boiling pasta',
                'steps': [
                    'Bring a pot of salted water to a boil.',
                    'Add the pasta and cook until tender.',
                    'Drain the pasta and serve it.',
                ],
            },
            {
                'task': 'heating soup',
                'steps': [
                    'Pour the soup into a pot or microwave-safe bowl.',
                    'Heat it until it is hot throughout.',
                    'Stir carefully and serve it.',
                ],
            },
            {
                'task': 'making scrambled eggs',
                'steps': [
                    'Beat the eggs in a bowl.',
                    'Cook them in a heated pan while stirring.',
                    'Remove them when they are soft and fully cooked.',
                ],
            },
            {
                'task': 'preparing rice',
                'steps': [
                    'Rinse the rice if needed.',
                    'Cook it with the correct amount of water.',
                    'Let it rest briefly before serving.',
                ],
            },
            {
                'task': 'washing fruit',
                'steps': [
                    'Hold the fruit under clean running water.',
                    'Rub the surface gently with your hands.',
                    'Dry the fruit before eating or cutting it.',
                ],
            },
            {
                'task': 'making lemonade',
                'steps': [
                    'Squeeze fresh lemon juice into a pitcher.',
                    'Add water and sugar to taste.',
                    'Stir well and serve chilled.',
                ],
            },
            {
                'task': 'organizing a bookshelf',
                'steps': [
                    'Remove books that do not belong there.',
                    'Group the remaining books by size, topic, or author.',
                    'Place the books neatly back on the shelf.',
                ],
            },
            {
                'task': 'cleaning a mirror',
                'steps': [
                    'Spray glass cleaner onto the mirror or cloth.',
                    'Wipe the mirror in smooth strokes.',
                    'Dry any streaks with a clean cloth.',
                ],
            },
            {
                'task': 'making a grocery list',
                'steps': [
                    'Check what food and supplies you already have.',
                    'Write down the items you need.',
                    'Group similar items together before shopping.',
                ],
            },
            {
                'task': 'preparing for bed',
                'steps': [
                    'Brush your teeth and wash your face.',
                    'Set an alarm if you need one.',
                    'Turn off distractions and get into bed.',
                ],
            },
            {
                'task': 'studying for a quiz',
                'steps': [
                    'Review the main notes or textbook sections.',
                    'Practice questions about the topic.',
                    'Rest briefly and review mistakes.',
                ],
            },
            {
                'task': 'writing a short paragraph',
                'steps': [
                    'Choose the main idea you want to explain.',
                    'Write a few sentences that support the idea.',
                    'Read it again and fix unclear wording.',
                ],
            },
            {
                'task': 'summarizing an article',
                'steps': [
                    'Read the article carefully.',
                    'Identify the main point and key details.',
                    'Write a shorter version in your own words.',
                ],
            },
            {
                'task': 'checking a math answer',
                'steps': [
                    'Review each step of your calculation.',
                    'Look for arithmetic or copying mistakes.',
                    'Compare the result with the original question.',
                ],
            },
            {
                'task': 'backing up files',
                'steps': [
                    'Choose the files you want to protect.',
                    'Copy them to cloud storage or an external drive.',
                    'Check that the backup was saved correctly.',
                ],
            },
            {
                'task': 'cleaning a keyboard',
                'steps': [
                    'Turn off or unplug the keyboard.',
                    'Remove loose dust and crumbs carefully.',
                    'Wipe the keys with a slightly damp cloth.',
                ],
            },
            {
                'task': 'setting up a workspace',
                'steps': [
                    'Choose a clean and comfortable place to work.',
                    'Arrange the tools and materials you need.',
                    'Remove distractions before you begin.',
                ],
            },
            {
                'task': 'starting a simple workout',
                'steps': [
                    'Warm up with light movement.',
                    'Do a few basic exercises at a safe pace.',
                    'Cool down and stretch gently.',
                ],
            },
            {
                'task': 'washing a car window',
                'steps': [
                    'Spray the window with glass cleaner.',
                    'Wipe the glass with a clean cloth.',
                    'Dry the window to remove streaks.',
                ],
            },
            {
                'task': 'preparing a backpack for travel',
                'steps': [
                    'Choose the items you need for the trip.',
                    'Pack heavy items first and lighter items on top.',
                    'Check the bag before leaving.',
                ],
            },
        ],
    },
    'strict_eval_tasks': {
        'examples': [
            {
                'prompt': 'Give exactly three numbered steps for cooking a boiled egg.',
                'answer': '1. Place the egg in a pot and cover it with water.\n2. Boil the water, then simmer the egg for 9 to 12 minutes.\n3. Cool the egg in cold water, then peel it.',
            },
            {
                'prompt': 'Give exactly three numbered steps for making toast.',
                'answer': '1. Place a slice of bread in the toaster.\n2. Toast it until it is golden brown.\n3. Remove it carefully and add butter or another topping.',
            },
            {
                'prompt': 'Give exactly three numbered steps for brushing your teeth.',
                'answer': '1. Put toothpaste on a toothbrush.\n2. Brush all sides of your teeth for about two minutes.\n3. Rinse your mouth and toothbrush with water.',
            },
            {
                'prompt': 'Give exactly three numbered steps for making a cup of tea.',
                'answer': '1. Boil fresh water.\n2. Steep the tea bag or leaves in the hot water.\n3. Remove the tea and serve it.',
            },
            {
                'prompt': 'Give exactly three numbered steps for washing your hands.',
                'answer': '1. Wet your hands with clean water and apply soap.\n2. Scrub your hands for at least 20 seconds.\n3. Rinse and dry your hands.',
            },
            {
                'prompt': 'Give exactly three numbered steps for sending an email.',
                'answer': '1. Write the recipient, subject, and message.\n2. Review the email for mistakes.\n3. Click send.',
            },
            {
                'prompt': 'Give exactly three numbered steps for planting a seed.',
                'answer': '1. Fill a small pot with soil.\n2. Place the seed in the soil and cover it lightly.\n3. Water the soil and put the pot in a suitable place.',
            },
            {
                'prompt': 'Give exactly three numbered steps for charging a phone.',
                'answer': '1. Plug the charger into a power outlet.\n2. Connect the cable to the phone.\n3. Wait until the battery has enough charge.',
            },
            {
                'prompt': 'Give exactly three numbered steps for taking a screenshot.',
                'answer': '1. Open the screen you want to capture.\n2. Press the screenshot shortcut on your device.\n3. Save or share the captured image.',
            },
            {
                'prompt': 'Give exactly three numbered steps for making rice.',
                'answer': '1. Rinse the rice if needed.\n2. Cook it with the correct amount of water.\n3. Let it rest briefly before serving.',
            },
            {
                'prompt': 'Give exactly three numbered steps for saving a document.',
                'answer': '1. Open the document you want to save.\n2. Choose the save option and select a location.\n3. Name the file and confirm the save.',
            },
            {
                'prompt': 'Give exactly three numbered steps for checking the weather.',
                'answer': '1. Open a weather app or website.\n2. Enter your location if needed.\n3. Read the forecast for the time you need.',
            },
            {
                'prompt': 'Give exactly three numbered steps for making a sandwich.',
                'answer': '1. Place your chosen filling between two slices of bread.\n2. Add any sauce or vegetables you want.\n3. Cut the sandwich if desired and serve it.',
            },
            {
                'prompt': 'Give exactly three numbered steps for washing fruit.',
                'answer': '1. Hold the fruit under clean running water.\n2. Rub the surface gently with your hands.\n3. Dry the fruit before eating or cutting it.',
            },
            {
                'prompt': 'Give exactly three numbered steps for backing up files.',
                'answer': '1. Choose the files you want to protect.\n2. Copy them to cloud storage or an external drive.\n3. Check that the backup was saved correctly.',
            },
        ],
    },
}
