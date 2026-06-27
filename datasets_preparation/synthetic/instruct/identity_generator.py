from utils import get_architecture_name
from datasets_preparation.synthetic.common import generate_dataset
from datasets_preparation.synthetic.group_utils import generate_weighted_group_examples
from datasets_preparation.synthetic.instruct.common import render_fixture_example
from datasets_preparation.synthetic.instruct.fixtures.identity import IDENTITY_FIXTURES


def generator_fn(*, config, rng, count, transforms):
    custom_identity_message = transforms.get('identity_message', None)

    model_name = transforms.get(
        'model_name',
        get_architecture_name(config).capitalize()
    )

    identity_message = (
        custom_identity_message if custom_identity_message
        else f'I am {model_name}, a helpful AI assistant.'
    )

    variables = {
        'model_name': model_name,
        'identity_message': identity_message,
    }

    def identity_answer_selector(*, group_name, fixture, rng, variables):
        if custom_identity_message and group_name == 'identity':
            return '{identity_message}'
        return rng.choice(fixture['answers'])

    def make_group_generator(group_name):
        def generate_example():
            return render_fixture_example(
                IDENTITY_FIXTURES,
                group_name,
                rng=rng,
                variables=variables,
                answer_selector=identity_answer_selector,
            )
        return generate_example

    return generate_weighted_group_examples(
        groups={
            'identity': (make_group_generator('identity'), 0.40),
            'human': (make_group_generator('human'), 0.20),
            'role': (make_group_generator('role'), 0.20),
            'name_only': (make_group_generator('name_only'), 0.10),
            'other_assistant': (make_group_generator('other_assistant'), 0.10),
        },
        transforms=transforms,
        count=count,
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
