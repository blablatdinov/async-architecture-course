import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    status = models.CharField(max_length=16)
