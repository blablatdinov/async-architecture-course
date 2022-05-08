import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def popug(mixer):
    return mixer.blend(User, role='popug')


@pytest.fixture
def task(mixer, popug):
    return mixer.blend('tasks.Task', executor=popug)


@pytest.fixture
def popug_api_client(popug, client):
    client.force_authenticate(popug)
    return client


def test(popug_api_client, task):
    got = popug_api_client.patch(f'/api/v1/tasks/{task.pk}/', data={
        'status': 'completed',
    })

    assert got.status_code == 201
