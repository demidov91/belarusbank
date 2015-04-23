from flask import Flask, jsonify

from settings import EXTREMELY_SIMPLE_KEY, DEBUG
import utils


app = Flask(__name__)

@app.route('/balance/' + EXTREMELY_SIMPLE_KEY + '/')
def balance():
    return jsonify({'cards': list(utils.get_cards_balance())})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.debug = DEBUG


