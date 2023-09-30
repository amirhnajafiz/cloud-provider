import pika
from pathlib import Path
import subprocess

from error import QemuException


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
        raise QemuException(f'Could not create image for VM "{vm_id}"')

    return user_image


# call back method for rabbitmq consumer
def callback(ch, method, properties, body):
    print('Received message: ' + body.decode('utf-8'))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

channel.start_consuming()
