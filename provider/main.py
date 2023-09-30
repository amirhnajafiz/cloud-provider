import pika
import json


# rabbitMQ topic name
QUEUE_NAME = 'vm-queue'
MQTT_HOST = 'localhost'

# opening a connection to rabbit channel
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=MQTT_HOST))

# connecting to provided channel
channel = connection.channel()

# create a queue
channel.queue_declare(queue=QUEUE_NAME)

# message to send
message = json.dumps({
    'command': 'start-vm',
    'options': {
        'image': 'ubuntu_base',
    }
})

# publish message
channel.basic_publish(
    exchange='', routing_key=QUEUE_NAME, body=bytes(message, "utf-8"))
