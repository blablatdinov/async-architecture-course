import random

from django.contrib.auth import get_user_model
from event_schema_registry import validate_schema
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
    event_version = message['event_version']
    validate_schema(message, message['event_name'], version=2)
    logger.info('Task.Added event version: {event_version} consumed. Creating task...')
    if event_version == 1:
        task = Task.objects.create(
            id=message['data']['public_id'],
            title=message['data']['title'],
            executor_id=message['data']['executor_id'],
            status='created',
        )
        logger.info(f'Task {str(task.id)} created')
        return
    elif event_version == 2:
        task = Task.objects.create(
            id=message['data']['public_id'],
            title=message['data']['title'],
            jira_id=message['data']['jira_id'],
        )
        logger.info(f'Task {str(task.id)} created')
        return
    logger.warning(f'Task {str(task.id)} not created')


def set_task_executor(message: dict):
    logger.info('Task.Assigned event version: {event_version} consumed. Setting task executor...')
    task = Task.objects.get(id=message['data']['task_id'])
    task.executor_id = message['data']['executor_id']
    task.cost = random.randint(10, 20)
    task.status = 'assigned'
    task.award = random.randint(20, 40)
    # TODO: публиковать событие для аналитики
    task.save()


def reshuffle_task(message: dict):
    task = Task.objects.get(id=message['data']['task_public_id'])
    # TODO: списать с исполнителя деньги
    task.executor_id = message['data']['executor_id']
    task.cost = random.randint(10, 20)
    task.award = random.randint(20, 40)
    task.save()


def complete_task(message: dict):
    task = Task.objects.get(id=message['data']['task_public_id'])
    task.status = 'completed'
    # TODO: Начислить деньги
    # TODO: публиковать событие для аналитики
    task.save()
