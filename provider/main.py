import pika
import json


# rabbitMQ topic name
QUEUE_NAME = 'vm-queue'
MQTT_HOST = 'localhost'


class ServerCommunication:
    def __init__(self):
        self.queue = QUEUE_NAME

    def __enter__(self):
        # opening a connection to rabbit channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQTT_HOST))

        # connecting to provided channel
        self.channel = self.connection.channel()

        # create a queue
        self.channel.queue_declare(queue=QUEUE_NAME)

        # create a basic consume for response handler
        self.channel.basic_consume(
            queue='amq.rabbitmq.reply-to',
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, properties, body):
        pass
