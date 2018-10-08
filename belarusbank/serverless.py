from belarusbank import utils as bb_utils

from passwords.utils import get_cedentials_by_cookie_data
from serverless_utils import json_response, redirect_to_auth, renewable_session


@renewable_session(provider='bb')
def overview(event, context):
    credentials = get_cedentials_by_cookie_data(event.get('cookie'))
    if credentials is None:
        return redirect_to_auth(service='bb', reason='no-password')

    return json_response({
        'cards': tuple(bb_utils.get_bb_cards_balance(*credentials)),
    })
