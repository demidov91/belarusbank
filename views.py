from flask import Flask, jsonify

from bcse.utils import get_data as get_bcse_data
from belarusbank.utils import get_bb_cards_balance
from mtbank.utils import overview as mtb_overview
from settings import EXTREMELY_SIMPLE_KEY, DEBUG

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'


@app.route('/balance/' + EXTREMELY_SIMPLE_KEY + '/bb/')
def bb_balance():
    return jsonify({'cards':  list(get_bb_cards_balance())})


@app.route('/balance/' + EXTREMELY_SIMPLE_KEY + '/mtb/')
def mtb_balance():
    return jsonify(mtb_overview())


@app.route('/bcse/')
def get_bcse():
    return jsonify(get_bcse_data())


if __name__ == '__main__':
    app.debug = DEBUG
    app.run(host='0.0.0.0')



