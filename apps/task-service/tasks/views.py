from django.contrib.auth import get_user_model
from django.urls import path
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Task

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'status',
        )


class TasksView(APIView):

    def get(self, request):
        return Response(
            TaskSerializer(Task.objects.filter(executor=request.user), many=True).data,
        )

    def post(self, request):
        executor = User.objects.order_by('?').first()
        Task.objects.create(
            executor=executor,
            title=request.data['title'],
            description=request.data['description'],
        )
        return Response(
            {'executor': executor.username, 'title': request.data['title'], 'description': request.data['description']},
            status=201,
        )


class TasksShuffleView(APIView):

    def post(self, request):
        if request.user.role != 'manager':
            raise PermissionDenied

        for task in Task.objects.all():
            task.executor = User.objects.order_by('?')
            task.save()

        return Response(status=201)


class TaskDetailView(APIView):

    def patch(self, request, task_id):
        task = Task.objects.get(pk=task_id)
        if request.user != task.executor:
            raise PermissionDenied

        for task in Task.objects.all():
            task.executor = User.objects.order_by('?').first()
            task.save()

        return Response(status=201)


def split_jira_topic_and_task_title(source_task_title: str) -> tuple[str, str]:
    splitted_string = source_task_title.split(']')
    jira_id = splitted_string[0][1:].strip()
    task_title = splitted_string[1].strip()
    return jira_id, task_title


urlpatterns = [
    path('api/v1/tasks/', TasksView.as_view()),
    path('api/v1/tasks/<int:task_id>/', TaskDetailView.as_view()),
    path('api/v1/tasks/shuffle/', TasksShuffleView.as_view()),
]
