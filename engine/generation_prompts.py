from config import GlobalConfig, TrainingStage


DEFAULT_PRETRAINING_GENERATION_TEST_PROMPTS = [
    'Cats are curious animals that',
    'A computer is a machine that',
    'The capital of France is',
    'In winter, the weather is often',
    'Chocolate is made from',
    'The purpose of sleep is',
    'A recipe for pancakes includes',
    'Soccer is played with',
    'Electric cars use',
    'Mountains are formed when'
]

DEFAULT_INSTRUCT_GENERATION_TEST_PROMPTS = [
    'Who are you? Answer in one short sentence.',
    'What is the capital of France? Answer in one short sentence.',
    'Give exactly three numbered steps for cooking a boiled egg.',
    'Write exactly one sentence about rain.',
    'Rewrite this sentence to be clearer:\nThe thing was bad because it was not good.\nOnly provide the rewritten sentence.',
    'List exactly three fruits, separated by commas.',
    'Explain what a GPU is in simple words. Use at most two short sentences.',
    'Write one short friendly reply to this message:\nCan we meet tomorrow?',
    'Summarize this in one sentence:\nPenguins are birds that cannot fly but are excellent swimmers.',
    "Correct the grammar of this sentence:\nHe don't like apples.\nOnly provide the corrected sentence."
]

DEFAULT_DPO_GENERATION_TEST_PROMPTS = [
    'Who are you? Answer in one short sentence.',
    'What is the capital of France? Answer in one short sentence.',
    'Give exactly three numbered steps for cooking a boiled egg.',
    'Write exactly one sentence about rain.',
    'Rewrite this sentence to be clearer:\nThe thing was bad because it was not good.\nOnly provide the rewritten sentence.',
    'List exactly three fruits, separated by commas.',
    'Explain what a GPU is in simple words. Use at most two short sentences.',
    'Write one short friendly reply to this message:\nCan we meet tomorrow?',
    'Summarize this in one sentence:\nPenguins are birds that cannot fly but are excellent swimmers.',
    "Correct the grammar of this sentence:\nHe don't like apples.\nOnly provide the corrected sentence."
]

def resolve_generation_test_prompts(config: GlobalConfig) -> list[str]:
    if config.generation.test_prompts is not None:
        return config.generation.test_prompts
    elif config.training.stage == TrainingStage.PRETRAINING:
        return DEFAULT_PRETRAINING_GENERATION_TEST_PROMPTS
    elif config.training.stage == TrainingStage.INSTRUCT:
        return DEFAULT_INSTRUCT_GENERATION_TEST_PROMPTS
    elif config.training.state == TrainingStage.DPO:
        return DEFAULT_DPO_GENERATION_TEST_PROMPTS
    else:
        raise ValueError(
            f'Unsupported training stage for generation prompts: {config.training.stage}'
        )
