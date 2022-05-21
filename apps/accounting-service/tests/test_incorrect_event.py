import json

import pytest

from accounting.services import event_callback
from accounting.models import IncorrectEvents

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def incorrect_event(mixer):
    return str.encode("""{"event_id": "716de44a-c0b2-44b9-8b74-5ae8a5c4439d", "event_version": 1, "event_name": "Task.Added", "event_time":
    "1652517206.153561", "producer": 1, "data": {"public_id": "5fa8dcfa-e30a-4f6c-ae02-e4ed3ca43ef8", "title":
    "some_title", "description": "some task",
    "executor_id": "e9091bb8-5c78-4388-8cf0-7e1654306c97", "jira_id": "UBERPOP-42"}}""")


def test(incorrect_event):
    event_callback('', '', '', incorrect_event)

    created_db_record = IncorrectEvents.objects.last()

    assert created_db_record.event == incorrect_event.decode('utf-8')
