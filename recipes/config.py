import yaml

from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Literal
from config import GlobalConfig
from logger import logger


class DatasetsCommonSettings(BaseModel):
    model_config = ConfigDict(extra='forbid')
    shard_size: int | None = None
    target_tokens: int | None = None
    validation_ratio: float = 0.01
    interleave_stopping_strategy: Literal['first_exhausted', 'all_exhausted', 'all_exhausted_without_replacement'] = 'first_exhausted'

class DatasetEntryConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    weight: float
    transforms: dict[str, Any] = Field(default_factory=dict)

class RecipeEvalDatasetConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    enabled: bool = False

class RecipeEvalsDataConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    hellaswag: RecipeEvalDatasetConfig = Field(default_factory=RecipeEvalDatasetConfig)
    winogrande: RecipeEvalDatasetConfig = Field(default_factory=RecipeEvalDatasetConfig)
    arc_challenge: RecipeEvalDatasetConfig = Field(default_factory=RecipeEvalDatasetConfig)
    ifeval_no_external: RecipeEvalDatasetConfig = Field(default_factory=RecipeEvalDatasetConfig)

class RecipeDataConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    seed: int
    datasets_common_settings: DatasetsCommonSettings = Field(default_factory=DatasetsCommonSettings)
    datasets: dict[str, dict[str, DatasetEntryConfig]] = Field(default_factory=dict)
    evals: RecipeEvalsDataConfig = Field(default_factory=RecipeEvalsDataConfig)

class RecipeConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str | None = None
    description: str | None = None
    config: GlobalConfig
    data: RecipeDataConfig | None = None

def load_recipe(recipe_path) -> RecipeConfig:
    recipe_path = Path(recipe_path)
    
    if not recipe_path.exists():
        raise FileNotFoundError(f'Provided recipe path does not exist: {recipe_path}')

    if not recipe_path.is_file():
        raise FileNotFoundError(f'Provided recipe path is not a file: {recipe_path}')

    if recipe_path.suffix not in {'.yaml', '.yml'}:
        raise ValueError(f'Recipe file must be a .yaml or .yml file: {recipe_path}')

    with recipe_path.open('r') as file:
        recipe_data = yaml.safe_load(file) or {}

    if not isinstance(recipe_data, dict):
        raise ValueError(f'The provided yaml file or structure is invalid: {recipe_path}')

    if not recipe_data:
        raise ValueError(f'Recipe file cannot be empty: {recipe_path}')

    loaded_recipe = RecipeConfig.model_validate(recipe_data)
    logger.info(f'Recipe loaded from: {recipe_path}')
    return loaded_recipe
