import os
import numpy as np
import sys
import multiprocessing as mp
import hashlib
import time
import math

from tqdm.auto import tqdm
from functools import partial
from pathlib import Path
from logger import logger
from utils import (
    load_json_file,
    save_json_file
)
from dataclasses import dataclass


def get_max_number_of_cpu_processes(config):
    num_processes = max(1, os.cpu_count() // 2)
    if config.runtime.number_of_cpu_processes != 0:
        num_processes = max(1, min(config.runtime.number_of_cpu_processes, os.cpu_count()))
    logger.info(f'Number of CPU processes: {num_processes}\n')
    return num_processes

def stable_hash(text, *, seed=None, hash_bytes=8):
    # fast and stable hash. More info: https://docs.python.org/3/library/hashlib.html#blake2
    if seed is not None:
        salt = f'{seed}-salt'.encode('utf-8')
        return int.from_bytes(hashlib.blake2b(text.encode(), digest_size=hash_bytes, key=salt).digest(), 'big')
    return int.from_bytes(hashlib.blake2b(text.encode(), digest_size=hash_bytes).digest(), 'big')

def make_source_key(ds_id, name):
    if name and name != 'default':
        return f'{ds_id}::{name}'
    return ds_id

def assert_common_structure_and_extract(datasets_mix, supported_datasets):
    ''' Validates common file structure and extracts seed, common dataset settings, valid datasets and probabilities (normalized weight distribution)
    '''
    assert 'seed' in datasets_mix
    seed = datasets_mix['seed']
    assert isinstance(seed, int)

    # Validate common settings if present.
    common_settings = datasets_mix.get('datasets_common_settings', {})
    shard_size = None
    target_tokens = None
    validation_ratio = None
    if 'shard_size' in common_settings:
        shard_size = common_settings['shard_size']
        assert shard_size is None or int(shard_size) > 0, 'datasets_common_settings.shard_size must be > 0'
    if 'target_tokens' in common_settings:
        target_tokens = common_settings['target_tokens']
        assert target_tokens is None or isinstance(target_tokens, int), 'datasets_common_settings.target_tokens must be an integer'
    if 'validation_ratio' in common_settings:
        validation_ratio = common_settings['validation_ratio']
        assert validation_ratio is None or isinstance(validation_ratio, float), 'datasets_common_settings.validation_ratio must be a float'
    assert 'interleave_stopping_strategy' in common_settings, 'common_settings.interleave_stopping_strategy is required'

    assert 'datasets' in datasets_mix
    datasets = datasets_mix['datasets']

    # Validate candidates
    valid_datasets = []
    for dataset_id, names in datasets.items():
        assert dataset_id in supported_datasets

        for name in names:
            assert name in supported_datasets[dataset_id]
            assert 'weight' in datasets[dataset_id][name]
            weight = float(datasets[dataset_id][name].get('weight', 0.0))
            assert weight >= 0.0, f'weight must be >= 0 for {dataset_id}/{name}'
            if weight > 0:
                valid_datasets.append({
                    'id': dataset_id,
                    'name': name,
                    **datasets[dataset_id][name],
                    'weight': weight,
                })

    assert valid_datasets, 'No datasets with weight > 0'

    probabilities = [ds['weight'] for ds in valid_datasets]

    # normalize probabilities
    total_p = sum(probabilities)
    assert total_p > 0.0, 'weight distribution must have positive total weight'
    probabilities = [p / total_p for p in probabilities]

    mixture_probs = [
        {make_source_key(ds['id'], ds.get('name', None)): round(p, 3)}
        for ds, p in zip(valid_datasets, probabilities)
    ]
    logger.info(f'Mixture probabilities: {mixture_probs}\n')

    return seed, common_settings, valid_datasets, probabilities

class ShardWriter:
    def __init__(self,
        *,
        target_folder,
        shard_file_prefix,
        shard_size,
        split_name,
        target_tokens=None,
        shard_bar_position=0,
        target_bar_position=2,
    ):
        self.cache_dir = Path(target_folder)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.shard_file_prefix = shard_file_prefix
        self.shard_size = int(shard_size)
        self.split_name = split_name
        self.target_tokens = target_tokens

        self.shard_index = 0
        self.token_count = 0
        self.total_tokens = 0
        self.buffer = np.empty((self.shard_size,), dtype=np.uint32)
        self.progress_bar = None
        self.target_progress_bar = None
        self.shard_bar_position = shard_bar_position
        self.target_bar_position = target_bar_position

    def get_state_dict(self):
        return {
            'shard_index': self.shard_index,
            'token_count': self.token_count,
            'total_tokens': self.total_tokens
        }

    def load_state_dict(self, state):
        self.shard_index = state['shard_index']
        self.token_count = state['token_count']
        self.total_tokens = state['total_tokens']

    def get_buffer_checkpoint(self):
        return self.buffer[:self.token_count]

    def load_buffer_checkpoint(self, buffer):
        assert buffer.size == self.token_count, (
            f'{self.split_name} buffer size does no match: '
            f'buffer has {buffer.size} but state expects {self.token_count}'
        )
        self.buffer[:self.token_count] = buffer.astype(np.uint32, copy=False)

    def delete_shards_from_current_index(self):
        for path in self.cache_dir.glob(f'{self.shard_file_prefix}_*.npy'):
            try:
                shard_index = int(path.stem.rsplit('_', 1)[1])
            except (IndexError, ValueError):
                continue

            if shard_index >= self.shard_index:
                logger.warning(f'Removing stale shard created after resume checkpoint: {path}')
                path.unlink()

    def is_done(self):
        return self.target_tokens is not None and self.total_tokens >= self.target_tokens

    def init_progress_bar(self):
        if self.progress_bar is None:
            self.progress_bar = tqdm(
                total=self.shard_size,
                initial=self.token_count,
                unit='tokens',
                desc=f'{self.split_name} shard {self.shard_index}',
                leave=False,
                position=self.shard_bar_position
            )

    def init_target_progress_bar(self):
        if self.target_tokens is None or self.target_progress_bar is not None:
            return
        self.target_progress_bar = tqdm(
            total=self.target_tokens,
            initial=self.total_tokens,
            unit='tokens',
            desc=f'{self.split_name} target',
            dynamic_ncols=True,
            leave=True,
            position=self.target_bar_position
        )

    def get_progress_bar(self):
        return self.progress_bar

    def get_target_progress_bar(self):
        return self.target_progress_bar

    def get_save_paths(self):
        current_filename = f'{self.shard_file_prefix}_{self.shard_index:06d}'
        final_path = self.cache_dir / f'{current_filename}.npy'
        temp_path = self.cache_dir / f'{current_filename}.tmp.npy'
        return final_path, temp_path

    def save_tokens(self, tokens):
        final_path, temp_path = self.get_save_paths()
        try:
            np.save(temp_path, tokens.astype(np.uint32, copy=False))
            temp_path.replace(final_path)
        except Exception as e:
            logger.error(f'\nError saving shard {self.shard_index} to {final_path}: {e}')
            logger.error('Stopping processing. Need to rerun the script to resume...')

            if temp_path.exists():
                try:
                    temp_path.unlink()
                except OSError:
                    pass

            sys.exit(1)

    def save_shard(self):
        if self.token_count == 0:
            return
        tokens = self.buffer if self.token_count == self.shard_size else self.buffer[:self.token_count]
        self.save_tokens(tokens)
        self.shard_index += 1
        self.token_count = 0

    def finish(self):
        if self.progress_bar is not None:
            self.progress_bar.close()
            self.progress_bar = None
        if self.target_progress_bar is not None:
            self.target_progress_bar.close()
            self.target_progress_bar = None
        self.save_shard()

    def write(self, tokens):
        if tokens.size == 0 or self.is_done():
            return 0

        tokens = tokens.astype(np.uint32, copy=False)

        if self.target_tokens is not None:
            remaining_target_tokens = self.target_tokens - self.total_tokens
            tokens = tokens[:remaining_target_tokens]

        written_count = 0
        offset = 0

        while offset < tokens.size:
            self.init_target_progress_bar()
            self.init_progress_bar()

            remaining_space = self.shard_size - self.token_count
            slice_length = min(remaining_space, tokens.size - offset)

            # populate the buffer
            self.buffer[self.token_count : self.token_count + slice_length] = tokens[offset : offset + slice_length]

            self.token_count += slice_length
            self.total_tokens += slice_length

            written_count += slice_length
            offset += slice_length

            self.progress_bar.update(slice_length)
            if self.target_progress_bar is not None:
                self.target_progress_bar.update(slice_length)

            if self.token_count == self.shard_size:
                self.progress_bar.close()
                self.progress_bar = None
                self.save_shard()

            if self.is_done():
                break

        return written_count

def tokenize_and_route(
    tokenizer_kwargs,
    tokenize_function,
    seed,
    validation_ratio,
    doc,
):
    source = doc.get('source', 'unknown')
    tokens = tokenize_function(tokenizer_kwargs, doc)

    # Makes assignment of 'train' or 'val' to the doc deterministic.
    HASH_BYTES = 8
    HASH_SPACE = 1 << (HASH_BYTES * 8) # 64 bit
    SEPARATION_THRESHOLD = int(validation_ratio * HASH_SPACE)

    is_val = stable_hash(doc['text'], seed=seed, hash_bytes=HASH_BYTES) < SEPARATION_THRESHOLD

    split = 'val' if is_val else 'train'

    return source, tokens, split

def shard_and_tokenize(
    *,
    seed,
    dataset,
    tokenize_function,
    tokenizer_kwargs,
    train_path,
    val_path,
    shard_file_prefix,
    shard_size,
    target_tokens,
    validation_ratio,
    num_proc,
    chunksize
):
    root_path = Path(train_path).parent
    state_dir = root_path / '.prep_state'
    state_dir.mkdir(parents=True, exist_ok=True)

    state_path = state_dir / 'state.json'
    train_buffer_path = state_dir / 'train_buffer.npy'
    val_buffer_path = state_dir / 'val_buffer.npy'

    @dataclass
    class ShardAndTokenizeState:
        train_writer: ShardWriter
        val_writer: ShardWriter
        status: str
        docs_seen: int
        source_doc_counts: dict
        source_token_counts: dict
        split_doc_counts: dict
        split_token_counts: dict

    def save_state(state: ShardAndTokenizeState):
        state_data = {
            'status': state.status,
            'docs_seen': state.docs_seen,
            'source_doc_counts': state.source_doc_counts,
            'source_token_counts': state.source_token_counts,
            'split_doc_counts': state.split_doc_counts,
            'split_token_counts': state.split_token_counts,
            'train_writer_state': state.train_writer.get_state_dict(),
            'train_writer_buffer_file_path': str(train_buffer_path),
            'val_writer_state': state.val_writer.get_state_dict(),
            'val_writer_buffer_file_path': str(val_buffer_path),
        }

        temp_state_path = state_path.with_name(f'{state_path.name}.tmp')
        temp_train_buffer_path = train_buffer_path.with_name(f'{train_buffer_path.stem}.tmp.npy')
        temp_val_buffer_path = val_buffer_path.with_name(f'{val_buffer_path.stem}.tmp.npy')

        try:
            np.save(temp_train_buffer_path, state.train_writer.get_buffer_checkpoint())
            np.save(temp_val_buffer_path, state.val_writer.get_buffer_checkpoint())
            save_json_file(temp_state_path, state_data)

            temp_train_buffer_path.replace(train_buffer_path)
            temp_val_buffer_path.replace(val_buffer_path)
            temp_state_path.replace(state_path)
        except Exception as e:
            logger.error(f'\nError saving state: {e}')
            logger.error('Stopping processing. Need to rerun the script to resume...')

            for path in [temp_state_path, temp_train_buffer_path, temp_val_buffer_path]:
                try:
                    if path.exists():
                        path.unlink()
                except OSError:
                    pass

            sys.exit(1)

    def load_state(state: ShardAndTokenizeState):
        if not (
            state_path.exists() and
            train_buffer_path.exists() and
            val_buffer_path.exists()
        ):
            return state, False

        logger.info(f'Loading state from: {state_dir}')
        state_data = load_json_file(state_path)
        train_buffer = np.load(train_buffer_path)
        val_buffer = np.load(val_buffer_path)

        state.status = state_data['status']
        state.docs_seen = state_data['docs_seen']
        state.source_doc_counts = state_data['source_doc_counts']
        state.source_token_counts = state_data['source_token_counts']
        state.split_doc_counts = state_data['split_doc_counts']
        state.split_token_counts = state_data['split_token_counts']
        state.train_writer.load_state_dict(state_data['train_writer_state'])
        state.train_writer.load_buffer_checkpoint(train_buffer)
        state.val_writer.load_state_dict(state_data['val_writer_state'])
        state.val_writer.load_buffer_checkpoint(val_buffer)

        return state, True

    shard_size = int(shard_size)
    assert shard_size > 0

    if target_tokens is not None:
        target_tokens = int(target_tokens)
        assert target_tokens > 0

    validation_ratio = float(validation_ratio)
    assert 0.0 <= validation_ratio < 1.0

    val_target_tokens = None
    if target_tokens is not None:
        if validation_ratio > 0.0:
            val_target_tokens = math.ceil(
                target_tokens * validation_ratio / (1.0 - validation_ratio)
            )
        else:
            val_target_tokens = 0

    train_writer = ShardWriter(
        target_folder=train_path,
        shard_file_prefix=shard_file_prefix,
        shard_size=shard_size,
        target_tokens=target_tokens,
        split_name='train',
        shard_bar_position=0,
        target_bar_position=2
    )

    val_writer = ShardWriter(
        target_folder=val_path,
        shard_file_prefix=shard_file_prefix,
        shard_size=shard_size,
        target_tokens=val_target_tokens,
        split_name='val',
        shard_bar_position=1,
        target_bar_position=3
    )

    def reached_target():
        if target_tokens is None:
            return False
        return train_writer.is_done() and val_writer.is_done()

    checkpoint_interval_docs = max(1, num_proc * chunksize) # save every time all workers complete.

    state = ShardAndTokenizeState(
        train_writer=train_writer,
        val_writer=val_writer,
        status='preparing',
        docs_seen=0,
        source_doc_counts={},
        source_token_counts={},
        split_doc_counts={ 'train': 0, 'val': 0 },
        split_token_counts={ 'train': 0, 'val': 0 }
    )
    state, loaded = load_state(state)
    if state.status == 'completed':
        logger.info(f'Pretraining data preparation already completed: {state_dir}')
        return

    if not loaded:
        for folder in [Path(train_path), Path(val_path)]:
            existing = sorted(folder.glob(f'{shard_file_prefix}_*.npy'))
            assert not existing, (
                f'Output folder already contains shards but no resume state exists: {folder}'
            )

    if state.docs_seen > 0:
        logger.info(f'Resuming from doc offset: {state.docs_seen:,}')
        dataset = dataset.skip(state.docs_seen)

        # delete stale shards...
        train_writer.delete_shards_from_current_index()
        val_writer.delete_shards_from_current_index()

    logger.info('Preparing pretraining train and val shards...')

    stopped_on_target = False
    pool = mp.Pool(num_proc)

    try:
        iterator = pool.imap(
            partial(
                tokenize_and_route,
                tokenizer_kwargs,
                tokenize_function,
                seed,
                validation_ratio
            ),
            dataset,
            chunksize=chunksize
        )
        for source, tokens, split in iterator:
            state.docs_seen += 1

            if tokens.size == 0:
                continue
            if split == 'val':
                written = val_writer.write(tokens)
            else:
                written = train_writer.write(tokens)

            if written == 0:
                if reached_target():
                    stopped_on_target = True
                    break
                continue

            state.source_doc_counts[source] = state.source_doc_counts.get(source, 0) + 1
            state.source_token_counts[source] = state.source_token_counts.get(source, 0) + written
            state.split_doc_counts[split] += 1
            state.split_token_counts[split] += written

            if state.docs_seen % checkpoint_interval_docs == 0:
                save_state(state)

            if reached_target():
                stopped_on_target = True
                break

    except Exception:
        pool.terminate()
        pool.join()
        raise
    else:
        if stopped_on_target:
            pool.terminate()
        else:
            pool.close()
        pool.join()

    if target_tokens is not None and not reached_target():
        state.status = 'exhausted_before_target'
        save_state(state)
        raise RuntimeError(
            'Pretraining dataset exhausted before reaching target tokens. '
            f'train_tokens={train_writer.total_tokens:,}/{target_tokens:,}, '
            f'val_tokens={val_writer.total_tokens:,}/{val_target_tokens:,}'
        )

    train_writer.finish()
    val_writer.finish()

    state.status = 'completed'
    save_state(state)

    if stopped_on_target:
        logger.info(f'Reached target train tokens: {train_writer.total_tokens:,}')
        logger.info(f'Reached target val tokens: {val_writer.total_tokens:,}')

    # Workaround for occasional pool shutdown issue...
    # Without this, some streaming runs crash after successful shard writing with PyGILState_Release during finalization...
    logger.info('Ensuring pool is terminated...')
    time.sleep(5)

    logger.info('Pretraining shard preparation complete.')
    logger.info(f'- Train tokens: {train_writer.total_tokens:,}')
    logger.info(f'- Val tokens: {val_writer.total_tokens:,}')
    logger.info(f'- Train docs: {state.split_doc_counts["train"]:,}')
    logger.info(f'- Val docs: {state.split_doc_counts["val"]:,}')

    logger.info('Source document counts:')
    for source, count in sorted(state.source_doc_counts.items()):
        logger.info(f'- {source}: {count:,}')

    logger.info('Source token counts:')
    for source, count in sorted(state.source_token_counts.items()):
        logger.info(f'- {source}: {count:,}')
