def get_credentials(session_id: str, encrypt_key: str):
    print([session_id, encrypt_key])
    from settings import MTB_USERNAME, MTB_PASSWORD
    return (MTB_USERNAME, MTB_PASSWORD)


def serverless_get_password(event, context):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html', },
        'body': open('passwords/simple_password_form.html', mode='r').read(),
    }


def serverless_post_password(event, context):
    print(event)
    return {
        'statusCode': 302,
        'headers': {
            'Set-Cookie': 'sessionId=session-cookie; Max-Age=3600;',
            'Set-cookie': 'encryptKey=encrypt-cookie; Max-Age=3600;',
            'Location': event['queryStringParameters']['next'],
        },
        'body': '',

    }