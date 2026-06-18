from datasets_preparation.synthetic.common import generate_dataset
from datasets_preparation.synthetic.instruct.common import row
from datasets_preparation.synthetic.group_utils import generate_weighted_group_examples
from datasets_preparation.synthetic.instruct.fixtures.identity import (
    DIRECT_IDENTITY_PROMPTS,
    HUMAN_PROMPTS,
    CAPABILITY_PROMPTS,
    CONSTRAINT_PROMPTS
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
        templates = [
            identity_message
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

    def generate_capabilities_answer():
        prompt = rng.choice(CAPABILITY_PROMPTS)
        templates = [
            f'I am {model_name}, and I help answer questions clearly and usefully.',
            identity_message,
            f'I am {model_name}, an AI assistant that helps with information and tasks.'
        ]
        return row(prompt, rng.choice(templates))

    def generate_identity_constraint_answer():
        prompt = rng.choice(CONSTRAINT_PROMPTS)
        templates = [
            model_name
        ]
        return row(prompt, rng.choice(templates))

    return generate_weighted_group_examples(
        groups={
            'identity': (generate_direct_identity, 0.45),
            'human': (generate_human_answer, 0.25),
            'capability': (generate_capabilities_answer, 0.20),
            'constraint': (generate_identity_constraint_answer, 0.10)
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
