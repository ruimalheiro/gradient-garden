from datasets_preparation.synthetic.common import generate_dataset
from datasets_preparation.synthetic.instruct.common import row
from datasets_preparation.synthetic.group_utils import generate_weighted_group_examples
from datasets_preparation.synthetic.instruct.fixtures.identity import (
    DIRECT_IDENTITY_PROMPTS,
    HUMAN_PROMPTS,
    ROLE_PROMPTS,
    NAME_ONLY_PROMPTS,
    OTHER_ASSISTANT_PROMPTS
)


def generator_fn(*, config, rng, count, transforms):
    custom_identity_message = transforms.get('identity_message', None)

    model_name = transforms.get(
        'model_name',
        config.model.architecture.value.capitalize()
    )

    identity_message = (
        custom_identity_message if custom_identity_message
        else f'I am {model_name}, a helpful AI assistant.'
    )

    def generate_direct_identity():
        prompt = rng.choice(DIRECT_IDENTITY_PROMPTS)

        if custom_identity_message:
            templates = [
                identity_message,
            ]
        else:
            templates = [
                identity_message,
                f'I am {model_name}, an AI assistant.',
                f'My name is {model_name}, and I am a helpful AI assistant.',
            ]

        return row(prompt, rng.choice(templates))

    def generate_human_answer():
        prompt = rng.choice(HUMAN_PROMPTS)
        templates = [
            f'No, I am {model_name}, a helpful AI assistant.',
            f'No, I am an AI assistant called {model_name}.',
            f'I am not human; I am {model_name}, a helpful AI assistant.',
        ]
        return row(prompt, rng.choice(templates))

    def generate_role_answer():
        prompt = rng.choice(ROLE_PROMPTS)
        templates = [
            f'I am {model_name}, and I help answer questions clearly and usefully.',
            identity_message,
            f'I am {model_name}, an AI assistant that helps with information and tasks.'
        ]
        return row(prompt, rng.choice(templates))

    def generate_name_only_answer():
        prompt = rng.choice(NAME_ONLY_PROMPTS)
        templates = [
            model_name
        ]
        return row(prompt, rng.choice(templates))

    def generate_other_assistant_answer():
        prompt = rng.choice(OTHER_ASSISTANT_PROMPTS)
        templates = [
            f'No, my name is {model_name}.',
            identity_message,
            f'You can call me {model_name}.',
        ]
        return row(prompt, rng.choice(templates))

    return generate_weighted_group_examples(
        groups={
            'identity': (generate_direct_identity, 0.40),
            'human': (generate_human_answer, 0.20),
            'role': (generate_role_answer, 0.20),
            'name_only': (generate_name_only_answer, 0.10),
            'other_assistant': (generate_other_assistant_answer, 0.10)
        },
        transforms=transforms,
        count=count
    )

def build_identity_dataset(*, config, ds_id, seed, count, transforms):
    return generate_dataset(
        config=config,
        ds_id=ds_id,
        seed=seed,
        count=count,
        transforms=transforms,
        label='Identity',
        file_name='identity',
        generator_fn=generator_fn
    )
