# Generated by Django 3.2.8 on 2022-05-15 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0005_user_today_award'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncorrectEvents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('event', models.TextField()),
                ('exception_text', models.TextField()),
            ],
        ),
    ]