# Generated by Django 3.2.8 on 2022-05-07 11:32

from django.contrib.auth.models import Group
from django.db import migrations


def create_groups(*args):
    Group.objects.bulk_create([
        Group(name='popug'),
        Group(name='manager'),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups)
    ]