import pyarrow.parquet as pq

from huggingface_hub import HfApi, HfFileSystem
from concurrent.futures import ThreadPoolExecutor
from datasets import load_dataset
from logger import logger


def find_parquet_files(
    *,
    ds_id,
    revision,
    token
):
    api = HfApi(token=token)

    files = api.list_repo_files(ds_id, repo_type='dataset', revision=revision)

    parquet_files = sorted(path for path in files if path.endswith('.parquet'))

    if not parquet_files:
        raise ValueError(f'No parquet files found for {ds_id}@{revision}')

    return parquet_files

def find_parquet_cursor(
    *,
    ds_id,
    revision,
    files,
    offset,
    token,
    num_proc,
    batch_size=64
):
    if offset < 0:
        raise ValueError('offset must be >= 0')

    if not files:
        raise ValueError('files must not be empty')

    if offset == 0:
        return {
            'next_document': 0,
            'next_file': files[0],
            'next_row': 0
        }

    fs = HfFileSystem(token=token)

    def count_rows(path):
        with fs.open(f'datasets/{ds_id}@{revision}/{path}', 'rb') as f:
            return pq.ParquetFile(f).metadata.num_rows

    current_document = 0
    for i in range(0, len(files), batch_size):
        batch_files = files[i:i + batch_size]

        with ThreadPoolExecutor(max_workers=min(num_proc, len(batch_files))) as pool:
            row_counts = list(pool.map(count_rows, batch_files))

        for path, rows in zip(batch_files, row_counts):
            next_document = current_document + rows

            if offset < next_document:
                return {
                    'next_document': offset,
                    'next_file': path,
                    'next_row': offset - current_document
                }

            current_document = next_document

    if offset == current_document:
        return {
            'next_document': offset,
            'next_file': None,
            'next_row': 0
        }

    raise ValueError(f'offset={offset:,} exceeds the dataset size of {current_document:,} documents')

def load_parquet_from_cursor(
    *,
    ds_id,
    revision,
    split,
    streaming,
    files,
    cursor,
    token
):
    next_file = cursor['next_file']
    if next_file is None:
        raise ValueError('Cannot load cursor as it points to the end of the dataset')

    try:
        file_index = files.index(next_file)
    except ValueError:
        raise ValueError(f'The cursor file: {next_file!r} was not found in the parquet index')

    remaining_files = files[file_index:]

    data_files = { split: [f'hf://datasets/{ds_id}@{revision}/{path}' for path in remaining_files] }

    ds = load_dataset(
        'parquet',
        data_files=data_files,
        split=split,
        streaming=streaming,
        token=token
    )

    next_row = cursor['next_row']

    if next_row > 0:
        ds = ds.skip(next_row)

    return ds

def load_dataset_with_search_parquet(
    *,
    ds_id,
    split,
    streaming,
    revision,
    start_document,
    token,
    num_proc,
    batch_size=64
):
    logger.info('finding parquet files...')
    files = find_parquet_files(
        ds_id=ds_id,
        revision=revision,
        token=token
    )
    logger.info(f'found {len(files)} files.')

    logger.info('finding parquet cursor...')
    cursor = find_parquet_cursor(
        ds_id=ds_id,
        revision=revision,
        files=files,
        offset=start_document,
        token=token,
        num_proc=num_proc,
        batch_size=batch_size
    )
    logger.info('found cursor.')

    logger.info('loading the dataset using cursor...')
    ds = load_parquet_from_cursor(
        ds_id=ds_id,
        revision=revision,
        split=split,
        streaming=streaming,
        files=files,
        cursor=cursor,
        token=token
    )
    logger.info('ds loaded.')

    return ds
