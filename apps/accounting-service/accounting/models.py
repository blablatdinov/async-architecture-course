import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=16)

    class Meta:
        db_table = 'auth_user'


class Task(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=16)
    executor = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    cost = models.IntegerField(null=True)
    status = models.CharField(max_length=16)
    award = models.IntegerField(null=True)
    jira_id = models.CharField(null=True, max_length=16)
