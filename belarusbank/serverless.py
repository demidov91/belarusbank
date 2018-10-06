from belarusbank import utils as bb_utils

from passwords.utils import get_cedentials_by_serveless_request
from serverless_utils import json_response, redirect_to_auth


def overview(event, context):
    credentials = get_cedentials_by_serveless_request(event)
    if credentials is None:
        return redirect_to_auth(next='/bb', reason='no-password')

    return json_response({
        'cards': tuple(bb_utils.get_bb_cards_balance(*credentials)),
    })