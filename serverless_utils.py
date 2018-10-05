import json
import logging
from functools import wraps

from constants import BASE_PATH

logger = logging.getLogger(__name__)


def redirect_response_302(url: str) -> dict:
    if url.startswith('/'):
        url = BASE_PATH[:-1] + '/' + url[1:]

    return {
        'statusCode': 302,
        'headers': {
            'Location': url,
        },
        'body': '',
    }


def json_response(data: dict) -> dict:
    return {
        'statusCode': 200,
        'body': json.dumps(data, ensure_ascii=False, indent=2),
    }

