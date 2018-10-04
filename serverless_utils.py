import json
from functools import wraps


def redirect_response_302(url: str) -> dict:
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


def no_trailing_slash(wrapped):
    @wraps(wrapped)
    def wrapper(event, context):
        if (
            'requestContext' in event and
            'path' in event['requestContext'] and
            event['requestContext']['path'].endswith('/')
        ):
            return redirect_response_302(event['requestContext']['path'][:-1])

        return wrapped(event, context)

    return wrapper
