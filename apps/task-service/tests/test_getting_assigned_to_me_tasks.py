import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def popug_executor(mixer):
    return mixer.blend(User)


@pytest.fixture(autouse=True)
def task(mixer, popug_executor):
    return mixer.blend('tasks.Task', executor=popug_executor)


@pytest.fixture(autouse=True)
def alien_task(mixer, popug_executor):
    return mixer.blend('tasks.Task')


@pytest.fixture
def popug_api_client(client, popug_executor):
    client.force_authenticate(user=popug_executor)
    return client


def test(popug_api_client):
    got = popug_api_client.get('/api/v1/tasks/')

    assert got.status_code == 200
    assert len(got.json()) == 1
    assert list(got.json()[0].keys()) == ['id', 'title', 'description', 'status']
