import os
import pytest

from json import load


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def event():
    with open(os.path.join(BASE_DIR, '..', 'event.json')) as f:
        return load(f)


@pytest.fixture
def context():
    return None
