import logging

import requests
from lxml import html

from constants import MTB_HOST


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
