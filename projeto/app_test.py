from flask import Flask
from flask import request
from flask import jsonify
import requests
import log
import requests
import logging.config


URL_LOGs = "http://127.0.0.1:4000/log"
app = Flask(__name__)

app.logger = logging.getLogger('defaultLogger')
@app.route('/testing')
def test():

    data =  {'text':'what is the answer?'}
    r = requests.post(url=URL_LOGs, json={'text':'what is the answer?'})
    return jsonify("Somebody is trying to test somethign")

if __name__ == "__main__":
    app.run(debug=True, port=10000)
