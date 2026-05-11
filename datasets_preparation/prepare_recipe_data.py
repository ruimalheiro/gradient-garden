from config import TrainingStage
from datasets_preparation import (
    prepare_hellaswag_dataset,
    prepare_winogrande_dataset,
    prepare_arc_challenge_dataset,
    prepare_pretraining_dataset,
    prepare_instruct_dataset,
    prepare_dpo_dataset,
)
from logger import logger


def prepare_recipe_data(recipe, num_proc):
    config = recipe.config

    if recipe.data is None:
        raise ValueError('Recipe is missing "data" section required for dataset preparation.')

    data_config = recipe.data
    datasets_mix = data_config.model_dump(mode='python', exclude={'evals'}) # to be compatible with mix dict structure
    data_evals = data_config.evals

    logger.info(f'Preparing recipe data for stage: {config.training.stage.value}')

    if config.training.stage == TrainingStage.PRETRAINING:
        if data_config.shard_size is None:
            raise ValueError('Pretraining recipes require data.shard_size.')
        prepare_pretraining_dataset(config=config, datasets_mix=datasets_mix, num_proc=num_proc)
    elif config.training.stage == TrainingStage.INSTRUCT:
        prepare_instruct_dataset(config=config, datasets_mix=datasets_mix, num_proc=num_proc)
    elif config.training.stage == TrainingStage.DPO:
        prepare_dpo_dataset(config=config, datasets_mix=datasets_mix, num_proc=num_proc)
    else:
        raise ValueError(f'Invalid training stage: {config.training.stage}')

    if data_evals.hellaswag.enabled:
        prepare_hellaswag_dataset(config=config, num_proc=num_proc)

    if data_evals.winogrande.enabled:
        prepare_winogrande_dataset(config=config, num_proc=num_proc)

    if data_evals.arc_challenge.enabled:
        prepare_arc_challenge_dataset(config=config, num_proc=num_proc)
