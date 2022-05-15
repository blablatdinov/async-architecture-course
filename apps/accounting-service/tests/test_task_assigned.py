import pytest
from django.contrib.auth import get_user_model

from accounting.services import set_task_executor

pytestmark = [pytest.mark.django_db]
User = get_user_model()


@pytest.fixture
def task(mixer):
    return mixer.blend('accounting.Task')


@pytest.fixture
def executor(mixer):
    return mixer.blend(User)


def test(task, executor):
    set_task_executor({
        'data': {
            'task_id': str(task.pk),
            'executor_id': str(executor.pk),
        },
    })
