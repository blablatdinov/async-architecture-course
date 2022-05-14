from django.contrib import admin

from accounting.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Task._meta.fields]
