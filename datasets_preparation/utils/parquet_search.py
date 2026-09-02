import pyarrow.parquet as pq

from huggingface_hub import HfApi, HfFileSystem
from concurrent.futures import ThreadPoolExecutor
from bisect import bisect_right
from datasets import load_dataset


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

def get_parquet_row_counts(
    *,
    ds_id,
    revision,
    files,
    token,
    num_proc
):
    fs = HfFileSystem(token=token)

    def count_rows(path):
        with fs.open(f'datasets/{ds_id}@{revision}/{path}', 'rb') as f:
            return pq.ParquetFile(f).metadata.num_rows

    with ThreadPoolExecutor(max_workers=num_proc) as pool:
        return list(pool.map(count_rows, files))

def build_parquet_index(*, files, row_counts):
    if len(files) != len(row_counts):
        raise ValueError('files and row_counts must have the same length')

    indexed_files = []
    current_document = 0

    for path, rows in zip(files, row_counts):
        indexed_files.append({
            'path': path,
            'rows': rows ,
            'start_document': current_document
        })
        current_document += rows

    return {
        'files': indexed_files,
        'total_rows': current_document
    }

def find_document_cursor(index, offset):
    if offset < 0:
        raise ValueError('offset must be >= 0')

    total_rows = index['total_rows']

    if offset > total_rows:
        raise ValueError(f'offset={offset:,} exceeds the dataset size of {total_rows:,} documents')

    if offset == total_rows:
        return {
            'next_document': offset,
            'next_file': None,
            'next_row': 0
        }

    files = index['files']

    starts = [file['start_document'] for file in files]
    file_index = bisect_right(starts, offset) - 1
    file = files[file_index]

    return {
        'next_document': offset,
        'next_file': file['path'],
        'next_row': offset - file['start_document']
    }

def load_parquet_from_cursor(
    *,
    ds_id,
    revision,
    split,
    index,
    cursor,
    token
):
    next_file = cursor['next_file']
    if next_file is None:
        raise ValueError('Cannot load cursor as it points to the end of the file')

    files = [file['path'] for file in index['files']]

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
        streaming=True,
        token=token
    )

    next_row = cursor['next_row']

    if next_row > 0:
        ds = ds.skip(next_row)

    return ds
