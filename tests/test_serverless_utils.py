from unittest import mock

import pytest

from serverless_utils import (
    json_response,
    redirect_response_302,
    redirect_to_auth,
)


def test_redirect_response_302__structure():
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


@pytest.mark.parametrize('url,location', [
    ('/', '/'),
    ('/abc', '/abc'),
    ('abc', 'abc'),
    ('abc/def', 'abc/def'),
])
@mock.patch('serverless_utils.BASE_PATH', '/')
def test_redirect_response_302__base_root_path(url, location):
    assert redirect_response_302(url)['headers']['Location'] == location


@pytest.mark.parametrize('url,location', [
    ('/', '/branch-name/'),
    ('/abc', '/branch-name/abc'),
    ('abc', 'abc'),
    ('abc/def', 'abc/def'),
])
@mock.patch('serverless_utils.BASE_PATH', '/branch-name/')
def test_redirect_response_302__base_custom_path(url, location):
    assert redirect_response_302(url)['headers']['Location'] == location


@mock.patch('serverless_utils.redirect_response_302', return_value='42')
def test_redirect_to_auth(patched):
    assert redirect_to_auth(service='service-name', reason='cause-I-feel-like-it') == '42'

    patched.assert_called_once_with('/auth?service=/service-name&reason=cause-I-feel-like-it')


@mock.patch('json.dumps', return_value='{"a": 1}')
def test_json_response(patched):
    data = {'a': 1}

    result = json_response(data)

    assert result == {
        'statusCode': 200,
        'body': '{"a": 1}',
    }
    patched.assert_called_once_with(data,  ensure_ascii=False, indent=2)
