import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture
def auth_client(mixer, client):
    client.force_authenticate(mixer.blend(User))
    return client


@pytest.fixture
def manager_client(mixer, client):
    client.force_authenticate(mixer.blend(User, role='manager'))
    return client


@pytest.fixture()
def mixer():
    from mixer.backend.django import mixer
    return mixer
