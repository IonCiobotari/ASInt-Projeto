from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import requests
import datetime
import log
import logging.config


app = Flask(__name__)

URL_log = "http://127.0.0.1:4000/log"

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

    today = datetime.datetime.today().strftime('%d/%m/20%y')
    if today not in CACHE.keys():
        try:
            r = requests.get(FENIX_CANTEEN_URL)
            save_CACHE(r.json())
            data = CACHE
            requests.post(url=URL_log, json={
                'text': 'cantinaPY Uncached Request on Default canteen handler from remote {}'.format(request.remote_addr)})

        except requests.exceptions.InvalidURL:

            data = r.status_code
    else:
        data = CACHE
        requests.post(url=URL_log, json={
            'text': 'cantinaPY cached Request on Default canteen handler from remote {}'.format(request.remote_addr)})
    return jsonify(data)

@app.route('/canteen/<day>') # return lunch and dinner for a given day
def canteen_day(day):
    global CACHE

    day = day.replace("-", "/") # day must come with dd-mm-yyyy format
    if day in CACHE.keys():
        data = CACHE[day]
        requests.post(url=URL_log, json={
            'text': 'cantinaPY cached Request on Default canteen handler from remote {} for day {}'.format(request.remote_addr,day)})
    else:
        try:
            r = requests.get(FENIX_CANTEEN_URL + "?day="+day)
            if r.status_code != 200:
                data = r.status_code
            else:
                for i in r.json():
                    if day in i.values():
                        data = {i['day']: i['meal']}
                        break
            requests.post(url=URL_log, json={
                'text': 'cantinaPY uncached Request on Default canteen handler from remote {} for day {}'.format(
                    request.remote_addr, day)})
        except requests.exceptions.InvalidURL:
            data = r.status_code    #changed to status_code

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
