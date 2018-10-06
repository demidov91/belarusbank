import json
import pytest

from tests_integration.constants import BASE_URL, BELARUSBANK_URL, BCSE_URL, MTBANK_URL
from urllib.request import urlopen


def test_bcse():
    data = json.loads(urlopen(BASE_URL + BCSE_URL).read().decode())

    assert set(data.keys()) == {'USD', 'EUR', 'RUB'}


@pytest.mark.parametrize('url', (
    f'{BASE_URL}{MTBANK_URL}',
    f'{BASE_URL}{MTBANK_URL}/',
))
def test_mtbank__no_cookie(url):
    with urlopen(url) as response:
        assert response.geturl() == f'{BASE_URL}/auth?next=/mtb&reason=no-password'


@pytest.mark.parametrize('url', (
    f'{BASE_URL}{BELARUSBANK_URL}',
    f'{BASE_URL}{BELARUSBANK_URL}/',
))
def test_belarusbank__no_cookie(url):
    with urlopen(url) as response:
        assert response.geturl() == f'{BASE_URL}/auth?next=/bb&reason=no-password'
