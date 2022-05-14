import json

import pika
from event_schema_registry import validate_schema
from loguru import logger

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
RABBITMQ_CHANNEL = connection.channel()
RABBITMQ_CHANNEL.queue_bind(exchange='popug-exchange', queue='accounting-service')


def publish_event(body):
    event_name = body['event_name']
    try:
        validate_schema(body, event_name, body['event_version'])
    except TypeError as e:
        # some notification
        raise e
    RABBITMQ_CHANNEL.basic_publish(
        exchange='popug-exchange',
        routing_key='',
        body=json.dumps(body),
    )
    logger.info(f'Event {event_name} published. Id: {body["event_id"]}')


RABBITMQ_CHANNEL.publish_event = publish_event
