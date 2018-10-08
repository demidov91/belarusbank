from unittest import mock

import pytest

from serverless_utils import (
    fix_cookie,
    json_response,
    parse_cookie,
    redirect_response_302,
    redirect_to_auth,
)


def test_redirect_response_302__simple_structure():
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


def test_redirect_response_302__headers():
    assert (
        redirect_response_302('http://nb.by/', headers={'Auth': 'anything'})['headers'] == {
            'Auth': 'anything',
            'Location': 'http://nb.by/',
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

    patched.assert_called_once_with('/auth?service=service-name&reason=cause-I-feel-like-it')


@mock.patch('json.dumps', return_value='{"a": 1}')
def test_json_response(patched):
    data = {'a': 1}

    result = json_response(data)

    assert result == {
        'statusCode': 200,
        'headers': {},
        'body': '{"a": 1}',
    }
    patched.assert_called_once_with(data,  ensure_ascii=False, indent=2)


def test_parse_cookie__positive():
    assert parse_cookie({'headers': {'Cookie': 'a=1; b=2;c=3;  d=4;', }, }) == {
        'a': '1',
        'b': '2',
        'c': '3',
        'd': '4',
    }


def test_parse_cookie__no_headers():
    assert parse_cookie({'something': {'Cookie': 'a=1; b=2;c=3;  d=4;', }, }) is None


def test_parse_cookie__no_cookie():
    assert parse_cookie({'headers': {'Mookie': 'a=1; b=2;c=3;  d=4;', }, }) is None


@pytest.mark.parametrize('cookie,provider,expected', [
    (
        {'s1-sessionId': '1', 's1-encryptKey': '2', 's2-sessionId': '3', 's2-encryptKey': '4', },
        's1',
        {'session_id': '1', 'encrypt_key': '2', 's2-sessionId': '3', 's2-encryptKey': '4', },
    ),
    (
        {'s1-sessionId': '1', 's1-encryptKey': '2', 's2-sessionId': '3', 's2-encryptKey': '4', },
        's2',
        {'session_id': '3', 'encrypt_key': '4', 's1-sessionId': '1', 's1-encryptKey': '2', },
    ),
    (
        {'s1-sessionId': '1', 's1-encryptKey': '2', 'any': 'thing', },
        's1',
        {'session_id': '1', 'encrypt_key': '2', 'any': 'thing', },
    ),
    (None, 's1', None),
])
def test_fix_cookie(cookie, provider, expected):
    assert fix_cookie(cookie, provider=provider) == expected
