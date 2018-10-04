from unittest import mock

from serverless_utils import (
    json_response,
    redirect_response_302,
)


def test_redirect_response_302():
    assert (
        redirect_response_302('http://nb.by/') ==
        {
            'statusCode': 302,
            'headers': {
                'Location': 'http://nb.by/',
            },
            'body': '',
        }
    )


@mock.patch('json.dumps', return_value='{"a": 1}')
def test_json_response(patched):
    data = {'a': 1}

    result = json_response(data)

    assert result == {
        'statusCode': 200,
        'body': '{"a": 1}',
    }
    patched.assert_called_once_with(data,  ensure_ascii=False, indent=2)
