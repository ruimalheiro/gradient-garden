import numpy as np
import sys
import multiprocessing as mp
import math

from tqdm.auto import tqdm
from functools import partial
from pathlib import Path
from utils import save_json_file
from datasets_preparation.utils.common import stable_hash
from datasets_preparation.utils.state import PreparationState
from logger import logger


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
    chunksize,
    state: PreparationState
):
    def save_state(
        state: PreparationState,
        train_writer: ShardWriter,
        val_writer: ShardWriter
    ):
        state_data = {
            'path': state.path,
            'status': state.status,
            'docs_seen': state.docs_seen,
            'source_metadata': state.source_metadata,
            'source_states': state.source_states,
            'source_doc_counts': state.source_doc_counts,
            'source_token_counts': state.source_token_counts,
            'split_doc_counts': state.split_doc_counts,
            'split_token_counts': state.split_token_counts,
            'train_writer_state': train_writer.get_state_dict(),
            'train_writer_buffer_file_path': state.train_writer_buffer_file_path,
            'val_writer_state': val_writer.get_state_dict(),
            'val_writer_buffer_file_path': state.val_writer_buffer_file_path
        }

        state_path = Path(state.path)
        train_writer_buffer_file_path = Path(state.train_writer_buffer_file_path)
        val_writer_buffer_file_path = Path(state.val_writer_buffer_file_path)

        temp_state_path = state_path.with_name(f'{state_path.name}.tmp')
        temp_train_buffer_path = train_writer_buffer_file_path.with_name(f'{train_writer_buffer_file_path.stem}.tmp.npy')
        temp_val_buffer_path = val_writer_buffer_file_path.with_name(f'{val_writer_buffer_file_path.stem}.tmp.npy')

        try:
            np.save(temp_train_buffer_path, train_writer.get_buffer_checkpoint())
            np.save(temp_val_buffer_path, val_writer.get_buffer_checkpoint())
            save_json_file(temp_state_path, state_data, indent=2)

            temp_train_buffer_path.replace(train_writer_buffer_file_path)
            temp_val_buffer_path.replace(val_writer_buffer_file_path)
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

    if state.status == 'completed':
        logger.info(f'Pretraining data preparation already completed: {state.path}')
        return

    if state.docs_seen == 0:
        for folder in [Path(train_path), Path(val_path)]:
            existing = sorted(folder.glob(f'{shard_file_prefix}_*.npy'))
            assert not existing, (
                f'Output folder already contains shards but no resume state exists: {folder}'
            )
    else:
        if state.train_writer_state:
            train_writer.load_state_dict(state.train_writer_state)
        if state.train_writer_buffer_file_path:
            train_writer.load_buffer_checkpoint(np.load(state.train_writer_buffer_file_path))

        if state.val_writer_state:
            val_writer.load_state_dict(state.val_writer_state)
        if state.val_writer_buffer_file_path:
            val_writer.load_buffer_checkpoint(np.load(state.val_writer_buffer_file_path))

    # delete stale shards...
    train_writer.delete_shards_from_current_index()
    val_writer.delete_shards_from_current_index()

    logger.info('Preparing pretraining train and val shards...')

    stopped_on_target = False
    pool = mp.Pool(num_proc)
    stop_event = mp.Event()

    def stoppable_dataset(ds, stop_event):
        for doc in ds:
            if stop_event.is_set():
                return
            yield doc

    iterator = pool.imap(
        partial(
            tokenize_and_route,
            tokenizer_kwargs,
            tokenize_function,
            seed,
            validation_ratio
        ),
        # dataset,
        stoppable_dataset(dataset, stop_event),
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
                stop_event.set()
                stopped_on_target = True
                break
            continue

        state.source_doc_counts[source] = state.source_doc_counts.get(source, 0) + 1
        state.source_token_counts[source] = state.source_token_counts.get(source, 0) + written
        state.split_doc_counts[split] += 1
        state.split_token_counts[split] += written

        if state.docs_seen % checkpoint_interval_docs == 0:
            save_state(state, train_writer, val_writer)

        if reached_target():
            stop_event.set()
            stopped_on_target = True
            break

    train_writer.finish()
    val_writer.finish()

    if target_tokens is not None and not reached_target():
        state.status = 'exhausted_before_target'
        save_state(state, train_writer, val_writer)
        raise RuntimeError(
            'Pretraining dataset exhausted before reaching target tokens. '
            f'train_tokens={train_writer.total_tokens:,}/{target_tokens:,}, '
            f'val_tokens={val_writer.total_tokens:,}/{val_target_tokens:,}'
        )

    state.status = 'completed'
    save_state(state, train_writer, val_writer)

    if stopped_on_target:
        logger.info(f'Reached target train tokens: {train_writer.total_tokens:,}')
        logger.info(f'Reached target val tokens: {val_writer.total_tokens:,}')

    logger.info('\nTerminating pool...')
    pool.close()
    pool.join()

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
