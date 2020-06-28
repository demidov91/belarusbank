import datetime
import ssl
from urllib.request import urlopen, Request
from xml.etree import ElementTree as ET

from serverless_utils import json_response


def get_remote_data():
    url = 'https://www.bcse.by/ru/currencymarket/ratesinformertab?mode=ContinuousDoubleAuction&tstamp={}'.format(
        int(datetime.datetime.now().timestamp() * 1000)
    )
    request = Request(url)
    request.add_header('X-Requested-With', 'XMLHttpRequest')
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return urlopen(request, timeout=20, context=ctx).read().decode('utf-8').strip()


def get_data():
    data = get_remote_data().replace('rate-chart-btn', '')
    doc = ET.fromstring(data)
    trs = doc.findall('tbody/tr')
    rates = {}
    for tr in trs:
        currency = tr[0][0].text[:tr[0][0].text.index('/')].strip()
        time = tr[0][1].tail.strip()
        rate = tr[1].text.strip()
        if len(tr[2]) > 1:
            diff = tr[2][1][0].text.strip()
            diff = diff[0] + diff[1:].strip()
        else:
            diff = tr[2][0].text.strip()
        rates[currency] = '{} ({}) ({})'.format(rate, diff, time)
    return rates


def serverless_get_data(event, context):
    return json_response(get_data())
