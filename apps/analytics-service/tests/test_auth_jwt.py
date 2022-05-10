import jwt
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

pytestmark = [pytest.mark.django_db]

User = get_user_model()


@pytest.fixture(autouse=True)
def popug_user(mixer):
    user = mixer.blend(User, username='popug1')
    user.set_password('1')
    user.save()
    user.groups.add(Group.objects.get(name='popug'))
    return user


def test(client):
    got = client.post('/api/token/', data={
        'username': 'popug1',
        'password': '1',
    })
    decoded_token = jwt.decode(got.json()['access'], settings.SECRET_KEY, algorithms=['HS256'])

    assert got.status_code == 200
    assert list(decoded_token.keys()) == ['token_type', 'exp', 'iat', 'jti', 'user_id', 'account_type']
    assert decoded_token['account_type'] == 'popug'
