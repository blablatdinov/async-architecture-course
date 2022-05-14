import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from event_schema_registry import validate_schema
from loguru import logger

from accounting.services import complete_task, create_task, create_user, reshuffle_task, set_task_executor

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):

        def callback(ch, method, properties, body):
            message = json.loads(body.decode('utf-8'))
            event_name = message.get('event_name')
            event_version = message.get('event_version')
            try:
                event_handler = {
                    'Auth.Registered': create_user,
                    'Task.Added': create_task,
                    'Task.Assigned': set_task_executor,
                    'Task.Shuffled': reshuffle_task,
                    'Task.Completed': complete_task,
                }.get(event_name)
                if event_handler:
                    logger.info(f'{event_name} version: {event_version} consumed.')
                    validate_schema(message, message['event_name'], message['event_version'])
                    event_handler(message)
                    logger.info(f'{event_name} version: {event_version} handled.')
            except Exception as e:
                # some notification
                logger.error(f'Cannot handle {event_name} event. Error: {str(e)}')
                pass

        settings.RABBITMQ_CHANNEL.basic_consume(
            queue='accounting-service',
            auto_ack=True,
            on_message_callback=callback,
        )
        logger.info('Start read events...')
        settings.RABBITMQ_CHANNEL.start_consuming()
