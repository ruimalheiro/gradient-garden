import numpy as np
import torch
import torch.nn.functional as F

from torch.nn.utils.rnn import pad_sequence


def load_tokens(filename):
    npt = np.load(filename, allow_pickle=False)
    if npt.dtype != np.int64:
        npt = npt.astype(np.int64)
    ptt = torch.from_numpy(npt)
    return ptt

def pad_batch_to_multiple_of(*, sequences, padding_value, multiple, max_length=None):
    padded = pad_sequence(
        sequences,
        batch_first=True,
        padding_value=padding_value
    )

    if multiple is None or multiple <= 1:
        return padded

    seq_len = padded.size(1)
    target_len = ((seq_len + multiple - 1) // multiple) * multiple
    if max_length is not None:
        target_len = min(target_len, max_length)

    remaining = target_len - seq_len
    if remaining <= 0:
        return padded
    return F.pad(padded, (0, remaining), value=padding_value)
