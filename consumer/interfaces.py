import logging
import subprocess
from typing import Optional

import execution
from error import NetworkException


def check_device_existence(device: str) -> bool:
    result = subprocess.run(['ip', 'link', 'show', 'dev', device], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if result.stdout:
        return True
    else:
        return False


def init_bridge(bridge_device: str, phys_device: str, ip: Optional[str], gateway: Optional[str]) -> bool:
    if check_device_existence(bridge_device):
        logging.debug(f'Device {bridge_device} already exists, will not re-create')

        return True
    else:
        logging.debug(f'Creating bridge device {bridge_device}')

        commands = [
            ['ip', 'link', 'add', bridge_device, 'type', 'bridge'],
            ['ip', 'link', 'set', bridge_device, 'up'],
            ['ip', 'link', 'set', phys_device, 'up'],
            ['ip', 'link', 'set', phys_device, 'master', bridge_device],
            ['ip', 'addr', 'flush', 'dev', phys_device],
        ]

        if ip:
            commands.append(['ip', 'addr', 'add', ip, 'dev', bridge_device])
        if gateway:
            commands.append(['ip', 'route', 'add', 'default', 'via', gateway, 'dev', bridge_device])

        return execution.run_command_chain(commands)


def create_tap_device(tap_device_name, bridge_device_name, user) -> bool:
    creation_ok = execution.run_command_chain([
        ['ip', 'tuntap', 'add', 'dev', tap_device_name, 'mode', 'tap', 'user', user],
        ['ip', 'link', 'set', 'dev', tap_device_name, 'up'],
        ['ip', 'link', 'set', tap_device_name, 'master', bridge_device_name],
    ])

    return creation_ok
