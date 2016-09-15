import requests
from lxml import html

from settings import MTB_USERNAME, MTB_PASSWORD, MTB_HOST

import logging
logger = logging.getLogger(__name__)


def overview():
    client = requests.session()
    resp = client.post(MTB_HOST + '/ib/site/login', data={
        'name': MTB_USERNAME,
        'password': MTB_PASSWORD,
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
    products = []
    for product in html.fromstring(resp.content).cssselect('.bank-product'):
        products.append({
            'card': product.cssselect('.product-title>a')[0].text,
            'balance': product.cssselect('.balance-table .summ.balance')[0].text,
            'currency': product.cssselect('.balance-table .currency')[0].text,
        })
    return {
        'cards': products,
    }

