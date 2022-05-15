import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def mixer():
    from mixer.backend.django import mixer
    return mixer


@pytest.fixture
def manager(mixer):
    mixer.blend(User, role='manager')


@pytest.fixture
def manager_api_client(manager, client):
    client.force_authenticate(manager)
    return client
