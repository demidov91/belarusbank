import json
import logging
from functools import wraps
from http.cookies import SimpleCookie
from typing import Optional

from constants import BASE_PATH, SESSION_LIFETIME

logger = logging.getLogger(__name__)


def redirect_response_302(url: str, headers: Optional[dict]=None) -> dict:
    if url.startswith('/'):
        url = BASE_PATH[:-1] + '/' + url[1:]

    full_headers = {
        'Location': url,
    }
    full_headers.update(headers or {})

    return {
        'statusCode': 302,
        'headers': full_headers,
        'body': '',
    }


def redirect_to_auth(*, service: str, reason: str):
    return redirect_response_302(f'/auth?service={service}&reason={reason}')


def json_response(data: dict) -> dict:
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(data, ensure_ascii=False, indent=2),
    }


def get_session_id_cookie(provider: str) -> str:
    return f'{provider}-sessionId'


def get_encrypt_key_cookie(provider: str) -> str:
    return f'{provider}-encryptKey'


def build_session_cookie_headers(session_id: str, encrypted_key: str, *, provider: str) -> dict:
    return {
        'Set-Cookie':
            f'{get_session_id_cookie(provider)}={session_id}; Max-Age={SESSION_LIFETIME}; Secure',
        'Set-cookie':
            f'{get_encrypt_key_cookie(provider)}={encrypted_key}; Max-Age={SESSION_LIFETIME}; Secure'
    }


def parse_cookie(event):
    if 'headers' not in event or 'Cookie' not in event['headers']:
        logger.info('No cookie')
        return None

    return {
        k: v.value
        for k, v in SimpleCookie(event['headers']['Cookie']).items()
    }


def fix_cookie(cookie: Optional[dict], *, provider: str) -> Optional[dict]:
    if cookie is None:
        return None

    cookie['session_id'] = cookie.pop(get_session_id_cookie(provider), None)
    cookie['encrypt_key'] = cookie.pop(get_encrypt_key_cookie(provider), None)

    return cookie


def renewable_session(provider: str):
    def decorator(wrapped):
        @wraps(wrapped)
        def wrapper(event, context):
            cookie = fix_cookie(parse_cookie(event), provider=provider)
            event['cookie'] = cookie
            result = wrapped(event, context)
            if isinstance(result, dict) and result.get('statusCode') == 200 and cookie:
                result['headers'].update(build_session_cookie_headers(
                    cookie['session_id'],
                    cookie['encrypt_key'],
                    provider=provider)
                )

            return result
        return wrapper

    return decorator

