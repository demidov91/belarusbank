import json
import logging
import os
import re
from typing import Iterable, Optional, Tuple

from lxml import html
from requests import Session

from constants import BB_HOST
from settings import BASE_DIR

logger = logging.getLogger(__name__)


def get_key(number: str) -> str:
    with open(os.path.join(BASE_DIR, 'keys.json'), 'r+') as f:
        return json.load(f).get(number)


def log_in(username: str, password: str) -> Optional[Tuple[Session, str]]:
    s = Session()
    response = s.get(BB_HOST + '/wps/portal/ibank/')
    if response.status_code >= 400:
        logger.debug(response.status_code)
        return None
    doc = html.fromstring(response.text.encode('utf-8'))

    action = doc.cssselect('form.loginForm')[0].get('action')
    login_step_one_response = s.post(BB_HOST + action, data={
        'bbIbUseridField': username,
        'bbIbPasswordField': password,
        'bbIbLoginAction': 'in-action',
    })
    logger.debug(login_step_one_response)
    if login_step_one_response.status_code >= 400:
        return None
    doc = html.fromstring(login_step_one_response.text.encode('utf-8'))
    action = doc.cssselect('form[name=LoginForm1]')[0].get('action')
    key_number = re.compile('.*?(\d+)').match(doc.cssselect('input[name=bbIbCodevalueField]')[0].get('placeholder')).group(1)
    logger.debug(key_number)
    login_step_two_request = {
        'cancelindicator': 'false',
        'bbIbLoginAction': 'in-action',
        'bbIbCodevalueField': get_key(key_number),
    }
    for field in ('field_1', 'field_2', 'field_3', 'field_4', 'field_5'):
        login_step_two_request[field] = doc.cssselect('form input[name={}]'.format(field))[0].get('value')
    login_step_two_response = s.post(BB_HOST + action, data=login_step_two_request)
    logger.debug('Login, step 2 response code is {}'.format(login_step_two_response.status_code))
    if login_step_two_response.status_code >= 400:
        return None

    return s, login_step_two_response.text.encode('utf-8')


def from_index_to_cards(s, index_page) -> Optional[Tuple[Session, str]]:
    doc = html.fromstring(index_page)
    cards_page_url = doc.cssselect('#top_link_1 a')[0].get('href')
    cards_page_response = s.get(BB_HOST + cards_page_url)
    logger.debug('Cards page response status is {}'.format(cards_page_response.status_code))
    if cards_page_response.status_code >= 400:
        return None

    return s, cards_page_response.text.encode('utf-8')


def parse_for_cards_balance(cards_page) -> Iterable[dict]:
    doc = html.fromstring(cards_page)
    card_accounts = doc.cssselect('.wpsPortletBody .cc_container table.accountTable>tbody>tr')
    for account in card_accounts:
        try:
            balance_element = account.cssselect('.tdBalance>.cellLable>nobr')[0]
            yield {
                'card': account.cssselect('.tdAccountText>.cellLable')[0].text.replace('\n', ''),
                'balance': balance_element.text.replace('\n', ''),
                'currency': balance_element.tail.replace('\n', ''),
            }
        except KeyError:
            logger.exception('Fail')


def get_bb_cards_balance(username: str, password: str) -> Optional[Iterable[dict]]:
    """
    Makes, actually, all the application work.
    """
    session_and_content = log_in(username, password)
    if session_and_content is None:
        return None

    session_and_content = from_index_to_cards(*session_and_content)
    if session_and_content is None:
        return None

    return parse_for_cards_balance(session_and_content[1])
