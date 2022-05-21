from django.contrib.auth import get_user_model
from loguru import logger

User = get_user_model()


def create_user(message: dict):
    logger.info('Auth.Registered event consumed. Creating user...')
    user = User.objects.create_user(
        id=message['data']['public_id'],
        username=message['data']['username'],
        role=message['data']['role'],
    )
    logger.info(f'User {str(user.id)} created')


def write_off_balance(message: dict):
    user = User.objects.get(pk=message['data']['user_id'])
    user.today_award -= message['data']['cost']
    user.save()


def accrue_balance(message: dict):
    user = User.objects.get(pk=message['data']['user_id'])
    user.today_award += message['data']['sum']
    user.save()
