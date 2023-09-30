import logging
import subprocess
from typing import List


def run_command_chain(commands: List[List[str]]) -> bool:
    for command in commands:
        logging.debug(f'Running command: {" ".join(command)}')
        result = subprocess.run(command)

        if result.returncode != 0:
            return False

    return True
