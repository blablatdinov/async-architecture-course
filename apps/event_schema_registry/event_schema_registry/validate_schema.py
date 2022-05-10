import json
from pathlib import Path

from jschon import JSON, JSONSchema, create_catalog


BASE_DIR = Path(__file__).parent


def validate_schema(event: dict, event_name: str, version: int):
    create_catalog('2020-12')
    definition_file_path = _get_definition_file_path(event_name, version)
    with open(BASE_DIR / definition_file_path, 'r') as schema_file:
        schema = JSONSchema(json.load(schema_file))

    validation_result = schema.evaluate(JSON(event)).output('basic')
    if not validation_result['valid']:
        raise TypeError(json.dumps(validation_result, indent=2))


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
