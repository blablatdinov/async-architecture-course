import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):

        def callback(ch, method, properties, body):
            try:
                # some logic
            except Exception as e:
                # some Notification

        settings.RABBITMQ_CHANNEL.basic_consume(
            queue='popug',
            auto_ack=True,
            on_message_callback=callback,
        )
        settings.RABBITMQ_CHANNEL.start_consuming()
