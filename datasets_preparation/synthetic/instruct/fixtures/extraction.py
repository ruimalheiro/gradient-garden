EXTRACTION_FIXTURES = {
    'name': {
        'prompt_templates': [
            'Extract the name from this sentence:\n{sentence}\nOnly provide the extracted name.',
            'Extract the name from this sentence: {sentence}',
            'Return only the name from this sentence:\n{sentence}',
            'What name appears in this sentence?\n{sentence}\nOnly provide the name.',
            'Find the person name in this sentence:\n{sentence}\nOnly output the name.',
        ],
        'examples': [
            {'sentence': 'Maria went to the store.', 'answer': 'Maria'},
            {
                'sentence': 'Daniel called his friend after lunch.',
                'answer': 'Daniel',
            },
            {'sentence': 'Sofia opened the window.', 'answer': 'Sofia'},
            {'sentence': 'Lucas finished the homework.', 'answer': 'Lucas'},
            {'sentence': 'Emma walked to the library.', 'answer': 'Emma'},
            {'sentence': 'Noah waited outside the school.', 'answer': 'Noah'},
            {
                'sentence': 'Olivia baked a cake for the party.',
                'answer': 'Olivia',
            },
            {
                'sentence': 'Liam brought a notebook to class.',
                'answer': 'Liam',
            },
            {'sentence': 'Ana sent the report yesterday.', 'answer': 'Ana'},
            {'sentence': 'Miguel fixed the broken chair.', 'answer': 'Miguel'},
            {'sentence': 'Rui lives near the station.', 'answer': 'Rui'},
            {'sentence': 'Clara answered the question.', 'answer': 'Clara'},
            {'sentence': 'Pedro closed the door quietly.', 'answer': 'Pedro'},
            {'sentence': 'Mia carried the bag upstairs.', 'answer': 'Mia'},
            {'sentence': 'Ethan wrote a short poem.', 'answer': 'Ethan'},
        ],
    },
    'city': {
        'prompt_templates': [
            'Extract the city from this sentence:\n{sentence}\nOnly provide the extracted city.',
            'Extract the city from this sentence: {sentence}',
            'Return only the city from this sentence:\n{sentence}',
            'What city appears in this sentence?\n{sentence}\nOnly provide the city.',
            'Find the city name in this sentence:\n{sentence}\nOnly output the city.',
        ],
        'examples': [
            {'sentence': 'Rui lives in London.', 'answer': 'London'},
            {
                'sentence': 'The conference will happen in Paris.',
                'answer': 'Paris',
            },
            {
                'sentence': 'Maria moved to Lisbon last year.',
                'answer': 'Lisbon',
            },
            {
                'sentence': 'The train arrived in Berlin at noon.',
                'answer': 'Berlin',
            },
            {
                'sentence': 'We visited Madrid during spring.',
                'answer': 'Madrid',
            },
            {
                'sentence': 'The meeting is scheduled in Rome.',
                'answer': 'Rome',
            },
            {'sentence': 'She booked a hotel in Tokyo.', 'answer': 'Tokyo'},
            {
                'sentence': 'The team flew to Dublin for the event.',
                'answer': 'Dublin',
            },
            {
                'sentence': 'He studied in Barcelona for a semester.',
                'answer': 'Barcelona',
            },
            {
                'sentence': 'The concert takes place in Vienna.',
                'answer': 'Vienna',
            },
            {
                'sentence': 'They opened a new office in Amsterdam.',
                'answer': 'Amsterdam',
            },
            {
                'sentence': 'The workshop will be held in Zurich.',
                'answer': 'Zurich',
            },
            {'sentence': 'I met my friend in Prague.', 'answer': 'Prague'},
            {
                'sentence': 'The museum is located in Athens.',
                'answer': 'Athens',
            },
            {'sentence': 'Her flight landed in Toronto.', 'answer': 'Toronto'},
        ],
    },
    'date': {
        'prompt_templates': [
            'Extract the date from this sentence:\n{sentence}\nOnly provide the extracted date.',
            'Extract the date from this sentence: {sentence}',
            'Return only the date from this sentence:\n{sentence}',
            'What date appears in this sentence?\n{sentence}\nOnly provide the date.',
            'Find the date in this sentence:\n{sentence}\nOnly output the date.',
        ],
        'examples': [
            {'sentence': 'The meeting is on June 12.', 'answer': 'June 12'},
            {
                'sentence': 'The deadline is September 3.',
                'answer': 'September 3',
            },
            {'sentence': 'The event starts on April 9.', 'answer': 'April 9'},
            {
                'sentence': 'The exam is scheduled for May 15.',
                'answer': 'May 15',
            },
            {
                'sentence': 'The package arrives on July 20.',
                'answer': 'July 20',
            },
            {
                'sentence': 'The class begins on October 1.',
                'answer': 'October 1',
            },
            {'sentence': 'The trip ends on August 22.', 'answer': 'August 22'},
            {
                'sentence': 'The concert is on December 5.',
                'answer': 'December 5',
            },
            {
                'sentence': 'The form is due on January 31.',
                'answer': 'January 31',
            },
            {
                'sentence': 'The workshop happens on March 14.',
                'answer': 'March 14',
            },
            {
                'sentence': 'The appointment is set for November 8.',
                'answer': 'November 8',
            },
            {
                'sentence': 'The sale begins on February 2.',
                'answer': 'February 2',
            },
        ],
    },
    'number': {
        'prompt_templates': [
            'Extract the number from this sentence:\n{sentence}\nOnly provide the extracted number.',
            'Extract the number from this sentence: {sentence}',
            'Return only the number from this sentence:\n{sentence}',
            'What number appears in this sentence?\n{sentence}\nOnly provide the number.',
            'Find the number in this sentence:\n{sentence}\nOnly output the number.',
        ],
        'examples': [
            {'sentence': 'There are 27 books on the shelf.', 'answer': '27'},
            {'sentence': 'The box contains 48 pencils.', 'answer': '48'},
            {
                'sentence': 'She bought 12 apples at the market.',
                'answer': '12',
            },
            {'sentence': 'The class has 30 students.', 'answer': '30'},
            {'sentence': 'He scored 95 points in the game.', 'answer': '95'},
            {'sentence': 'The recipe needs 4 eggs.', 'answer': '4'},
            {'sentence': 'The train leaves from platform 6.', 'answer': '6'},
            {'sentence': 'The room has 18 chairs.', 'answer': '18'},
            {'sentence': 'The ticket costs 15 pounds.', 'answer': '15'},
            {'sentence': 'The building has 9 floors.', 'answer': '9'},
            {'sentence': 'The team won 3 matches.', 'answer': '3'},
            {'sentence': 'The garden has 21 flowers.', 'answer': '21'},
        ],
    },
    'email': {
        'prompt_templates': [
            'Extract the email address from this sentence:\n{sentence}\nOnly provide the extracted email address.',
            'Extract the email address from this sentence: {sentence}',
            'Return only the email address from this sentence:\n{sentence}',
            'What email address appears in this sentence?\n{sentence}\nOnly provide the email address.',
            'Find the email address in this sentence:\n{sentence}\nOnly output the email address.',
        ],
        'examples': [
            {
                'sentence': 'Please contact ana@example.com for details.',
                'answer': 'ana@example.com',
            },
            {
                'sentence': 'Send the file to rui@example.org.',
                'answer': 'rui@example.org',
            },
            {
                'sentence': 'The support address is help@site.com.',
                'answer': 'help@site.com',
            },
            {
                'sentence': 'Email the team at team@example.net.',
                'answer': 'team@example.net',
            },
            {
                'sentence': 'Questions can go to info@company.com.',
                'answer': 'info@company.com',
            },
            {
                'sentence': 'My address is maria@test.com.',
                'answer': 'maria@test.com',
            },
            {
                'sentence': 'Use admin@school.org for login help.',
                'answer': 'admin@school.org',
            },
            {
                'sentence': 'The newsletter comes from news@example.com.',
                'answer': 'news@example.com',
            },
            {
                'sentence': 'You can reach me at alex@domain.co.',
                'answer': 'alex@domain.co',
            },
            {
                'sentence': 'Forward it to office@example.org.',
                'answer': 'office@example.org',
            },
        ],
    },
    'color': {
        'prompt_templates': [
            'Extract the color from this sentence:\n{sentence}\nOnly provide the extracted color.',
            'Extract the color from this sentence: {sentence}',
            'Return only the color from this sentence:\n{sentence}',
            'What color appears in this sentence?\n{sentence}\nOnly provide the color.',
            'Find the color in this sentence:\n{sentence}\nOnly output the color.',
        ],
        'examples': [
            {'sentence': 'The car is painted red.', 'answer': 'red'},
            {'sentence': 'She wore a blue jacket.', 'answer': 'blue'},
            {'sentence': 'The door was green.', 'answer': 'green'},
            {'sentence': 'He picked the yellow flower.', 'answer': 'yellow'},
            {'sentence': 'The cat slept on a black chair.', 'answer': 'black'},
            {'sentence': 'The walls are white.', 'answer': 'white'},
            {'sentence': 'I bought a purple notebook.', 'answer': 'purple'},
            {
                'sentence': 'The orange cup is on the table.',
                'answer': 'orange',
            },
            {
                'sentence': 'The sky looked gray before the storm.',
                'answer': 'gray',
            },
            {'sentence': 'She chose a pink ribbon.', 'answer': 'pink'},
            {'sentence': 'The brown dog ran outside.', 'answer': 'brown'},
            {
                'sentence': 'The silver watch was on the desk.',
                'answer': 'silver',
            },
        ],
    },
    'animal': {
        'prompt_templates': [
            'Extract the animal from this sentence:\n{sentence}\nOnly provide the extracted animal.',
            'Extract the animal from this sentence: {sentence}',
            'Return only the animal from this sentence:\n{sentence}',
            'What animal appears in this sentence?\n{sentence}\nOnly provide the animal.',
            'Find the animal in this sentence:\n{sentence}\nOnly output the animal.',
        ],
        'examples': [
            {
                'sentence': 'The rabbit jumped over the fence.',
                'answer': 'rabbit',
            },
            {'sentence': 'A dog barked near the gate.', 'answer': 'dog'},
            {'sentence': 'The cat slept on the sofa.', 'answer': 'cat'},
            {'sentence': 'A horse ran across the field.', 'answer': 'horse'},
            {'sentence': 'The bird landed on the branch.', 'answer': 'bird'},
            {
                'sentence': 'A turtle crossed the path slowly.',
                'answer': 'turtle',
            },
            {
                'sentence': 'The elephant walked through the grass.',
                'answer': 'elephant',
            },
            {
                'sentence': 'A dolphin swam beside the boat.',
                'answer': 'dolphin',
            },
            {'sentence': 'The fox hid behind the tree.', 'answer': 'fox'},
            {'sentence': 'A sheep stood near the barn.', 'answer': 'sheep'},
            {'sentence': 'The lion rested under the tree.', 'answer': 'lion'},
            {
                'sentence': 'A bear walked through the forest.',
                'answer': 'bear',
            },
        ],
    },
    'food': {
        'prompt_templates': [
            'Extract the food from this sentence:\n{sentence}\nOnly provide the extracted food.',
            'Extract the food from this sentence: {sentence}',
            'Return only the food from this sentence:\n{sentence}',
            'What food appears in this sentence?\n{sentence}\nOnly provide the food.',
            'Find the food in this sentence:\n{sentence}\nOnly output the food.',
        ],
        'examples': [
            {'sentence': 'She ate pasta for dinner.', 'answer': 'pasta'},
            {'sentence': 'He made rice for lunch.', 'answer': 'rice'},
            {'sentence': 'The child wanted pizza.', 'answer': 'pizza'},
            {'sentence': 'They served soup at the cafe.', 'answer': 'soup'},
            {'sentence': 'I packed an apple in my bag.', 'answer': 'apple'},
            {
                'sentence': 'The sandwich was on the plate.',
                'answer': 'sandwich',
            },
            {'sentence': 'She cooked eggs for breakfast.', 'answer': 'eggs'},
            {
                'sentence': 'He bought bread from the bakery.',
                'answer': 'bread',
            },
            {
                'sentence': 'The salad had tomatoes and lettuce.',
                'answer': 'salad',
            },
            {
                'sentence': 'We ordered noodles for dinner.',
                'answer': 'noodles',
            },
            {'sentence': 'The cake was on the table.', 'answer': 'cake'},
            {'sentence': 'He drank milk with breakfast.', 'answer': 'milk'},
        ],
    },
    'country': {
        'prompt_templates': [
            'Extract the country from this sentence:\n{sentence}\nOnly provide the extracted country.',
            'Extract the country from this sentence: {sentence}',
            'Return only the country from this sentence:\n{sentence}',
            'What country appears in this sentence?\n{sentence}\nOnly provide the country.',
            'Find the country in this sentence:\n{sentence}\nOnly output the country.',
        ],
        'examples': [
            {
                'sentence': 'He traveled to Portugal last summer.',
                'answer': 'Portugal',
            },
            {'sentence': 'She moved to Spain in March.', 'answer': 'Spain'},
            {
                'sentence': 'The team visited France for the match.',
                'answer': 'France',
            },
            {
                'sentence': 'They flew to Germany for a conference.',
                'answer': 'Germany',
            },
            {'sentence': 'I learned about Japan in class.', 'answer': 'Japan'},
            {'sentence': 'The package came from Italy.', 'answer': 'Italy'},
            {
                'sentence': 'He studied in Canada for two years.',
                'answer': 'Canada',
            },
            {'sentence': 'The film was made in Brazil.', 'answer': 'Brazil'},
            {
                'sentence': 'She bought coffee from Colombia.',
                'answer': 'Colombia',
            },
            {
                'sentence': 'The singer was born in Ireland.',
                'answer': 'Ireland',
            },
            {'sentence': 'They spent winter in Norway.', 'answer': 'Norway'},
            {
                'sentence': 'The article mentioned Australia.',
                'answer': 'Australia',
            },
        ],
    },
    'month': {
        'prompt_templates': [
            'Extract the month from this sentence:\n{sentence}\nOnly provide the extracted month.',
            'Extract the month from this sentence: {sentence}',
            'Return only the month from this sentence:\n{sentence}',
            'What month appears in this sentence?\n{sentence}\nOnly provide the month.',
            'Find the month in this sentence:\n{sentence}\nOnly output the month.',
        ],
        'examples': [
            {'sentence': 'The event happens in April.', 'answer': 'April'},
            {'sentence': 'The course starts in January.', 'answer': 'January'},
            {'sentence': 'The festival is planned for May.', 'answer': 'May'},
            {
                'sentence': 'The deadline falls in September.',
                'answer': 'September',
            },
            {'sentence': 'The trip begins in July.', 'answer': 'July'},
            {'sentence': 'The shop opens in November.', 'answer': 'November'},
            {'sentence': 'The exam is in March.', 'answer': 'March'},
            {
                'sentence': 'The concert happens in December.',
                'answer': 'December',
            },
            {'sentence': 'The flowers bloom in June.', 'answer': 'June'},
            {'sentence': 'The class ends in October.', 'answer': 'October'},
            {'sentence': 'The sale starts in February.', 'answer': 'February'},
            {'sentence': 'The holiday is in August.', 'answer': 'August'},
        ],
    },
    'time': {
        'prompt_templates': [
            'Extract the time from this sentence:\n{sentence}\nOnly provide the extracted time.',
            'Extract the time from this sentence: {sentence}',
            'Return only the time from this sentence:\n{sentence}',
            'What time appears in this sentence?\n{sentence}\nOnly provide the time.',
            'Find the time in this sentence:\n{sentence}\nOnly output the time.',
        ],
        'examples': [
            {'sentence': 'The train leaves at 8:30.', 'answer': '8:30'},
            {'sentence': 'The meeting starts at 10:00.', 'answer': '10:00'},
            {'sentence': 'Class begins at 9:15.', 'answer': '9:15'},
            {'sentence': 'Dinner is at 7:00.', 'answer': '7:00'},
            {'sentence': 'The movie starts at 6:45.', 'answer': '6:45'},
            {'sentence': 'The bus arrives at 12:20.', 'answer': '12:20'},
            {'sentence': 'The call is scheduled for 3:30.', 'answer': '3:30'},
            {'sentence': 'The shop closes at 5:00.', 'answer': '5:00'},
            {'sentence': 'The alarm rings at 6:10.', 'answer': '6:10'},
            {'sentence': 'The flight departs at 14:25.', 'answer': '14:25'},
            {'sentence': 'Practice starts at 4:15.', 'answer': '4:15'},
            {'sentence': 'The webinar begins at 11:45.', 'answer': '11:45'},
        ],
    },
}
