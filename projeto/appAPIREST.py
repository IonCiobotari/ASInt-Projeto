from flask import Flask
from flask import jsonify
from flask import request
import requests

app = Flask(__name__)

URL_canteen = "http://127.0.0.1:5000/"
URL_rooms = "http://127.0.0.1:5200/"
URL_services = "http://127.0.0.1:5100/"

URL = {'canteen':URL_canteen, 'rooms':URL_rooms, 'services':URL_services}

@app.route('/API/<path:path>', methods = ['GET', 'PUT', 'POST', 'DELETE'])
def show_path_result(path):

    url_args = path.split("/")

    if url_args[0] in URL:
        # decode path
        r_url = URL[url_args[0]] + path
        try:
            if request.method == 'GET':
                r = requests.get(r_url)
                data = r.json()
            elif request.method == 'PUT':
                data = request.json
                r = requests.put(url = r_url, json = data)
                data = r.status_code
            elif request.method == 'POST':
                data = request.json
                r = requests.post(url = r_url, json = data)
                data = r.status_code
            elif request.method == 'DELETE':
                r = requests.delete(r_url)
                data = r.status_code
        except requests.exceptions.InvalidURL:
            data = "Invalid url"
        except requests.exceptions.ConnectionError:
            data = "Connection error with "+path
    else:
        data = "Invalid url"

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=6000)