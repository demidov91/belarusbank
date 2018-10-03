import json
import logging

import requests
from lxml import html

from constants import MTB_HOST
from passwords.utils import get_credentials

logger = logging.getLogger(__name__)


def overview(username, password):
    client = requests.session()
    resp = client.post(MTB_HOST + '/ib/site/login', data={
        'name': username,
        'password': password,
    })
    logger.debug('Login status {}'.format(resp.status_code))
    if resp.status_code != 200:
        logger.error(resp.text)
        return None
    resp = client.get(MTB_HOST + '/ib/site/dashboard/v2')
    logger.debug('Dashboard status {}'.format(resp.status_code))
    if resp.status_code != 200:
        logger.error(resp.text)
        return None
    cards = []
    depo = []
    for product in html.fromstring(resp.content).cssselect('.bank-product'):
        parsed_product = {
            'name': product.cssselect('.product-title>a')[0].text,
            'balance': product.cssselect('.balance-table .summ.balance')[0].text,
            'currency': product.cssselect('.balance-table .currency')[0].text,
        }
        if product.cssselect('.cards-parent'):
            cards.append(parsed_product)
        else:
            depo.append(parsed_product)
    return {
        'cards': cards,
        'depo': depo,
    }


def _redirect_to_auth(*, next: str, reason: str):
    return {
        'statusCode': 302,
        'headers': {
            'Location': f'auth?next={next}&reason={reason}',
        },
        'body': '',
    }


def serverless_overview(event, context):
    if 'headers' not in event or 'Cookie' not in event['headers']:
        logger.info('No cookie')
        return _redirect_to_auth(next='mtb', reason='no-password')

    cookie = dict(
        x.split('=')
        for x in (
            one_cookie.strip()
            for one_cookie in event['headers']['Cookie'].split(';')
            if '=' in one_cookie
        )
    )

    if 'sessionId' not in cookie or 'encryptKey' not in cookie:
        logger.info('No session')
        return _redirect_to_auth(next='mtb', reason='no-password')

    username, password = get_credentials(cookie['sessionId'], cookie['encryptKey'])

    return {
        'statusCode': 200,
        'body': json.dumps(overview(username, password)),
    }
