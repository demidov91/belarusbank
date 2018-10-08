from urllib.parse import parse_qs

from passwords import utils as passwords_utils
from serverless_utils import redirect_response_302, build_session_cookie_headers


def get_password(event, context):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html', },
        'body': open('passwords/simple_password_form.html', mode='r').read(),
    }


def post_password(event, context):
    data = parse_qs(event['body'])
    service_name = event['queryStringParameters']['service']

    record_hash, encrypted_key = passwords_utils.save_credentials(
        data['username'][0],
        data['password'][0]
    )
    return redirect_response_302(
        f'/{service_name}',
        headers=build_session_cookie_headers(record_hash, encrypted_key, provider=service_name)
    )


def clear_sessions(event, context):
    return passwords_utils.clear_sessions()
