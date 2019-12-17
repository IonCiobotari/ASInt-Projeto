from flask import Flask
from flask import jsonify
import requests

app = Flask(__name__)

URL_canteen = "http://127.0.0.1:5000/"
URL_rooms = "http://127.0.0.1:5200/"
URL_services = "http://127.0.0.1:5100/"

URL = {'canteen':URL_canteen, 'rooms':URL_rooms, 'services':URL_services}

@app.route('/API/<path:path>')
def show_path_result(path):

    url_args = path.split("/")

    if url_args[0] in URL:
        # decode path
        r_url = URL[url_args[0]] + path
        print(r_url)
        try:
            r = requests.get(r_url)
           # print(r.json())
            data = r.json()
        except requests.exceptions.InvalidURL:
            data = "Invalid url"
    else:
        data = "Invalid url"

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=6000)