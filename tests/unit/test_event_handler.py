from unittest.mock import call, create_autospec, patch

from github.ContentFile import ContentFile
from jsonschema.exceptions import ValidationError

from functions.release import handler


@patch('functions.release.Github', autospec=True)
@patch('functions.release.b64decode')
@patch('functions.release.requests', autospec=True)
@patch('functions.release.validate')
@patch.dict('os.environ', {'GITHUB_TOKEN': 'secret'})
def test_event_handler(validate, requests, b64decode, Client, event, schema):
    context = None

    client = Client.return_value

    contents = create_autospec(
        ContentFile,
        content='eyJyZXBvc2l0b3JpZXMiOiBbIkNvZGVydG9jYXQvSGVsbG8tV29ybGQiXX0K'
    )

    client.get_repo.return_value.get_contents.return_value = contents

    b64decode.return_value = '{"repositories": ["Codertocat/Hello-World"]}'

    requests.get.return_value.json.return_value = schema

    # The first call to validate is successful, whereas the second call
    # raises an error.
    validate.side_effect = (None, ValidationError(''),)

    response = handler(event, context)

    assert Client.call_args == call('secret')
    assert client.get_repo.call_args == call('jasonwalsh/deps')
    assert b64decode.call_args == call(
        'eyJyZXBvc2l0b3JpZXMiOiBbIkNvZGVydG9jYXQvSGVsbG8tV29ybGQiXX0K'
    )

    assert validate.call_args == call(
        instance={'repositories': ['Codertocat/Hello-World']},
        schema=schema
    )

    assert response['statusCode'] == 200

    response = handler(event, context)

    assert response['statusCode'] == 400
