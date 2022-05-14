import pytest
from django.contrib.auth import get_user_model

from tasks.models import Task

User = get_user_model()

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def executors(mixer):
    mixer.cycle(5).blend(User, role='popug')


@pytest.fixture(autouse=True)
def tasks(mixer):
    mixer.cycle(5).blend('tasks.Task')


def test(manager_client):
    got = manager_client.post('/api/v1/tasks/shuffle/')

    assert got.status_code == 201
    assert Task.objects.filter(executor__isnull=True).count() == 0
