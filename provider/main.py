import pika
import json
import argparse
import sys


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
        print(json.loads(body))

    def send_msg(self, cdata):
        response = None

        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            properties=pika.BasicProperties(
                reply_to='amq.rabbitmq.reply-to',
                content_type='application/json'
            ),
            body=json.dumps(cdata).encode('utf-8')
        )

        self.channel.start_consuming()

        return response

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cloud Provider')
    subparsers = parser.add_subparsers(dest='subparser_name')
    create_vm_parser = subparsers.add_parser('start-vm')
    create_vm_parser.add_argument(
        '--image', help='Name of the image to start', required=True)
    subparsers.add_parser('list-vms')
    args = parser.parse_args()

    if args.subparser_name == 'list-vms':
        data = {
            'command': 'list-vms',
        }
    elif args.subparser_name == 'start-vm':
        data = {
            'command': 'start-vm',
            'options': {
                'image': args.image,
            }
        }
    else:
        print('Command does not exist', file=sys.stderr)
        sys.exit(1)

    c = ServerCommunication()
    c.send_msg(data)
