from functools import wraps
from flask import Flask, jsonify

from settings import EXTREMELY_SIMPLE_KEY, DEBUG
import utils
import bcse
from mtbank.utils import overview as mtb_overview

app = Flask(__name__)


def add_utf_encoding(wrapped):
    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        response = wrapped(*args, **kwargs)
        response.headers['Content-Type'] += '; charset=utf-8'
        return response
    return wrapper

@app.route('/balance/' + EXTREMELY_SIMPLE_KEY + '/bb/')
def bb_balance():
    return jsonify({'cards':  list(utils.get_bb_cards_balance())})


@app.route('/balance/' + EXTREMELY_SIMPLE_KEY + '/mtb/')
#@add_utf_encoding
def mtb_balance():
    return jsonify(mtb_overview())


@app.route('/bcse/')
def get_bcse():
    return jsonify(bcse.get_data())


if __name__ == '__main__':
    app.debug = DEBUG
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'
    app.run(host='0.0.0.0')



