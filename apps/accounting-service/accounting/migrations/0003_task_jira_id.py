# Generated by Django 3.2.8 on 2022-05-14 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='jira_id',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
