import datetime
import uuid

from django.conf import settings
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


class TaskSerializerV2(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'status',
            'jira_id',
        )


class TasksView(APIView):

    def get(self, request):
        return Response(
            TaskSerializer(Task.objects.filter(executor=request.user), many=True).data,
        )

    def _publish_event(self, task: Task):
        settings.RABBITMQ_CHANNEL.publish_event(
            {
                "event_id": str(uuid.uuid4()),
                "event_version": 1,
                "event_name": "Task.Added",
                "event_time": str(datetime.datetime.now().timestamp()),
                "producer": "task service",
                "data": {
                    "public_id": str(task.pk),
                    "title": task.title,
                    "description": task.description,
                    # "executor_id": str(task.executor_id),
                    "executor_id": 'e9091bb8-5c78-4388-8cf0-7e1654306c97',
                },
            },
        )

    def post(self, request):
        executor = User.objects.order_by('?').first()
        task = Task.objects.create(
            executor=executor,
            title=request.data['title'],
            description=request.data['description'],
        )
        self._publish_event(task)
        return Response(
            {'executor': executor.username, 'title': request.data['title'], 'description': request.data['description']},
            status=201,
        )


class TasksViewV2(APIView):

    def get(self, request):
        return Response(
            TaskSerializerV2(Task.objects.filter(executor=request.user), many=True).data,
        )

    def _publish_events(self, task: Task):
        settings.RABBITMQ_CHANNEL.publish_event(
            {
                "event_id": str(uuid.uuid4()),
                "event_version": 2,
                "event_name": "Task.Added",
                "event_time": str(datetime.datetime.now().timestamp()),
                "producer": "task service",
                "data": {
                    "public_id": str(task.pk),
                    "title": task.title,
                    "description": task.description,
                    # "executor_id": str(task.executor_id),
                    "executor_id": 'e9091bb8-5c78-4388-8cf0-7e1654306c97',
                    "jira_id": task.jira_id,
                },
            },
        )
        settings.RABBITMQ_CHANNEL.publish_event(
            {
                "event_id": str(uuid.uuid4()),
                "event_version": 1,
                "event_name": "Task.Assigned",
                "event_time": str(datetime.datetime.now().timestamp()),
                "producer": "task service",
                "data": {
                    # "executor_id": str(task.executor_id),
                    "executor_id": 'e9091bb8-5c78-4388-8cf0-7e1654306c97',
                    "task_id": str(task.pk),
                },
            },
        )

    def post(self, request):
        executor = User.objects.order_by('?').first()
        jira_id, title = split_jira_topic_and_task_title(request.data['title'])
        task = Task.objects.create(
            executor=executor,
            title=title,
            jira_id=jira_id,
            description=request.data['description'],
        )
        self._publish_events(task)
        return Response(
            {
                'executor': executor.username,
                'title': title,
                'jira_id': jira_id,
                'description': request.data['description'],
            },
            status=201,
        )


class TasksShuffleView(APIView):

    def post(self, request):
        if request.user.role != 'manager':
            raise PermissionDenied

        for task in Task.objects.all():
            task.executor = User.objects.exclude(status='completed').order_by('?').first()
            task.save()
            settings.RABBITMQ_CHANNEL.publish_event(
                {
                    "event_id": str(uuid.uuid4()),
                    "event_version": 1,
                    "event_name": "Task.Shuffled",
                    "event_time": str(datetime.datetime.now().timestamp()),
                    "producer": "task service",
                    "data": {
                        # "executor_id": str(task.executor_id),
                        "executor_id": 'e9091bb8-5c78-4388-8cf0-7e1654306c97',
                        # "task_public_id": str(task.pk),
                        "task_public_id": '4d04aa77-29d6-474c-a30e-edd35897d344',
                    },
                },
            )

        return Response(status=201)


class TaskDetailView(APIView):

    def patch(self, request, task_id):
        task = Task.objects.get(pk=task_id)
        if request.user != task.executor:
            raise PermissionDenied

        task.status = request.data['status']
        settings.RABBITMQ_CHANNEL.publish_event(
            {
                "event_id": str(uuid.uuid4()),
                "event_version": 1,
                "event_name": "Task.Completed",
                "event_time": str(datetime.datetime.now().timestamp()),
                "producer": "task service",
                "data": {
                    # "task_public_id": str(task.pk),
                    "task_public_id": '4d04aa77-29d6-474c-a30e-edd35897d344',
                },
            },
        )
        task.save()

        return Response(status=201)


def split_jira_topic_and_task_title(source_task_title: str) -> tuple[str, str]:
    splitted_string = source_task_title.split(']')
    jira_id = splitted_string[0][1:].strip()
    task_title = splitted_string[1].strip()
    return jira_id, task_title


urlpatterns = [
    path('api/v1/tasks/', TasksView.as_view()),
    path('api/v2/tasks/', TasksViewV2.as_view()),
    path('api/v1/tasks/<str:task_id>/', TaskDetailView.as_view()),
    path('api/v1/tasks/shuffle/', TasksShuffleView.as_view()),
]
