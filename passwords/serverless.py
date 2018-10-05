import json

from urllib.parse import parse_qs

from constants import SESSION_LIFETIME
from passwords import utils as passwords_utils
from serverless_utils import no_trailing_slash, json_response


@no_trailing_slash
def get_password(event, context):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html', },
        'body': open('passwords/simple_password_form.html', mode='r').read(),
    }


@no_trailing_slash
def post_password(event, context):
    data = parse_qs(event['body'])

    record_hash, encrypted_key = passwords_utils.save_credentials(
        data['username'][0],
        data['password'][0]
    )
    return {
        'statusCode': 302,
        'headers': {
            'Set-Cookie': f'sessionId={record_hash}; Max-Age={SESSION_LIFETIME};',
            'Set-cookie': f'encryptKey={encrypted_key}; Max-Age={SESSION_LIFETIME};',
            'Location': event['queryStringParameters']['next'],
        },
        'body': '',
    }


def clear_sessions(event, context):
    return passwords_utils.clear_sessions()