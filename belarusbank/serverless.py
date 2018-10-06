from belarusbank import utils as bb_utils

from serverless_utils import json_response


def overview(event, context):
    return json_response({
        'cards': tuple(bb_utils.get_bb_cards_balance()),
    })