import re
import json
import torch
import random
import numpy as np

from datetime import datetime, timezone


def clean_name(name):
    return re.sub(r'[^a-zA-Z0-9._-]+', '_', name).strip('_').lower()

def generate_timestamp():
    return datetime.now(timezone.utc)

def generate_name(timestamp=None, name=None) -> tuple[str, datetime]:
    if timestamp is None:
        timestamp = generate_timestamp()
    timestamp_str = timestamp.strftime('%Y%m%d_%H%M%S_UTC')
    if not name:
        return timestamp_str, timestamp
    return f'{timestamp_str}_{clean_name(name)}', timestamp

def convert_byte_to_gib(byte_data):
    return round(byte_data / (1024 ** 3), 2)

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def set_seed(seed: int, *, deterministic: bool = False):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

    if deterministic:
        torch.backends.cudnn.benchmark = False
        torch.backends.cudnn.deterministic = True
        torch.use_deterministic_algorithms(True, warn_only=True)
