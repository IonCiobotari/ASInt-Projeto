from flask import Flask
from flask import jsonify
import requests

app = Flask(__name__)

URL_canteen = "http://127.0.0.1:5000/"
URL_rooms = "http://127.0.0.1:6000/"
URL_services = "http://127.0.0.1:7000/"

URL = {'canteen':URL_canteen, 'rooms':URL_rooms, 'services':URL_services}


#@app.route('/API/canteen')
def show_canteen():
    try:
        r = requests.get(URL_canteen)
    except requests.exceptions.InvalidURL:
        return jsonify("Microservice is down")
    # transform data?
    return r.json()

#@app.route('/API/canteen/<date>')
def show_canteen_day(date):
    try:
        r = requests.get(URL_canteen+"/"+date)
    except requests.exceptions.InvalidURL:
        return jsonify("Microservice is down")
    # transform data?
    return r.json()

#@app.route('/API/rooms')
def show_salas():
    try:
        r = requests.get(URL_rooms)
    except requests.exceptions.InvalidURL:
        return jsonify("Microservice is down")
    # transform data?
    return r.json()

#@app.route('/API/rooms/<id>')
def show_salas_id(id):
    try:
        r = requests.get(URL_rooms+"/"+id)
    except requests.exceptions.InvalidURL:
        return jsonify("Microservice is down")
    # transform data?
    return r.json()

#@app.route('/API/rooms/<id>/<date>')
def show_salas_id_day(id, date):
    try:
        r = requests.get(URL_rooms+"/"+"id"+"/"+date)
    except requests.exceptions.InvalidURL:
        return jsonify("Microservice is down")
    # transform data?
    return r.json()

#@app.route('/API/services')
def show_secretariado():
    try:
        r = requests.get(URL_services)
    except requests.exceptions.InvalidURL:
        return jsonify("Microservice is down")
    # transform data?
    return r.json()

#@app.route('/API/services/<id>')
def show_secretariado_id(id):
    try:
        r = requests.get(URL_services+"/"+id)
    except requests.exceptions.InvalidURL:
        return jsonify("Microservice is down")
    # transform data?
    return r.json()


@app.route('/API/<path:path>')
def show_path_result(path):
    
    args = path.split("/")
    r_url = URL[args[0]] + path

    # decode path

    try:
        r = requests.get(r_url)
        return r.json()
    except requests.exceptions.InvalidURL:
        return jsonify("Invalid URL")

if __name__ == "__main__":
    app.run(debug=True)