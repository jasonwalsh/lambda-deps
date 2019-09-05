import os
import pytest

from json import load


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def event():
    with open(os.path.join(BASE_DIR, '..', 'event.json')) as f:
        return load(f)


@pytest.fixture
def schema():
    return {
        '$schema': 'http://json-schema.org/draft-07/schema#',
        'properties': {
            'repositories': {
                'items': {
                    'type': 'string'
                },
                'type': 'array'
            }
        },
        'type': 'object'
    }
