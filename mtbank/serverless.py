import logging

from mtbank import utils as mtbank_utils
from passwords.utils import get_cedentials_by_cookie_data
from serverless_utils import redirect_to_auth, json_response, renewable_session


logger = logging.getLogger(__name__)


@renewable_session(provider='mtb')
def overview(event, context):
    credentials = get_cedentials_by_cookie_data(event.get('cookie'))
    if credentials is None:
        return redirect_to_auth(service='mtb', reason='no-password')

    return json_response(mtbank_utils.overview(*credentials))
