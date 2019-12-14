from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import requests
import datetime

app = Flask(__name__)

FENIX_CANTEEN_URL = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen"
CACHE = {}

# save new cache information
def save_CACHE(data):
    global CACHE

    CACHE = {}
    for i in data:
        CACHE[i['day']] = i['meal']


@app.route('/canteen') # Returns lunch and dinner for the current week
def canteen_week():
    global CACHE

    today = datetime.datetime.today().strftime('%d/%m/%y')
    if today not in CACHE.keys():
        try:
            r = requests.get(FENIX_CANTEEN_URL)
            save_CACHE(r.json())
        except requests.exceptions.InvalidURL:
            pass
    
    if r.status_code != 200:
        data = r.status_code
    else:
        data = CACHE

    return jsonify(data)

@app.route('/canteen/<day>') # return lunch and dinner for a given day
def canteen_day(day):
    global CACHE
    
    day = day.replace("-", "/") # day must come with dd-mm-yyyy format
    if day in CACHE:
        data = CACHE[day]
    else:
        try:
            r = requests.get(FENIX_CANTEEN_URL + "?day="+day)
            data = 404
            for i in r.json():
                if day in i.values():
                    data = {i['day']: i['meal']}
                    break
        except requests.exceptions.InvalidURL:
            data = r.status_code

    return jsonify(data)

#@app.route('/canteen/lunch') # return lunch for the current week


#@app.route('/<path:path>')
#def decode_path(path):



if __name__ == "__main__":
    app.run(debug=True, port=5000)

