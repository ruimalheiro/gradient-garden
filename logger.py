import json
import re

from pathlib import Path


ANSI_REMOVER_RGX = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

class ConsoleLogger:
    def __init__(self):
        self.is_master_process = False
        self.log_file_path = None
    
    def set_master(self, is_master_process):
        self.is_master_process = is_master_process

    def set_log_file_path(self, path):
        self.log_file_path = Path(path).with_suffix('.log')
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)

    def write_to_file(self, content):
        if self.log_file_path is None:
            return
        content = ANSI_REMOVER_RGX.sub('', str(content))
        with self.log_file_path.open('a', encoding='utf-8') as file:
            file.write(f'{content}\n')

    def info(self, content, force=False, pbar=None, is_json=False):
        if is_json:
            content = json.dumps(content, indent=4)
        if self.is_master_process or force:
            if pbar is not None:
                pbar.write(content)
            else:
                print(content)
            self.write_to_file(content)

    def separator(self, char='-', length=40, force=False, pbar=None):
        self.info(char * length, force=force, pbar=pbar)

    def section(self, title, char='-', length=40, force=False, pbar=None):
        self.info(f'\n{title}:', force=force, pbar=pbar)
        self.separator(char=char, length=length, force=force, pbar=pbar)

    def warning_wrapper(self, content):
        yellow = '\033[93m'
        reset = '\033[0m'
        return f'{yellow}WARNING: {content}{reset}'

    def warning(self, content, force=False, pbar=None, is_json=False):
        self.info(self.warning_wrapper(content), force=force, pbar=pbar, is_json=is_json)

    def error_wrapper(self, content):
        red = '\033[91m'
        reset = '\033[0m'
        return f'{red}ERROR: {content}{reset}'

    def error(self, content, force=True, pbar=None, is_json=False):
        self.info(self.error_wrapper(content), force=force, pbar=pbar, is_json=is_json)

logger = ConsoleLogger()
