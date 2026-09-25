import pytest

from types import SimpleNamespace
from datasets_preparation.utils.parquet_search import find_parquet_files


def test_find_parquet_files_uses_selected_builder_config_and_split():
    dataset_builder = SimpleNamespace(
        config=SimpleNamespace(
            data_files={
                'train': [
                    (
                        'hf://datasets/HuggingFaceFW/fineweb-edu@abc123/'
                        'sample-10BT/train/000_00000.parquet'
                    ),
                    (
                        'hf://datasets/HuggingFaceFW/fineweb-edu@abc123/'
                        'sample-10BT/train/000_00001.parquet'
                    ),
                ],
                'validation': [
                    (
                        'hf://datasets/HuggingFaceFW/fineweb-edu@abc123/'
                        'sample-10BT/validation/000_00000.parquet'
                    )
                ],
            }
        )
    )

    files = find_parquet_files(
        ds_id='HuggingFaceFW/fineweb-edu',
        name='sample-10BT',
        split='train',
        revision='abc123',
        dataset_builder=dataset_builder
    )

    assert files == [
        'sample-10BT/train/000_00000.parquet',
        'sample-10BT/train/000_00001.parquet'
    ]

def test_find_parquet_files_rejects_missing_split():
    dataset_builder = SimpleNamespace(
        config=SimpleNamespace(
            data_files={
                'train': [
                    (
                        'hf://datasets/HuggingFaceFW/fineweb-edu@abc123/'
                        'sample-10BT/train/000_00000.parquet'
                    )
                ]
            }
        )
    )

    with pytest.raises(ValueError, match="Split 'validation' was not found"):
        find_parquet_files(
            ds_id='HuggingFaceFW/fineweb-edu',
            name='sample-10BT',
            split='validation',
            revision='abc123',
            dataset_builder=dataset_builder
        )
