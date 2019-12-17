from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import log
import requests
import logging.config


app = Flask(__name__)

app.logger = logging.getLogger('defaultLogger')
@app.route('/testing')
def test():
    app.logger.info('Somebody tested')
    return jsonify("Somebody is trying to test somethign")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
