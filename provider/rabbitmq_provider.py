import pika


QUEUE_NAME = 'vm-queue'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME)

channel.basic_publish(
    exchange='', routing_key=QUEUE_NAME, body=bytes("one VM please ^_^", "utf-8"))
