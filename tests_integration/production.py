import json

from tests_integration.constants import BASE_URL, BCSE_URL, MTBANK_URL
from urllib.request import urlopen


def test_bcse():
    data = json.loads(urlopen(BASE_URL + BCSE_URL).read().decode())

    assert set(data.keys()) == {'USD', 'EUR', 'RUB'}


def test_mtbank__no_cookie():
    with urlopen(BASE_URL + MTBANK_URL) as response:
        assert response.geturl() == BASE_URL + '/auth?next=mtb&reason=no-password'


def test_mtbank__railing_slash():
    with urlopen(BASE_URL + MTBANK_URL + '/') as response:
        assert response.geturl() == BASE_URL + '/auth?next=mtb&reason=no-password'
