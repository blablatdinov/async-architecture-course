import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):

        def callback(ch, method, properties, body):
            message = json.loads(body.decode('utf-8'))
            if message['title'] != 'Auth.Registered':
                return

            User.objects.create_user(
                id=message['data']['id'],
                username=message['data']['username'],
                role=message['data']['group'],
            )

        settings.RABBITMQ_CHANNEL.basic_consume(
            queue='popug',
            auto_ack=True,
            on_message_callback=callback,
        )
        settings.RABBITMQ_CHANNEL.start_consuming()
