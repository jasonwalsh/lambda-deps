import os
import requests

from base64 import b64decode
from http import HTTPStatus
from json import loads

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from github import Github


def handler(event, context):
    body = loads(event['body'])
    client = Github(os.getenv('GITHUB_TOKEN', ''))
    repository_name = body['repository']['full_name']
    repository = client.get_repo(repository_name)
    blob = repository.get_contents('deps.json')
    instance = loads(b64decode(blob.content))
    schema_url = os.getenv('SCHEMA_URL', '')
    schema = requests.get(schema_url).json()

    try:
        validate(instance=instance, schema=schema)
    except ValidationError:
        return {
            'statusCode': HTTPStatus.BAD_REQUEST
        }

    return {
        'statusCode': HTTPStatus.OK
    }
