from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    role = models.CharField(max_length=16)

    class Meta:
        db_table = 'auth_user'
