import os
import json
from pathlib import Path

from jsonschema import validate, ValidationError, Draft202012Validator
import pytest


BASE_DIR = Path(__file__).parent


def validate_schema(event: dict, event_name: str, version: int):
    definition_file_path = BASE_DIR / _get_definition_file_path(event_name, version)
    try:
        with open(definition_file_path, 'r') as schema_file:
            schema = json.load(schema_file)
    except FileNotFoundError:
        raise TypeError(f'Schema file for event {event_name} version: {version} not found')

    try:
        validate(instance=event, schema=schema)
    except ValidationError as e:
        raise TypeError('Schema file: {}. Error: {}'.format(definition_file_path, str(e)))


def _get_definition_file_path(event_name: str, version: int) -> str:
    return 'schemas/{}/{}.json'.format(
        event_name.lower().replace('.', '/'),
        version,
    )


def test_get_definition_file_path():
    got = _get_definition_file_path('Task.added', 1)

    assert got == 'schemas/task/added/1.json'


def test_validate_schema():
    got = validate_schema(
        {
            "event_id": "some_id",
            "event_version": 1,
            "event_name": "event_name",
            "event_time": "392409283",
            "producer": "some producer",
            "data": {
                "public_id": "some_task_public_id",
                "title": "taks title",
                "description": "",
                "executor_id": "some_executor_public_id",
            },
        },
        event_name='Task.added',
        version=1,
    )


@pytest.mark.parametrize('file_path', [
    f'{x[0]}/{x[2][0]}'
    for x in os.walk(BASE_DIR / 'schemas')
    if len(x[2]) > 0
])
def test_schemas(file_path):
    with open(file_path, 'r') as schema_file:
        schema = Draft202012Validator(schema=json.load(schema_file))
