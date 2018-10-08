import datetime
import logging
from typing import Tuple, Optional
from uuid import uuid4

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from cryptography.fernet import Fernet

from constants import STAGE, PASSWORDS_TABLE, SESSION_LIFETIME


logger = logging.getLogger(__name__)


def get_credentials(session_id: str, encrypt_key: str) -> Tuple[Optional[str], Optional[str]]:
    table = _get_passwords_table()
    try:
        item = table.update_item(
            Key={'id': session_id},
            UpdateExpression='SET last_accessed_at = :current_time',
            ExpressionAttributeValues={':current_time': datetime.datetime.now().isoformat()},
            ReturnValues='ALL_OLD',
        )['Attributes']
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


def get_cedentials_by_cookie_data(cookie_data: dict) -> Optional[Tuple[str, str]]:
    if (
        not cookie_data or
        not cookie_data.get('session_id') or
        not cookie_data.get('encrypt_key')
    ):
        logger.info('No cookie')
        return None

    username, password = get_credentials(
        session_id=cookie_data['session_id'],
        encrypt_key=cookie_data['encrypt_key']
    )

    if not (username and password):
        return None

    return username, password


def clear_sessions():
    table = _get_passwords_table()
    id_list = [
        x['id'] for x in
        table.scan(FilterExpression=Attr('last_accessed_at').lt(
            (datetime.datetime.now() - datetime.timedelta(seconds=SESSION_LIFETIME)).isoformat()
        ))['Items']
    ]

    logger.info('%d items gonna be cleared.', len(id_list))

    with table.batch_writer() as batch:
        for item_id in id_list:
            batch.delete_item({'id': item_id})

    logger.info('%d items were cleared.', len(id_list))
