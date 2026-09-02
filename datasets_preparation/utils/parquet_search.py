import pyarrow.parquet as pq

from huggingface_hub import HfApi, HfFileSystem
from concurrent.futures import ThreadPoolExecutor
from bisect import bisect_right


def find_parquet_files(
    *,
    dataset_id,
    revision,
    token
):
    api = HfApi(token=token)

    files = api.list_repo_files(dataset_id, repo_type='dataset', revision=revision)

    parquet_files = sorted(path for path in files if path.endswith('.parquet'))

    if not parquet_files:
        raise ValueError(f'No parquet files found for {dataset_id}@{revision}')

    return parquet_files

def get_parquet_row_counts(
    *,
    dataset_id,
    revision,
    files,
    token,
    num_proc
):
    fs = HfFileSystem(token=token)

    def count_rows(path):
        with fs.open(f'datasets/{dataset_id}@{revision}/{path}', 'rb') as f:
            return pq.ParquetFile(f).metadata.num_rows

    with ThreadPoolExecutor(max_workers=num_proc) as pool:
        return list(pool.map(count_rows, files))

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
