from unittest import mock

from serverless_utils import (
    json_response,
    no_trailing_slash,
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


def test_no_trailing_slash__no_slash():
    wrapped = mock.Mock()
    wrapper = no_trailing_slash(wrapped)

    event = {'requestContext': {'path': '/some/url'}}
    context = mock.Mock()

    wrapper(event, context)

    wrapped.assert_called_once_with(event, context)


@mock.patch('serverless_utils.redirect_response_302', return_value=42)
def test_no_trailing_slash__with_slash(patched_redirect):
    wrapped = mock.Mock()
    wrapper = no_trailing_slash(wrapped)

    event = {'requestContext': {'path': '/some/url/'}}
    context = mock.Mock()

    assert wrapper(event, context) == 42

    patched_redirect.assert_called_once_with('/some/url')
