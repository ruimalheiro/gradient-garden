import json
import subprocess

from pathlib import Path
from importlib.metadata import version
from logger import logger
from engine.context import RunContext


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
        'workload_summary': workload_summary
    }

    snapshot_json = json.dumps(snapshot, indent=2, default=str)
    snapshot_path.write_text(snapshot_json, encoding='utf-8')

    logger.info(f'Snapshot saved to: {snapshot_path}')
