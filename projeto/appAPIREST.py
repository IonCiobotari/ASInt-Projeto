from flask import Flask
from flask import jsonify
import requests

app = Flask(__name__)

URL_canteen = "http://127.0.0.1:5000/canteen"
URL_rooms = "http://127.0.0.1:6000/rooms"
URL_services = "http://127.0.0.1:5100/services"

URL = {'canteen':URL_canteen, 'rooms':URL_rooms, 'services':URL_services}

@app.route('/API/<serv>/<path:path>')
def show_path_result(serv, path):
    print(serv)
    print(path)
    if serv in URL:
        if path != "":
            path = "/"+path
        r_url = URL[serv] + path
        print(r_url)
        # decode path
        try:
            r = requests.get(r_url)
            print(r.json())
            return r.json()
        except requests.exceptions.InvalidURL:
            return jsonify("Invalid URL")
    else:
        return jsonify("Invalid url")

if __name__ == "__main__":
    app.run(debug=True, port=6000)