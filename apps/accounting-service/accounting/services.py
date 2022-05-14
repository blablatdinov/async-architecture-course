from django.contrib.auth import get_user_model
from loguru import logger

from accounting.models import Task

User = get_user_model()


def create_user(message: dict):
    logger.info('Auth.Registered event consumed. Creating user...')
    user = User.objects.create_user(
        id=message['data']['public_id'],
        username=message['data']['username'],
        role=message['data']['role'],
    )
    logger.info(f'User {str(user.id)} created')


def create_task(message: dict):
    logger.info('Task.Added event consumed. Creating task...')
    task = Task.objects.create(
        id=message['data']['public_id'],
        title=message['data']['title'],
        executor_id=message['data']['executor_id'],
    )
    logger.info(f'Task {str(task.id)} created')
