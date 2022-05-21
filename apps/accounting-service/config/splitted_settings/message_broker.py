import datetime
import json
import uuid

import pika
from event_schema_registry import validate_schema
from loguru import logger

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
RABBITMQ_CHANNEL = connection.channel()
RABBITMQ_CHANNEL.queue_bind(exchange='popug-exchange', queue='accounting-service')


def publish_event(event_name: str, event_version: int, body: dict):
    event_id = str(uuid.uuid4())
    event = {
        "event_id": event_id,
        "event_version": event_version,
        "event_name": event_name,
        "event_time": str(datetime.datetime.now().timestamp()),
        "producer": "accounting service",
        "data": body,
    }
    try:
        validate_schema(event, event_name, event_version)
    except TypeError as e:
        # some notification
        raise e

    RABBITMQ_CHANNEL.basic_publish(
        exchange='popug-exchange',
        routing_key='',
        body=json.dumps(event),
    )
    logger.info(f'Event {event_name} published. Id: {event_id}')


RABBITMQ_CHANNEL.publish_event = publish_event
