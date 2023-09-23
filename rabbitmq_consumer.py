import pika


QUEUE_NAME = 'vm-queue'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME)


def callback(ch, method, properties, body):
    print('Received message: ' + body.decode('utf-8'))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

channel.start_consuming()
