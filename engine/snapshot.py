import json
import subprocess
import platform
import torch
import os

from pathlib import Path
from importlib.metadata import version
from logger import logger
from engine.context import RunContext
from utils import convert_byte_to_gib


PROJECT_ROOT = Path(__file__).resolve().parent.parent

def git_commit_hash():
    try:
        return subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'],
            cwd=PROJECT_ROOT,
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return None

def get_packages_versions():
    requirements = (PROJECT_ROOT / 'requirements.txt').read_text().splitlines()
    valid_requirements = [req.strip() for req in requirements if req.strip() and not req.strip().startswith('#')]
    package_versions = []
    for package in valid_requirements:
        try:
            resolved = f'{package}=={version(package)}'
        except Exception:
            resolved = f'{package}==UNKNOWN'
        package_versions.append(resolved)

    return package_versions

def get_hardware_metadata():
    metadata = {
        'platform': platform.platform(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'cpu_count': os.cpu_count(),
        'cuda_available': torch.cuda.is_available(),
        'cuda_version': torch.version.cuda,
        'gpu_count': torch.cuda.device_count() if torch.cuda.is_available() else 0,
        'gpus': []
    }

    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            device_properties = torch.cuda.get_device_properties(i)
            metadata['gpus'].append({
                'name': device_properties.name,
                'vram_gib': convert_byte_to_gib(device_properties.total_memory),
                'multi_processor_count': device_properties.multi_processor_count
            })

    return metadata

def create_run_snapshot(*, run_ctx: RunContext, args, workload_summary, save_dir_path):
    snapshot_name = run_ctx.name
    timestamp = run_ctx.timestamp

    snapshot_dir = Path(save_dir_path)
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    snapshot_path = snapshot_dir / f'{snapshot_name}.json'

    snapshot = {
        'snapshot_name': snapshot_name,
        'snapshot_path': str(snapshot_path),
        'created_at_utc': timestamp.isoformat(),
        'args': vars(args),
        'git_commit_hash': git_commit_hash(),
        'requirements': get_packages_versions(),
        'hardware': get_hardware_metadata(),
        'workload_summary': workload_summary
    }

    snapshot_json = json.dumps(snapshot, indent=2, default=str)
    snapshot_path.write_text(snapshot_json, encoding='utf-8')

    logger.info(f'Snapshot saved to: {snapshot_path}')
