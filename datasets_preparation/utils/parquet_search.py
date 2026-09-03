import pyarrow.parquet as pq

from huggingface_hub import HfApi, HfFileSystem
from concurrent.futures import ThreadPoolExecutor
from datasets import load_dataset
from tqdm.auto import tqdm
from functools import partial
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

def count_rows(fs, ds_id, revision, cache, path):
    if cache is not None and path in cache:
        return cache[path]

    with fs.open(f'datasets/{ds_id}@{revision}/{path}', 'rb') as f:
        row_count = pq.ParquetFile(f).metadata.num_rows
        if cache is not None:
            cache[path] = row_count
        return row_count

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

    current_document = 0

    with tqdm(total=len(files), desc='Searching parquet shards', unit='shards') as progress:
        for i in range(0, len(files), batch_size):
            batch_files = files[i:i + batch_size]

            with ThreadPoolExecutor(max_workers=min(num_proc, len(batch_files))) as pool:
                row_counts = list(pool.map(partial(count_rows, fs, ds_id, revision, None), batch_files))

            progress.update(len(batch_files))

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

def get_file_index_from_cursor(files, cursor):
    next_file = cursor['next_file']
    logger.info(f'Loading parquet dataset from {cursor["next_file"]}, row {cursor["next_row"]:,}')

    if next_file is None:
        raise ValueError('Cannot load cursor as it points to the end of the dataset')

    try:
        return files.index(next_file)
    except ValueError:
        raise ValueError(f'The cursor file: {next_file!r} was not found in the parquet index')

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
    file_index = get_file_index_from_cursor(files, cursor)

    remaining_files = files[file_index:]

    logger.info(f'Using {len(remaining_files):,} parquet files from cursor onward')

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
    logger.info('Dataset loaded.')

    return ds

def advance_parquet_cursor(
    *,
    ds_id,
    revision,
    files,
    cursor,
    n_documents,
    token,
    row_count_cache=None
):
    if n_documents < 0:
        raise ValueError('n_documents must be >= 0')

    if n_documents == 0:
        return cursor

    file_index = get_file_index_from_cursor(files, cursor)

    if row_count_cache is None:
        row_count_cache = {}

    fs = HfFileSystem(token=token)

    next_document = cursor['next_document']
    next_row = cursor['next_row']

    while n_documents > 0:
        path = files[file_index]
        rows = count_rows(fs, ds_id, revision, row_count_cache, path)

        if next_row < 0 or next_row >= rows:
            raise ValueError(f'Cursor row {next_row:,} is outside {path} with {rows:,} rows')

        remaining_rows = rows - next_row

        if n_documents < remaining_rows:
            next_row += n_documents
            next_document += n_documents
            n_documents = 0
            break

        n_documents -= remaining_rows
        next_document += remaining_rows

        file_index += 1
        next_row = 0

        if file_index == len(files):
            if n_documents == 0:
                return {
                    'next_document': next_document,
                    'next_file': None,
                    'next_row': 0
                }

            raise ValueError('Cannot advance cursor beyond the end of the dataset')

    return {
        'next_document': next_document,
        'next_file': files[file_index],
        'next_row': next_row
    }
