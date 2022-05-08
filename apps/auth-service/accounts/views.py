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
        return Response(
            {'username': request.data['username'], 'group': request.data['group']},
            status=201,
        )


urlpatterns = [
    path('api/v1/accounts/', CreatePopug.as_view()),
]
