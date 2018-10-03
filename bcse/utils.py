import datetime
import json
from urllib.request import urlopen, Request

from xml.etree import ElementTree as ET


def get_remote_data():
    url = 'http://www.bcse.by/ru/currencymarket/ratesinformertab?mode=ContinuousDoubleAuction&tstamp={}'.format(
        int(datetime.datetime.now().timestamp() * 1000)
    )
    request = Request(url)
    request.add_header('X-Requested-With', 'XMLHttpRequest')
    return urlopen(request).read().decode('utf-8').strip()


def get_data():
    data = get_remote_data().replace('rate-chart-btn', '')
    doc = ET.fromstring(data)
    trs = doc.findall('tbody/tr')
    rates = {}
    for tr in trs:
        currency = tr[0][0].text[:tr[0][0].text.index('/')].strip()
        time = tr[0][1].tail.strip()
        rate = tr[1].text.strip()
        diff = tr[2][1][0].text.strip()
        diff = diff[0] + diff[1:].strip()
        rates[currency] = '{} ({}) ({})'.format(rate, diff, time)
    return rates


def sls_get_data(event, context):
    return {
        'isBase64Encoded': False,
        "statusCode": 200,
        "headers": {},
        'body': json.dumps(get_data()),
    }
