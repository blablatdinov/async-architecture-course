import json

import pika
from event_schema_registry import validate_schema

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
RABBITMQ_CHANNEL = connection.channel()

RABBITMQ_CHANNEL.queue_declare(queue='popug')


def publish_event(body):
    try:
        validate_schema(body, body['event_name'], body['event_version'])
    except TypeError as e:
        # some notification
        raise e
    RABBITMQ_CHANNEL.basic_publish(
        exchange='',
        routing_key='popug',
        body=json.dumps(body),
    )


RABBITMQ_CHANNEL.publish_event = publish_event
