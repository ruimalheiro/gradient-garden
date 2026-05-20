import re

from datetime import datetime, timezone


def clean_name(name):
    return re.sub(r'[^a-zA-Z0-9._-]+', '_', name).strip('_').lower()

def generate_timestamp():
    return datetime.now(timezone.utc)

def generate_run_name(timestamp=None, name=None) -> dict:
    if timestamp is None:
        timestamp = generate_timestamp()
    timestamp_str = timestamp.strftime('%Y%m%d_%H%M%S_UTC')
    if not name:
        return timestamp_str, timestamp
    return f'{timestamp_str}_{clean_name(name)}', timestamp
