import pika
import subprocess
import os
import random
import string
import sys
import json
import psutil
from pathlib import Path

from error import QemuException
import interfaces


# rabbitMQ topic name
QUEUE_NAME = 'vm-queue'
MQTT_HOST = 'localhost'

BASE_IMAGE_FOLDER = Path('base_images')
USER_IMAGE_FOLDER = Path('user_images')

# open rabbitmq connections
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=MQTT_HOST))

channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME)


# create a new vm by using the user requested image
def create_vm(vm_id: str, image_name: str) -> Path:
    base_image = BASE_IMAGE_FOLDER / f'{image_name}.qcow2'
    if not base_image.is_file():
        raise IOError(f'Image "{image_name}" does not exist')

    user_image = USER_IMAGE_FOLDER / f'{vm_id}.qcow2'

    create_img_result = subprocess.run([
        'qemu-img', 'create', '-f', 'qcow2',
        '-b', str(base_image.absolute()), '-F', 'qcow2', str(user_image)])
    if create_img_result.returncode != 0:
        raise QemuException(f'could not create image for VM "{vm_id}"')

    return user_image


# call back method for rabbitmq consumer
def callback(channel_instance, method, properties, body):
    message = body.decode('utf-8')
    print('received message: ' + message)

    data = json.loads(message)

    if 'command' not in data:
        return
    elif data['command'] == 'start-vm':
        vm_id = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
        print(f'starting VM "{vm_id}"')

        try:
            image_name = os.path.basename(data['options']['image'])
        except KeyError:
            print('image not specified', file=sys.stderr)
            return

        try:
            user_image = create_vm(vm_id, image_name)
        except (OSError, QemuException) as e:
            print(str(e), file=sys.stderr)
            return

        tap_device = f'vm-{vm_id}'
        if not interfaces.create_tap_device(tap_device, 'br0', 'your-user'):
            print(f'could not create tap device for VM "{vm_id}"', file=sys.stderr)
            return

        mac_addr = interfaces.create_mac_address()
        print(f'assigning MAC address "{mac_addr}" to VM "{vm_id}"')

        p = subprocess.Popen([
            'qemu-system-x86_64', '-m', '4096', '-hda', str(user_image),
            '-device', f'virtio-net-pci,netdev=pubnet,mac={mac_addr}',
            '-netdev', f'tap,id=pubnet,ifname={tap_device},script=no,downscript=no',
            '-name', f'qemu-vm-{vm_id},process=vm-{vm_id}',
        ])
        print(f'started VM "{vm_id}" as process ID {p.pid}')

    channel_instance.basic_ack(delivery_tag=method.delivery_tag)


# start consuming
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

if not interfaces.check_device_existence('br0'):
    # br0 is the name of the bridge interfaces that will be created
    #     (can be anything)
    # enp0s25 is the name of your ethernet network, often eth0
    # 192.168.0.10/24 is the IP of your computer in the local network including
    #     subnet mask
    # 192.168.2.1 is the IP of your network gateway, in local networks usually
    #     your router
    interfaces.init_bridge('br0', 'enp0s25', '192.168.0.10/24', '192.168.0.1')

channel.start_consuming()
