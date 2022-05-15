import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=16)
    today_award = models.IntegerField(default=0)

    class Meta:
        db_table = 'auth_user'


class ManagementAward(models.Model):
    date = models.DateField()
    award = models.IntegerField()


class CountPopugWithNegativeAward(models.Model):
    date = models.DateField()
    award = models.IntegerField()
