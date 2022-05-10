import json

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
RABBITMQ_CHANNEL = connection.channel()

RABBITMQ_CHANNEL.queue_declare(queue='popug')


def publish_event(title, body):
    RABBITMQ_CHANNEL.basic_publish(
        exchange='',
        routing_key='popug',
        body=json.dumps({'title': title, 'body': body}),
    )


RABBITMQ_CHANNEL.publish_event = publish_event
