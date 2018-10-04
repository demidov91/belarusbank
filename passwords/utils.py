import datetime
import logging
from typing import Tuple, Optional
from urllib.parse import parse_qs
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError
from cryptography.fernet import Fernet

from constants import SESSION_LIFETIME, STAGE, PASSWORDS_TABLE
from serverless_utils import no_trailing_slash


logger = logging.getLogger(__name__)


def get_credentials(session_id: str, encrypt_key: str) -> Tuple[Optional[str], Optional[str]]:
    table = _get_passwords_table()
    try:
        item = table.update_item(
            Key={'id': session_id},
            UpdateExpression='SET last_accessed_at = :current_time',
            ExpressionAttributeValues={':current_time': datetime.datetime.now().isoformat()},
            ReturnValues='ALL_OLD',
        )['Item']
    except KeyError:
        return None, None

    fernet_key = Fernet(encrypt_key.encode())
    return (
        fernet_key.decrypt(item['username'].encode()).decode(),
        fernet_key.decrypt(item['password'].encode()).decode(),
    )


def save_credentials(username: str, password: str) -> Tuple[str, str]:
    """
    :param username: plain username.
    :param password: plain password.
    :return: DB record hash and a secret key.
    """
    bytes_key = Fernet.generate_key()
    fernet_key = Fernet(bytes_key)
    encrypted_username = fernet_key.encrypt(username.encode()).decode()
    encrypted_password = fernet_key.encrypt(password.encode()).decode()
    record_hash = store_credentials(encrypted_username, encrypted_password)
    return record_hash, bytes_key.decode()


def _get_passwords_table():
    """
    This is a workaround to use both locally and on aws.
    :return:
    """
    if STAGE != 'local':
        return boto3.resource('dynamodb', region_name='eu-central-1').Table(PASSWORDS_TABLE)

    db = boto3.resource(
        'dynamodb',
        endpoint_url='http://localhost:8000',
        region_name='eu-central-1'
    )

    try:
        db.meta.client.describe_table(TableName=PASSWORDS_TABLE)
    except ClientError:
        return db.create_table(
            TableName=PASSWORDS_TABLE,
            AttributeDefinitions=[{
                'AttributeName': 'id',
                'AttributeType': 'S',
            }],
            KeySchema=[{
                'AttributeName': 'id',
                'KeyType': 'HASH',
            }],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1,
            }
        )

    return db.Table(PASSWORDS_TABLE)



def store_credentials(encrypted_username: str, encrypted_password: str) -> str:
    table = _get_passwords_table()
    item_hash = str(uuid4())
    table.put_item(Item={
        'id': item_hash,
        'username': encrypted_username,
        'password': encrypted_password,
        'last_accessed_at': datetime.datetime.now().isoformat(),
    })
    return item_hash


@no_trailing_slash
def serverless_get_password(event, context):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html', },
        'body': open('passwords/simple_password_form.html', mode='r').read(),
    }


@no_trailing_slash
def serverless_post_password(event, context):
    data = parse_qs(event['body'])

    record_hash, encrypted_key = save_credentials(data['username'][0], data['password'][0])
    return {
        'statusCode': 302,
        'headers': {
            'Set-Cookie': f'sessionId={record_hash}; Max-Age={SESSION_LIFETIME};',
            'Set-cookie': f'encryptKey={encrypted_key}; Max-Age={SESSION_LIFETIME};',
            'Location': event['queryStringParameters']['next'],
        },
        'body': '',

    }
