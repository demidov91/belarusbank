import logging

from mtbank import utils as mtbank_utils
from passwords.utils import get_cedentials_by_serveless_request
from serverless_utils import redirect_to_auth, json_response


logger = logging.getLogger(__name__)


def overview(event, context):
    credentials = get_cedentials_by_serveless_request(event)
    if credentials is None:
        return redirect_to_auth(next='/mtb', reason='no-password')

    return json_response(mtbank_utils.overview(*credentials))
