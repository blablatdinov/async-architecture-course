import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from loguru import logger

from accounting.services import create_task, create_user, set_task_executor

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):

        def callback(ch, method, properties, body):
            message = json.loads(body.decode('utf-8'))
            event_name = message.get('event_name')
            try:
                event_handler = {
                    'Auth.Registered': create_user,
                    'Task.Added': create_task,
                    'Task.Assigned': set_task_executor,
                }.get(event_name)
                if event_handler:
                    event_handler(message)
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
