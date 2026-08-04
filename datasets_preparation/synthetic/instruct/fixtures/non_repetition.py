_NUMBERED_TWO_REASON_TEMPLATES = [
    'Give exactly two different reasons to {action}. Use a numbered list.',
    'List two distinct reasons to {action}. Number them 1 and 2.',
    'Provide two non-overlapping reasons to {action}. Use only a numbered list.',
    'In exactly two numbered points, explain why someone should {action}.',
    'Name two separate reasons to {action}; output only items 1 and 2.',
]


_NUMBERED_TWO_REASON_RECORDS = [
    (
        'drink water',
        'It replaces fluid lost through normal activity.',
        'It helps the body regulate temperature.',
    ),
    (
        'sleep well',
        'Sleep gives the body time to recover.',
        'Sleep supports memory and concentration.',
    ),
    (
        'exercise regularly',
        'Exercise strengthens muscles and bones.',
        'Exercise can improve mood.',
    ),
    (
        'read books',
        'Books can introduce new ideas and information.',
        'Reading can provide entertainment.',
    ),
    (
        'save money',
        'Savings can cover unexpected expenses.',
        'Savings can fund future goals.',
    ),
    (
        'wash your hands',
        'Washing removes visible dirt.',
        'Washing can reduce the spread of germs.',
    ),
    (
        'wear a coat in winter',
        'A coat reduces heat loss from the body.',
        'A coat can block cold wind.',
    ),
    (
        'learn mathematics',
        'Mathematics helps with everyday calculations.',
        'Mathematics supports many scientific and technical fields.',
    ),
    (
        'eat a variety of vegetables',
        'Vegetables provide vitamins and minerals.',
        'Their fiber can support digestion.',
    ),
    (
        'back up important files',
        'A backup can replace files lost after device failure.',
        'A backup can restore an earlier version after an accidental change.',
    ),
    (
        'plan ahead',
        'Planning clarifies the actions a task requires.',
        'Planning makes deadlines and dependencies easier to notice.',
    ),
    (
        'practice a skill',
        'Practice improves accuracy and fluency.',
        'Practice reveals specific areas that still need work.',
    ),
    (
        'proofread a message before sending it',
        'Proofreading catches spelling and grammar errors.',
        'Proofreading can reveal an unclear or missing detail.',
    ),
    (
        'label storage boxes',
        'Labels make stored items easier to find.',
        'Labels reduce the need to open several boxes while searching.',
    ),
    (
        'use a strong unique password',
        'A strong password is harder to guess.',
        'A unique password limits damage if another account is compromised.',
    ),
    (
        'take short breaks during focused work',
        'A break can reduce mental fatigue.',
        'A break provides a chance to adjust posture and move.',
    ),
    (
        'check the weather before an outdoor trip',
        'The forecast helps you choose suitable clothing.',
        'Weather alerts may change the safest route or timing.',
    ),
    (
        'keep a written shopping list',
        'A list reduces the chance of forgetting needed items.',
        'A list can discourage unplanned purchases.',
    ),
    (
        'learn basic first aid',
        'It helps a person respond calmly to minor injuries.',
        'It helps a person recognize when professional help is needed.',
    ),
    (
        'review meeting notes afterward',
        'Review confirms which decisions were made.',
        'Review identifies assigned actions and deadlines.',
    ),
    (
        'keep frequently used tools organized',
        'Organization makes the correct tool faster to locate.',
        'Organization makes missing or damaged tools easier to notice.',
    ),
    (
        'wear a bicycle helmet',
        'A helmet can reduce the severity of some head injuries.',
        'The outer shell can help protect against cuts and abrasions.',
    ),
    (
        'update software from trusted sources',
        'Updates can fix known security weaknesses.',
        'Updates can correct bugs or improve compatibility.',
    ),
    (
        'ask clarifying questions',
        'Questions expose missing information.',
        'Questions reduce the risk of acting on a wrong assumption.',
    ),
]


_NUMBERED_THREE_REASON_TEMPLATES = [
    'Give exactly three different {request}. Use a numbered list.',
    'List three distinct {request}. Number the items 1 through 3.',
    'Provide exactly three non-repeating {request}. Use only a numbered list.',
    'Answer with three separate {request}, formatted as items 1, 2, and 3.',
    'Name exactly three {request}; do not add text outside the numbered list.',
]


_NUMBERED_THREE_REASON_RECORDS = [
    (
        'benefits of regular exercise',
        'It strengthens muscles and bones.',
        'It supports cardiovascular fitness.',
        'It can improve mood.',
    ),
    (
        'benefits of reading',
        'Reading can build vocabulary.',
        'Reading can teach new information.',
        'Reading can strengthen sustained attention.',
    ),
    (
        'ways to support general health',
        'Eat balanced meals.',
        'Be physically active regularly.',
        'Get enough sleep.',
    ),
    (
        'ways to be polite',
        'Use courteous language.',
        'Listen without interrupting.',
        "Respect other people's time.",
    ),
    (
        'reasons to learn programming',
        'Programming develops structured problem-solving skills.',
        'Programming enables people to build useful tools.',
        'Programming is relevant to many careers.',
    ),
    (
        'reasons to learn another language',
        'It enables communication with more people.',
        'It can make travel easier.',
        'It provides access to media and ideas in another language.',
    ),
    (
        'benefits of teamwork',
        'Teams can combine different expertise.',
        'Teams can divide a large workload.',
        'Teammates can review and support one another.',
    ),
    (
        'reasons to keep a schedule',
        'A schedule reserves time for important work.',
        'A schedule reduces missed appointments.',
        'A schedule makes competing priorities visible.',
    ),
    (
        'ways to save energy at home',
        'Turn off lights in empty rooms.',
        'Reduce unnecessary heating or cooling.',
        'Use energy-efficient appliances and bulbs.',
    ),
    (
        'reasons to ask questions',
        'Questions clarify confusing ideas.',
        'Questions uncover missing information.',
        'Questions test whether an assumption is correct.',
    ),
    (
        'benefits of adequate hydration',
        'Water replaces fluids lost by the body.',
        'Water helps regulate body temperature.',
        'Water supports normal digestion and circulation.',
    ),
    (
        'reasons to write notes',
        'Notes preserve important details.',
        'Notes make later review more efficient.',
        'The act of writing can reinforce memory.',
    ),
    (
        'risks of reusing one password everywhere',
        'One leaked password can expose several accounts.',
        'Attackers can try the same credentials on other services.',
        'Changing every affected account becomes more difficult.',
    ),
    (
        'causes of missed project deadlines',
        'The original estimate may be unrealistic.',
        'A required dependency may arrive late.',
        'Important work may lack a clear owner.',
    ),
    (
        'tools for taking simple notes',
        'Use a paper notebook.',
        'Use a plain-text editor.',
        'Use a voice recorder when speaking is more practical.',
    ),
    (
        'habits that support focused work',
        'Choose one specific task before starting.',
        'Silence nonessential notifications.',
        'Take planned breaks between work periods.',
    ),
    (
        'places suitable for quiet study',
        'Use a library reading room.',
        'Use an empty classroom when permitted.',
        'Use a quiet room at home.',
    ),
    (
        'objects useful on a rainy walk',
        'Carry an umbrella.',
        'Wear a waterproof outer layer.',
        'Use a water-resistant bag for valuables.',
    ),
    (
        'activities for a screen-free evening',
        'Read a printed book.',
        'Play a tabletop game.',
        'Take a walk in a safe area.',
    ),
    (
        'strategies for remembering appointments',
        'Add each appointment to a calendar immediately.',
        'Set a reminder before travel or preparation must begin.',
        'Review the next day’s schedule each evening.',
    ),
    (
        'benefits of labeling digital folders clearly',
        'Labels make related files easier to locate.',
        'Labels help distinguish active work from archives.',
        'Labels make shared folders easier for others to understand.',
    ),
    (
        'risks of opening unexpected attachments',
        'The file may contain malicious software.',
        'The message may be impersonating a trusted sender.',
        'The attachment may expose confidential information when opened or replied to.',
    ),
    (
        'causes of indoor clutter',
        'Items may lack assigned storage locations.',
        'Unneeded possessions may accumulate.',
        'Frequently used objects may not be returned after use.',
    ),
    (
        'tools for measuring a small room',
        'Use a tape measure for wall lengths.',
        'Use a laser measure for longer clear distances.',
        'Use a notepad to record dimensions and units.',
    ),
]


_BULLET_POINT_TEMPLATES = [
    'Give exactly {count} non-repeating bullet points about {topic}.',
    'List {count} distinct points about {topic}. Use bullet points only.',
    'Provide exactly {count} different bullets on {topic}; add no other text.',
    'Write {count} unique bullet points concerning {topic}.',
    'Answer with {count} separate bullets about {topic}, with no repeated idea.',
]


_BULLET_POINT_RECORDS = [
    (
        'why sleep matters',
        2,
        [
            'Sleep supports physical recovery.',
            'Sleep helps consolidate memories.',
            'Sleep supports attention and reaction time.',
            'Sleep helps regulate mood.',
        ],
    ),
    (
        'why water matters',
        2,
        [
            'Water replaces fluid lost by the body.',
            'Water helps regulate body temperature.',
            'Water supports digestion and circulation.',
            'Water helps transport dissolved nutrients and waste.',
        ],
    ),
    (
        'why exercise matters',
        2,
        [
            'Exercise strengthens muscles and bones.',
            'Exercise supports heart and lung fitness.',
            'Exercise can improve mood.',
            'Exercise helps maintain mobility.',
        ],
    ),
    (
        'why reading matters',
        2,
        [
            'Reading can expand vocabulary.',
            'Reading can teach new information.',
            'Reading can provide entertainment.',
            'Reading can strengthen sustained attention.',
        ],
    ),
    (
        'why saving money matters',
        2,
        [
            'Savings can cover emergencies.',
            'Savings can support future purchases.',
            'Savings can reduce reliance on borrowing.',
            'Savings can provide flexibility during income changes.',
        ],
    ),
    (
        'why handwashing matters',
        2,
        [
            'Handwashing removes visible dirt.',
            'Handwashing reduces many germs on the skin.',
            'Handwashing can limit contamination of food.',
            'Handwashing can reduce transmission between people and surfaces.',
        ],
    ),
    (
        'why checking work matters',
        2,
        [
            'Checking can catch calculation errors.',
            'Checking can reveal omitted requirements.',
            'Checking can identify unclear wording.',
            'Checking can catch accidental disclosure of private details.',
        ],
    ),
    (
        'why file backups matter',
        2,
        [
            'Backups can replace files lost after hardware failure.',
            'Backups can undo accidental deletion.',
            'Versioned backups can recover earlier content.',
            'Off-device backups can help after theft or physical damage.',
        ],
    ),
    (
        'why clear labels matter',
        2,
        [
            'Labels make items easier to find.',
            'Labels help people return items to the correct place.',
            'Labels distinguish similar containers or files.',
            'Labels can display dates or handling instructions.',
        ],
    ),
    (
        'why planning matters',
        2,
        [
            'Planning clarifies the desired outcome.',
            'Planning exposes missing resources.',
            'Planning makes dependencies visible.',
            'Planning helps reserve time for priority work.',
        ],
    ),
    (
        'risks of weak passwords',
        2,
        [
            'Weak passwords are easier to guess.',
            'Common passwords may appear in automated attack lists.',
            'A reused weak password can expose several accounts.',
            'A compromised account may reveal personal information.',
        ],
    ),
    (
        'causes of missed appointments',
        2,
        [
            'The event may not have been recorded.',
            'A reminder may have been set too late.',
            'Travel time may have been underestimated.',
            'A calendar may contain the wrong time zone.',
        ],
    ),
    (
        'benefits of a tidy workspace',
        2,
        [
            'Needed tools are easier to locate.',
            'Clear surfaces provide room to work.',
            'Removing clutter can reduce distractions.',
            'Visible damage or missing items are easier to notice.',
        ],
    ),
    (
        'safe habits when downloading files',
        2,
        [
            'Use a trusted source.',
            'Check the file name and type before opening it.',
            'Scan the file with available security tools.',
            'Avoid bypassing security warnings you do not understand.',
        ],
    ),
    (
        'ways to prepare for rain',
        2,
        [
            'Carry an umbrella.',
            'Wear a waterproof outer layer.',
            'Protect electronics in a water-resistant bag.',
            'Choose footwear with reliable grip.',
        ],
    ),
    (
        'why teamwork matters',
        3,
        [
            'Teams combine different expertise.',
            'Teams can divide a large workload.',
            'Teammates can review one another’s work.',
            'Teammates can provide support during setbacks.',
            'Discussion can reveal options one person missed.',
        ],
    ),
    (
        'why schools matter',
        3,
        [
            'Schools teach foundational knowledge and skills.',
            'Schools provide structured practice and feedback.',
            'Schools give students opportunities to work with peers.',
            'Schools can connect families with support services.',
            'Schools expose students to varied subjects and activities.',
        ],
    ),
    (
        'why libraries matter',
        3,
        [
            'Libraries provide access to books and other resources.',
            'Libraries offer places for quiet study.',
            'Libraries help people use information sources.',
            'Libraries host community learning activities.',
            'Libraries preserve local and historical materials.',
        ],
    ),
    (
        'why clean water matters',
        3,
        [
            'Clean water is safer to drink.',
            'Clean water supports food preparation.',
            'Clean water is needed for effective hygiene.',
            'Clean water reduces exposure to many contaminants.',
            'Clean water supports healthcare and sanitation.',
        ],
    ),
    (
        'benefits of keeping a schedule',
        3,
        [
            'A schedule reserves time for important tasks.',
            'A schedule reduces forgotten appointments.',
            'A schedule exposes conflicts before they occur.',
            'A schedule makes available time easier to estimate.',
            'A schedule helps coordinate work with other people.',
        ],
    ),
]


_COMMA_LIST_TEMPLATES = [
    'List exactly {count} different {category}, separated by commas.',
    'Name {count} unique {category}. Use commas only.',
    'Give {count} distinct {category} as a comma-separated list. Add no other text.',
    'Return only {count} non-repeating {category}, separated by commas.',
    'Provide a comma-only list of exactly {count} different {category}.',
]


_COMMA_FOUR_POOLS = [
    (
        'animals',
        ['cat', 'dog', 'horse', 'rabbit', 'lion', 'zebra', 'fox', 'bear'],
    ),
    (
        'fruits',
        ['apple', 'banana', 'orange', 'pear', 'mango', 'peach', 'grape', 'plum'],
    ),
    (
        'colors',
        ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'black', 'white'],
    ),
    (
        'vegetables',
        [
            'carrot',
            'onion',
            'broccoli',
            'spinach',
            'pepper',
            'cabbage',
            'pea',
            'celery',
        ],
    ),
    (
        'programming languages',
        ['Python', 'JavaScript', 'Rust', 'Java', 'Go', 'Ruby', 'Swift', 'Kotlin'],
    ),
    (
        'countries',
        ['Portugal', 'France', 'Japan', 'Canada', 'Kenya', 'Chile', 'India', 'Norway'],
    ),
    (
        'cities',
        ['London', 'Lisbon', 'Paris', 'Tokyo', 'Nairobi', 'Toronto', 'Oslo', 'Lima'],
    ),
    (
        'hand tools',
        [
            'hammer',
            'wrench',
            'pliers',
            'screwdriver',
            'chisel',
            'level',
            'mallet',
            'handsaw',
        ],
    ),
    (
        'sports',
        [
            'football',
            'tennis',
            'basketball',
            'swimming',
            'rugby',
            'cricket',
            'volleyball',
            'cycling',
        ],
    ),
    (
        'drinks',
        ['water', 'tea', 'coffee', 'juice', 'milk', 'lemonade', 'cocoa', 'smoothie'],
    ),
    (
        'vehicles',
        ['car', 'bus', 'train', 'bicycle', 'truck', 'tram', 'ferry', 'scooter'],
    ),
    (
        'planets',
        [
            'Mercury',
            'Venus',
            'Earth',
            'Mars',
            'Jupiter',
            'Saturn',
            'Uranus',
            'Neptune',
        ],
    ),
    (
        'trees',
        ['oak', 'maple', 'pine', 'birch', 'willow', 'cedar', 'beech', 'elm'],
    ),
    (
        'geometric shapes',
        [
            'circle',
            'triangle',
            'square',
            'rectangle',
            'pentagon',
            'hexagon',
            'oval',
            'trapezoid',
        ],
    ),
    (
        'materials',
        ['wood', 'glass', 'steel', 'rubber', 'cotton', 'ceramic', 'paper', 'leather'],
    ),
    (
        'occupations',
        [
            'teacher',
            'nurse',
            'carpenter',
            'chef',
            'engineer',
            'driver',
            'librarian',
            'gardener',
        ],
    ),
]


_COMMA_FIVE_POOLS = [
    (
        'household objects',
        [
            'chair',
            'table',
            'lamp',
            'spoon',
            'towel',
            'mirror',
            'blanket',
            'pillow',
            'plate',
        ],
    ),
    (
        'school supplies',
        [
            'pencil',
            'notebook',
            'ruler',
            'eraser',
            'folder',
            'pen',
            'marker',
            'glue',
            'scissors',
        ],
    ),
    (
        'modes of transport',
        [
            'car',
            'train',
            'bicycle',
            'bus',
            'plane',
            'tram',
            'ferry',
            'scooter',
            'subway',
        ],
    ),
    (
        'weather words',
        [
            'rain',
            'snow',
            'wind',
            'fog',
            'sunshine',
            'cloud',
            'thunder',
            'drizzle',
            'hail',
        ],
    ),
    (
        'body parts',
        ['hand', 'foot', 'arm', 'leg', 'head', 'eye', 'ear', 'nose', 'shoulder'],
    ),
    (
        'musical instruments',
        [
            'piano',
            'guitar',
            'violin',
            'drums',
            'flute',
            'trumpet',
            'cello',
            'clarinet',
            'harp',
        ],
    ),
    (
        'desserts',
        [
            'cake',
            'pie',
            'pudding',
            'brownie',
            'cookie',
            'sorbet',
            'custard',
            'tart',
            'mousse',
        ],
    ),
    (
        'jobs',
        [
            'teacher',
            'doctor',
            'engineer',
            'nurse',
            'chef',
            'mechanic',
            'designer',
            'farmer',
            'electrician',
        ],
    ),
    (
        'flowers',
        [
            'rose',
            'tulip',
            'daisy',
            'lily',
            'orchid',
            'sunflower',
            'violet',
            'iris',
            'poppy',
        ],
    ),
    (
        'kitchen utensils',
        [
            'spoon',
            'fork',
            'knife',
            'whisk',
            'spatula',
            'ladle',
            'tongs',
            'peeler',
            'grater',
        ],
    ),
    (
        'emotions',
        [
            'joy',
            'sadness',
            'anger',
            'fear',
            'surprise',
            'calm',
            'pride',
            'relief',
            'disappointment',
        ],
    ),
    (
        'clothing items',
        [
            'shirt',
            'coat',
            'trousers',
            'sock',
            'hat',
            'scarf',
            'glove',
            'dress',
            'sweater',
        ],
    ),
]


_COMMA_EXAMPLE_TEMPLATES = [
    'Give exactly three different examples of {category}, separated by commas.',
    'Name three unique examples of {category}. Use commas only.',
    'Provide three distinct examples of {category} as a comma-separated list.',
    'Return only three non-repeating examples of {category}, separated by commas.',
    'List exactly three examples of {category}; use commas and no extra text.',
]


_COMMA_THREE_POOLS = [
    (
        'healthy foods',
        ['apples', 'carrots', 'beans', 'oats', 'lentils', 'spinach', 'yogurt'],
    ),
    (
        'warm clothing',
        ['coat', 'scarf', 'gloves', 'sweater', 'hat', 'boots', 'thermal shirt'],
    ),
    (
        'things found in a kitchen',
        ['pan', 'plate', 'spoon', 'kettle', 'cutting board', 'cup', 'oven mitt'],
    ),
    (
        'classroom objects',
        ['desk', 'whiteboard', 'pencil', 'chair', 'textbook', 'ruler', 'projector'],
    ),
    (
        'things found in a garden',
        ['flowers', 'soil', 'seeds', 'shovel', 'watering can', 'compost', 'fence'],
    ),
    (
        'breakfast foods',
        ['eggs', 'toast', 'cereal', 'oatmeal', 'yogurt', 'fruit', 'pancakes'],
    ),
    (
        'outdoor activities',
        [
            'hiking',
            'cycling',
            'running',
            'gardening',
            'rowing',
            'birdwatching',
            'picnicking',
        ],
    ),
    (
        'computer parts',
        [
            'CPU',
            'GPU',
            'RAM',
            'motherboard',
            'storage drive',
            'power supply',
            'cooling fan',
        ],
    ),
    (
        'writing tools',
        ['pen', 'pencil', 'marker', 'chalk', 'stylus', 'crayon', 'fountain pen'],
    ),
    (
        'recyclable materials accepted in many programs',
        [
            'paper',
            'cardboard',
            'glass bottles',
            'steel cans',
            'aluminum cans',
            'plastic bottles',
            'newspapers',
        ],
    ),
    (
        'fruits',
        ['apple', 'mango', 'pear', 'peach', 'orange', 'plum', 'banana'],
    ),
    (
        'animals',
        ['cat', 'rabbit', 'horse', 'dog', 'fox', 'zebra', 'bear'],
    ),
    (
        'colors',
        ['red', 'green', 'purple', 'blue', 'yellow', 'orange', 'black'],
    ),
    (
        'sports',
        ['tennis', 'rugby', 'cricket', 'football', 'swimming', 'volleyball', 'cycling'],
    ),
    (
        'hand tools',
        ['hammer', 'pliers', 'level', 'wrench', 'screwdriver', 'chisel', 'mallet'],
    ),
    (
        'navigation aids',
        [
            'map',
            'compass',
            'road sign',
            'GPS receiver',
            'landmark',
            'route guide',
            'trail marker',
        ],
    ),
]


NON_REPETITION_FIXTURES = {
    'numbered_two_reasons': {
        'messages': [
            {
                'role': 'user',
                'content': list(_NUMBERED_TWO_REASON_TEMPLATES),
            },
            {
                'role': 'assistant',
                'content': '{answer}',
            },
        ],
        'examples': [
            {
                'action': action,
                'steps': [first_reason, second_reason],
            }
            for action, first_reason, second_reason in _NUMBERED_TWO_REASON_RECORDS
        ],
    },
    'numbered_three_reasons': {
        'messages': [
            {
                'role': 'user',
                'content': list(_NUMBERED_THREE_REASON_TEMPLATES),
            },
            {
                'role': 'assistant',
                'content': '{answer}',
            },
        ],
        'examples': [
            {
                'request': request,
                'steps': [first_item, second_item, third_item],
            }
            for request, first_item, second_item, third_item
            in _NUMBERED_THREE_REASON_RECORDS
        ],
    },
    'bullet_points': {
        'messages': [
            {
                'role': 'user',
                'content': list(_BULLET_POINT_TEMPLATES),
            },
            {
                'role': 'assistant',
                'content': '- {answer}',
            },
        ],
        'examples': [
            {
                'topic': topic,
                'count': count,
                'items': list(items),
                'separator': '\n- ',
            }
            for topic, count, items in _BULLET_POINT_RECORDS
        ],
    },
    'comma_lists_four': {
        'messages': [
            {
                'role': 'user',
                'content': list(_COMMA_LIST_TEMPLATES),
            },
            {
                'role': 'assistant',
                'content': '{answer}',
            },
        ],
        'examples': [
            {
                'category': category,
                'count': 4,
                'items': list(items),
                'separator': ', ',
            }
            for category, items in _COMMA_FOUR_POOLS
        ],
    },
    'comma_lists_five': {
        'messages': [
            {
                'role': 'user',
                'content': list(_COMMA_LIST_TEMPLATES),
            },
            {
                'role': 'assistant',
                'content': '{answer}',
            },
        ],
        'examples': [
            {
                'category': category,
                'count': 5,
                'items': list(items),
                'separator': ', ',
            }
            for category, items in _COMMA_FIVE_POOLS
        ],
    },
    'comma_examples_three': {
        'messages': [
            {
                'role': 'user',
                'content': list(_COMMA_EXAMPLE_TEMPLATES),
            },
            {
                'role': 'assistant',
                'content': '{answer}',
            },
        ],
        'examples': [
            {
                'category': category,
                'count': 3,
                'items': list(items),
                'separator': ', ',
            }
            for category, items in _COMMA_THREE_POOLS
        ],
    },
}
