import logging
from http.cookies import SimpleCookie

from mtbank import utils as mtbank_utils
from passwords.utils import get_credentials
from serverless_utils import redirect_response_302, json_response


logger = logging.getLogger(__name__)


def _redirect_to_auth(*, next: str, reason: str):
    return redirect_response_302(f'/auth?next={next}&reason={reason}')


def overview(event, context):
    if 'headers' not in event or 'Cookie' not in event['headers']:
        logger.info('No cookie')
        return _redirect_to_auth(next='/mtb', reason='no-password')

    cookie = SimpleCookie(event['headers']['Cookie'])

    if 'sessionId' not in cookie or 'encryptKey' not in cookie:
        logger.info('No session')
        return _redirect_to_auth(next='/mtb', reason='no-password')

    username, password = get_credentials(cookie['sessionId'].value, cookie['encryptKey'].value)

    if not (username and password):
        return _redirect_to_auth(next='/mtb', reason='no-password')

    return json_response(mtbank_utils.overview(username, password))
