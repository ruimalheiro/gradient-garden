import wandb

from datetime import datetime
from logger import logger


class WandbWrapper():
    def __init__(self, enabled=True, is_master_process=True, wandb_api_key=None):
        self.WANDB = False
        self.is_master_process = is_master_process

        if enabled and self.is_master_process:
            if wandb_api_key is not None:
                wandb.login(key=wandb_api_key)
                self.WANDB = True
                logger.info('Wandb enabled.')

    def init(self, project_name, *, job_name=None, config=None, output_path=None, parent_run_id=None, fork_step=None):
        if not self.WANDB:
            return
        
        if not job_name:
            job_start_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            job_name = f'run_{job_start_time}'

        wandb.init(
            project=project_name,
            name=job_name,
            config=config,
            dir=output_path,
            fork_from=f'{parent_run_id}?_step={fork_step}' if parent_run_id else None
        )

    def log(self, data, step, commit=True):
        if not self.WANDB:
            return
        wandb.log(data, step=step, commit=commit)

    def finish(self):
        if not self.WANDB:
            return
        wandb.finish()
