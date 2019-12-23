# utilizar POST, PUT, GET
# guardar informação numa base de dados (pickle)

# secretarias
#   local
#   nome
#   horario
#   descriçao

# todo
# /secretariado
# /secretariado/<id>

# app port = 5100

# utilizar GET

# considerar implementar uma cache


from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import requests
import pickle
import logging.config
import log
import os

app = Flask(__name__)
URL_log = "http://127.0.0.1:4000/log"
app.logger = logging.getLogger('defaultLogger')
DB = []

def saveDB(DB):
    try:
        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        rel_path = "Pickles/servicesDB.pickle"
        abs_file_path = os.path.join(script_dir, rel_path)
        pickling = open(abs_file_path, "wb+")
        pickle.dump(DB, pickling)
        pickling.close()
    except FileNotFoundError:
        print("ERROR: could not open file")

@app.route('/services', methods = ['GET', 'POST'])
def services():
    r = requests.post(url=URL_log, json={
        'text': 'secretariadoPY  Processing services request from remote {} with method = {}'.format(request.remote_addr,request.method)})

    if request.method == 'GET':
        if DB == []:
            return jsonify("No services available")
        else:
            return jsonify(DB)
    elif request.method == 'POST':
        service = {
            'ID': len(DB),
            'location': request.json['location'],
            'name': request.json['name'],
            'hours':request.json['hours'],
            'description':request.json.get('description', "")
        }
        DB.append(service)
        # insert new service in DB
        saveDB(DB)

        return jsonify(DB[-1])

@app.route('/services/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def service_id(id):
    requests.post(url=URL_log, json={
        'text': 'secretariadoPY  Processing services request with ID = {} from remote {} with method = {}'.format(id,request.remote_addr,request.method)})

    if request.method == 'GET':
        if DB == []:
            return jsonify("No services available")
    elif request.method == 'PUT':
        print(request.json)
        if 'location' in request.json and request.json['location'] != "":
            DB[id]['location'] = request.json['location']
        if 'name' in request.json and request.json['name'] != "":
            DB[id]['name'] = request.json['name']
        if 'hours' in request.json and request.json['hours'] != "":
            DB[id]['hours'] = request.json['hours']
        if 'description' in request.json and request.json['description'] != "":
            DB[id]['description'] = request.json['description']
        saveDB(DB)
    elif request.method == 'DELETE':
        del DB[id]
        for i in range(len(DB)):
            DB[i]['ID'] = i
        saveDB(DB)

    try:
        r = DB[id]
    except IndexError:
        r = "Service not found"

    return jsonify(r)



if __name__ == "__main__":
    try:
        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        rel_path = "Pickles/servicesDB.pickle"
        abs_file_path = os.path.join(script_dir, rel_path)
        pickling = open(abs_file_path, "rb+")
        DB = pickle.load(pickling)
        pickling.close()
    except FileNotFoundError:
        DB = []
    except EOFError:
        DB = []

    app.run(debug=True, port=5100)
