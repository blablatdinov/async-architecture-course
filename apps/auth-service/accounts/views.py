import datetime
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import path
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()


class CreatePopug(APIView):

    def post(self, request):
        user = User.objects.create_user(username=request.data['username'])
        user.groups.add(Group.objects.get(name=request.data['group']))
        string_user_id = str(user.id)
        account_data = {'id': string_user_id, 'username': request.data['username'], 'group': request.data['group']}
        settings.RABBITMQ_CHANNEL.publish_event({
            'event_id': str(uuid.uuid4()),
            'event_version': 1,
            'event_name': 'Auth.Registered',
            'event_time': str(datetime.datetime.now().timestamp()),
            'producer': 'auth service',
            'data': {
                'public_id': string_user_id,
                'username': user.username,
                'role': account_data['group'],
            },
        })
        return Response(
            account_data,
            status=201,
        )


urlpatterns = [
    path('api/v1/accounts/', CreatePopug.as_view()),
]
