import pytest
from django.contrib.auth import get_user_model

from accounting.services import complete_task

pytestmark = [pytest.mark.django_db]
User = get_user_model()


@pytest.fixture
def task(mixer):
    return mixer.blend('accounting.Task')


@pytest.fixture
def executor(mixer):
    return mixer.blend(User, role='popug')


def test(task, executor):
    complete_task({
        'data': {
            'task_public_id': str(task.pk),
        },
    })
