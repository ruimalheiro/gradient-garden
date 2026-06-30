from logger import logger
from config import TrainingStage
from datasets_preparation.data_preparation_utils import get_max_number_of_cpu_processes
from datasets_preparation.evals.prepare_hellaswag_dataset import prepare_hellaswag_dataset
from datasets_preparation.evals.prepare_winogrande_dataset import prepare_winogrande_dataset
from datasets_preparation.evals.prepare_arc_challenge_dataset import prepare_arc_challenge_dataset
from datasets_preparation.evals.prepare_ifeval_no_external import prepare_ifeval_no_external_dataset
from datasets_preparation.prepare_pretraining_dataset import prepare_pretraining_dataset
from datasets_preparation.prepare_instruct_dataset import prepare_instruct_dataset
from datasets_preparation.prepare_dpo_dataset import prepare_dpo_dataset


def prepare_recipe_data(recipe, num_proc):
    config = recipe.config

    if recipe.data is None:
        raise ValueError('Recipe is missing "data" section required for dataset preparation.')

    data_config = recipe.data
    data_evals = data_config.evals

    logger.info(f'Preparing recipe data for stage: {config.training.stage.value}')

    if data_config.datasets:
        datasets_mix = data_config.model_dump(mode='python', exclude={'evals'}) # to be compatible with mix dict structure

        if config.training.stage == TrainingStage.PRETRAINING:
            if data_config.datasets_common_settings.shard_size is None:
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

    if data_evals.ifeval_no_external.enabled:
        prepare_ifeval_no_external_dataset(config=config, num_proc=num_proc)
