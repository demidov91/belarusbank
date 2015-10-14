from flask import Flask, jsonify

from settings import EXTREMELY_SIMPLE_KEY, DEBUG
import utils
import bcse

app = Flask(__name__)

@app.route('/balance/' + EXTREMELY_SIMPLE_KEY + '/')
def balance():
    return jsonify({'cards':  list(utils.get_cards_balance())})


@app.route('/bcse/')
def  get_bcse():
    return jsonify(bcse.get_data())


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.debug = DEBUG


