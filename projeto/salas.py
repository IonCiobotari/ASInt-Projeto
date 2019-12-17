# utilizar GET

# considerar implementar uma cache

# /salas
# /salas/<id>
# /salas/<id>/<day>


# app port = 6000

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import log
import requests
import logging.config


app = Flask(__name__)

app.logger = logging.getLogger('defaultLogger')
#@app.route('/')
#def main():

@app.route('/salas')
# menu da semana
def salas_list():
    try:
        r = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces")
    except requests.exceptions.InvalidURL:
        return jsonify("Fenix service is down")
    print(r.status_code)
    data = r.json()
    print(data)
    app.logger.info('Processing default salas request')
    return jsonify(str(r.json()))



#dia tem de estar em dd-mm-yyyy
@app.route('/salas/<ID>')
def salas_ID(ID):
    print(ID)
    try:
        r = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"+ID)
    except requests.exceptions.InvalidURL:
        return jsonify("Fenix service is down")
    print(r.status_code)
    data = r.json()
    print(data)
    app.logger.info('Processing salas request with ID = {}'.format(ID))
    return jsonify(str(r.json()))

#dia tem de estar em dd-mm-yyyy
@app.route('/salas/<ID>/<day>')
def salas_dayID(ID,day):
    day = day.replace("-", "/")
    print(day)
    try:
        r = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"+ID+'?day='+day)
    except requests.exceptions.InvalidURL:
        return jsonify("Fenix service is down")
    print(r.status_code)
    data = r.json()
    print(data)
    app.logger.info('Processing salas request with ID = {} and day = {}'.format(ID,day))
    return jsonify(str(r.json()))#TODO return only ocupation for the currrent day and not for the current week like fenix API returns
if __name__ == "__main__":
    app.run(debug=True, port=5000)
