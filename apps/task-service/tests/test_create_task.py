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


def test_v2(auth_client):
    got = auth_client.post('/api/v2/tasks/', data={
        'title': '[UBERPOP-42] Поменять оттенок зелёного на кнопке',
        'description': 'some task',
    })

    created_task = Task.objects.last()

    assert got.status_code == 201
    assert created_task.executor is not None
    assert created_task.jira_id == 'UBERPOP-42'
    assert created_task.title == 'Поменять оттенок зелёного на кнопке'
