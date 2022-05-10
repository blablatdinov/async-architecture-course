import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APIClient

pytestmark = [pytest.mark.django_db]
User = get_user_model()


@pytest.fixture
def manager(mixer):
    user = mixer.blend(User, username='manager')
    user.groups.add(Group.objects.get(name='manager'))
    return user


@pytest.fixture
def manager_client(manager):
    client = APIClient()
    client.force_authenticate(user=manager)
    return client


def test(manager_client):
    got = manager_client.post('/api/v1/accounts/', data={
        'username': 'popug2',
        'group': 'popug',
    })

    created_popug = User.objects.last()

    assert got.status_code == 201
    assert created_popug.username == got.json()['username'] == 'popug2'
    assert created_popug.groups.first().name == 'popug'
