import pytest

from tasks.models import Task

pytestmark = [pytest.mark.django_db]


def test(auth_client):
    got = auth_client.post('/api/v1/tasks/', data={
        'title': 'some task',
        'description': 'some task',
    })

    created_task = Task.objects.last()

    assert got.status_code == 201
    assert created_task.executor is not None
