# utilizar GET

# considerar implementar uma cache

# /salas
# /salas/<id>
# /salas/<id>/<day>


# app port = 5200

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import redirect
import log
import requests
import logging.config

app = Flask(__name__)

URL_log = "http://127.0.0.1:4000/log"

@app.route('/rooms')
# menu da semana
def salas_list():
    try:
        r = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces")
    except requests.exceptions.InvalidURL:
        return jsonify("Fenix service is down")
    requests.post(url=URL_log, json={
        'text': 'salasPY  Processing salas request from remote {}'.format(request.remote_addr)})

    return jsonify(r.json())


# dia tem de estar em dd-mm-yyyy
@app.route('/rooms/<ID>')
def salas_ID(ID):
    try:
        r = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/" + ID)
    except requests.exceptions.InvalidURL:
        return jsonify("Fenix service is down")
    requests.post(url=URL_log, json={
        'text': 'salasPY  Processing salas request with ID = {} from remote {}'.format(ID,request.remote_addr)})

    return jsonify(r.json())


# dia tem de estar em dd-mm-yyyy
@app.route('/rooms/<ID>/<day>')
def salas_dayID(ID, day):
    day = day.replace("-", "/")
    try:
        r = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/" + ID + '?day=' + day)
    except requests.exceptions.InvalidURL:
        return jsonify("Fenix service is down")
    data = r.json()
    if 'events' in data.keys():
        vect = []
        for event in data['events']:
            if event['day'] == day:
                vect.append(event)
        data['events'] = vect
    else:
        return redirect('/rooms/{}'.format(ID))

    requests.post(url=URL_log, json={
        'text': 'salasPY  Processing salas request with ID = {} and day = {} from remote {}'.format( ID, day,request.remote_addr)})

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5200)
