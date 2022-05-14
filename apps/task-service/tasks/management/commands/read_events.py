import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from loguru import logger

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):

        def callback(ch, method, properties, body):
            try:
                message = json.loads(body.decode('utf-8'))
                if message.get('event_name') != 'Auth.Registered':
                    return

                logger.info('Auth.Registered event consumed. Creating user...')

                user = User.objects.create_user(
                    id=message['data']['public_id'],
                    username=message['data']['username'],
                    role=message['data']['role'],
                )
                logger.info(f'User {str(user.id)} created')
            except Exception as e:
                # some notification
                logger.error(f'Cannot handle Auth.Registered event. Error: {str(e)}')
                pass

        settings.RABBITMQ_CHANNEL.basic_consume(
            queue='task-service',
            auto_ack=True,
            on_message_callback=callback,
        )
        logger.info('Start read events...')
        settings.RABBITMQ_CHANNEL.start_consuming()
