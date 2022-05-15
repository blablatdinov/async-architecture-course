from django.core.management.base import BaseCommand

from accounting.services import consuming_events


class Command(BaseCommand):

    def handle(self, *args, **options):
        consuming_events()
