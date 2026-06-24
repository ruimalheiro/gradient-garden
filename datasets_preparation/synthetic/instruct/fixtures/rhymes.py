RHYME_FIXTURES = {
    'exactly_four_unique': {
        'examples': [
            {
                'prompt': 'Give exactly four different words that rhyme with cat, separated by commas.',
                'answer': 'bat, hat, mat, rat',
            },
            {
                'prompt': 'Give exactly four different words that rhyme with dog, separated by commas.',
                'answer': 'fog, log, hog, frog',
            },
            {
                'prompt': 'Give exactly four different words that rhyme with sun, separated by commas.',
                'answer': 'bun, fun, run, done',
            },
            {
                'prompt': 'Give exactly four different words that rhyme with light, separated by commas.',
                'answer': 'bright, night, sight, right',
            },
            {
                'prompt': 'Give exactly four different words that rhyme with tree, separated by commas.',
                'answer': 'bee, free, see, three',
            },
            {
                'prompt': 'Give exactly four different words that rhyme with blue, separated by commas.',
                'answer': 'true, clue, glue, new',
            },
            {
                'prompt': 'Give exactly four different words that rhyme with rain, separated by commas.',
                'answer': 'brain, train, plain, chain',
            },
            {
                'prompt': 'Give exactly four different words that rhyme with book, separated by commas.',
                'answer': 'cook, look, hook, took',
            },
            {
                'prompt': 'Give exactly four different words that rhyme with time, separated by commas.',
                'answer': 'climb, rhyme, chime, prime',
            },
            {
                'prompt': 'Give exactly four different words that rhyme with day, separated by commas.',
                'answer': 'play, stay, way, say',
            },
            {
                'prompt': 'Give exactly four different words that rhyme with red, separated by commas.',
                'answer': 'bed, fed, led, said',
            },
            {
                'prompt': 'Give exactly four different words that rhyme with cold, separated by commas.',
                'answer': 'bold, old, sold, told',
            },
            {
                'prompt': 'Give exactly four different words that rhyme with make, separated by commas.',
                'answer': 'bake, cake, lake, take',
            },
            {
                'prompt': 'Give exactly four different words that rhyme with wall, separated by commas.',
                'answer': 'ball, call, fall, tall',
            },
            {
                'prompt': 'Give exactly four different words that rhyme with hand, separated by commas.',
                'answer': 'band, land, sand, stand',
            },
            {
                'prompt': 'Give exactly four different words that rhyme with mouse, separated by commas.',
                'answer': 'house, blouse, spouse, grouse',
            },
            {
                'prompt': 'Give exactly four different words that rhyme with star, separated by commas.',
                'answer': 'car, far, jar, bar',
            },
            {
                'prompt': 'Give exactly four different words that rhyme with green, separated by commas.',
                'answer': 'bean, clean, mean, seen',
            },
            {
                'prompt': 'Give exactly four different words that rhyme with slow, separated by commas.',
                'answer': 'go, show, snow, throw',
            },
            {
                'prompt': 'Give exactly four different words that rhyme with care, separated by commas.',
                'answer': 'bare, fair, hair, share',
            },
        ],
    },
    'exactly_three_unique': {
        'examples': [
            {
                'prompt': 'Give exactly three different words that rhyme with cat, separated by commas.',
                'answer': 'bat, hat, mat',
            },
            {
                'prompt': 'Give exactly three different words that rhyme with dog, separated by commas.',
                'answer': 'fog, log, hog',
            },
            {
                'prompt': 'Give exactly three different words that rhyme with sun, separated by commas.',
                'answer': 'fun, run, bun',
            },
            {
                'prompt': 'Give exactly three different words that rhyme with light, separated by commas.',
                'answer': 'night, sight, bright',
            },
            {
                'prompt': 'Give exactly three different words that rhyme with tree, separated by commas.',
                'answer': 'bee, free, see',
            },
            {
                'prompt': 'Give exactly three different words that rhyme with blue, separated by commas.',
                'answer': 'true, clue, glue',
            },
            {
                'prompt': 'Give exactly three different words that rhyme with rain, separated by commas.',
                'answer': 'train, plain, chain',
            },
            {
                'prompt': 'Give exactly three different words that rhyme with book, separated by commas.',
                'answer': 'cook, look, hook',
            },
            {
                'prompt': 'Give exactly three different words that rhyme with day, separated by commas.',
                'answer': 'play, stay, way',
            },
            {
                'prompt': 'Give exactly three different words that rhyme with cold, separated by commas.',
                'answer': 'bold, old, told',
            },
            {
                'prompt': 'Give exactly three different words that rhyme with make, separated by commas.',
                'answer': 'bake, cake, lake',
            },
            {
                'prompt': 'Give exactly three different words that rhyme with wall, separated by commas.',
                'answer': 'ball, call, fall',
            },
        ],
    },
    'exactly_five_unique': {
        'examples': [
            {
                'prompt': 'Give exactly five different words that rhyme with cat, separated by commas.',
                'answer': 'bat, hat, mat, rat, sat',
            },
            {
                'prompt': 'Give exactly five different words that rhyme with dog, separated by commas.',
                'answer': 'fog, log, hog, frog, bog',
            },
            {
                'prompt': 'Give exactly five different words that rhyme with light, separated by commas.',
                'answer': 'bright, night, sight, right, flight',
            },
            {
                'prompt': 'Give exactly five different words that rhyme with tree, separated by commas.',
                'answer': 'bee, free, see, three, key',
            },
            {
                'prompt': 'Give exactly five different words that rhyme with rain, separated by commas.',
                'answer': 'brain, train, plain, chain, main',
            },
            {
                'prompt': 'Give exactly five different words that rhyme with time, separated by commas.',
                'answer': 'climb, rhyme, chime, prime, lime',
            },
            {
                'prompt': 'Give exactly five different words that rhyme with red, separated by commas.',
                'answer': 'bed, fed, led, said, thread',
            },
            {
                'prompt': 'Give exactly five different words that rhyme with cold, separated by commas.',
                'answer': 'bold, old, sold, told, gold',
            },
            {
                'prompt': 'Give exactly five different words that rhyme with make, separated by commas.',
                'answer': 'bake, cake, lake, take, shake',
            },
            {
                'prompt': 'Give exactly five different words that rhyme with wall, separated by commas.',
                'answer': 'ball, call, fall, tall, small',
            },
        ],
    },
    'no_repeats_explicit': {
        'examples': [
            {
                'prompt': 'Give exactly four words that rhyme with cat. Do not repeat any word. Use commas only.',
                'answer': 'bat, hat, mat, rat',
            },
            {
                'prompt': 'Give exactly four words that rhyme with dog. Do not repeat any word. Use commas only.',
                'answer': 'fog, log, hog, frog',
            },
            {
                'prompt': 'Give exactly four words that rhyme with sun. Do not repeat any word. Use commas only.',
                'answer': 'bun, fun, run, done',
            },
            {
                'prompt': 'Give exactly four words that rhyme with light. Do not repeat any word. Use commas only.',
                'answer': 'bright, night, sight, right',
            },
            {
                'prompt': 'Give exactly four words that rhyme with tree. Do not repeat any word. Use commas only.',
                'answer': 'bee, free, see, three',
            },
            {
                'prompt': 'Give exactly four words that rhyme with rain. Do not repeat any word. Use commas only.',
                'answer': 'brain, train, plain, chain',
            },
            {
                'prompt': 'Give exactly four words that rhyme with book. Do not repeat any word. Use commas only.',
                'answer': 'cook, look, hook, took',
            },
            {
                'prompt': 'Give exactly four words that rhyme with time. Do not repeat any word. Use commas only.',
                'answer': 'climb, rhyme, chime, prime',
            },
            {
                'prompt': 'Give exactly four words that rhyme with day. Do not repeat any word. Use commas only.',
                'answer': 'play, stay, way, say',
            },
            {
                'prompt': 'Give exactly four words that rhyme with blue. Do not repeat any word. Use commas only.',
                'answer': 'true, clue, glue, new',
            },
            {
                'prompt': 'Give exactly four words that rhyme with red. Do not repeat any word. Use commas only.',
                'answer': 'bed, fed, led, said',
            },
            {
                'prompt': 'Give exactly four words that rhyme with wall. Do not repeat any word. Use commas only.',
                'answer': 'ball, call, fall, tall',
            },
            {
                'prompt': 'Give exactly four words that rhyme with hand. Do not repeat any word. Use commas only.',
                'answer': 'band, land, sand, stand',
            },
            {
                'prompt': 'Give exactly four words that rhyme with star. Do not repeat any word. Use commas only.',
                'answer': 'car, far, jar, bar',
            },
            {
                'prompt': 'Give exactly four words that rhyme with slow. Do not repeat any word. Use commas only.',
                'answer': 'go, show, snow, throw',
            },
        ],
    },
    'comma_format_only': {
        'examples': [
            {
                'prompt': 'List four rhyming words for cat. Separate them with commas only.',
                'answer': 'bat, hat, mat, rat',
            },
            {
                'prompt': 'List four rhyming words for dog. Separate them with commas only.',
                'answer': 'fog, log, hog, frog',
            },
            {
                'prompt': 'List four rhyming words for light. Separate them with commas only.',
                'answer': 'bright, night, sight, right',
            },
            {
                'prompt': 'List four rhyming words for rain. Separate them with commas only.',
                'answer': 'brain, train, plain, chain',
            },
            {
                'prompt': 'List four rhyming words for tree. Separate them with commas only.',
                'answer': 'bee, free, see, three',
            },
            {
                'prompt': 'List four rhyming words for make. Separate them with commas only.',
                'answer': 'bake, cake, lake, take',
            },
            {
                'prompt': 'List four rhyming words for cold. Separate them with commas only.',
                'answer': 'bold, old, sold, told',
            },
            {
                'prompt': 'List four rhyming words for wall. Separate them with commas only.',
                'answer': 'ball, call, fall, tall',
            },
            {
                'prompt': 'List four rhyming words for care. Separate them with commas only.',
                'answer': 'bare, fair, hair, share',
            },
            {
                'prompt': 'List four rhyming words for green. Separate them with commas only.',
                'answer': 'bean, clean, mean, seen',
            },
        ],
    },
}
