from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import requests
import datetime
import log
import logging.config


app = Flask(__name__)

FENIX_CANTEEN_URL = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen"
CACHE = {}
app.logger = logging.getLogger('defaultLogger')

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
            app.logger.info('Uncached Request on Default canteen handler')
        except requests.exceptions.InvalidURL:
            app.logger.info('Invalid URL on default Canteen request')
            data = r.status_code
    else:
        data = CACHE
        app.logger.info('Cached request on Canteen default handler')
    return jsonify(data)

@app.route('/canteen/<day>') # return lunch and dinner for a given day
def canteen_day(day):
    global CACHE

    day = day.replace("-", "/") # day must come with dd-mm-yyyy format
    if day in CACHE.keys():
        data = CACHE[day]
        app.logger.info('Cached request on Canteen Day handler for day: {}'.format(day))
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
                app.logger.info('Uncached request on Canteen Day handler for day: {}'.format(day))
        except requests.exceptions.InvalidURL:
            app.logger.info('Invalid URL on Canteen Day handler for day: {}'.format(day))
            data = r.status_code    #changed to status_code

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
