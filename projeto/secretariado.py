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
    if request.method == 'GET':
        app.logger.info('GET request on default services handler')
        if DB == []:
            return jsonify("No services available")
        else:
            return jsonify(DB)
    elif request.method == 'POST':
        app.logger.info('POST request on default services handler')
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

@app.route('/services/<int:id>', methods = ['GET', 'PUT'])
def service_id(id):
    if request.method == 'GET':
        app.logger.info('GET request on service handler for ID {}'.format(id))
        if DB == []:
            return jsonify("No services available")
    elif request.method == 'PUT':
        app.logger.info('PUT request on service handler for ID {}'.format(id))
        if 'location' in request.json:
            DB[id]['location'] = request.json['location']
        if 'name' in request.json:
            print("name")
            DB[id]['name'] = request.json['name']
        if 'hours' in request.json:
            DB[id]['hours'] = request.json['hours']
        if 'description' in request.json:
            DB[id]['description'] = request.json['description']
        print(DB[id])
        print(request.json)
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
