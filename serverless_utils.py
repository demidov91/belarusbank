import json
import logging
from typing import Optional

from constants import BASE_PATH

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
        'body': json.dumps(data, ensure_ascii=False, indent=2),
    }

