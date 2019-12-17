from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import requests
import datetime
import logging.config
import log


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

    print(CACHE)


@app.route('/canteen') # Returns lunch and dinner for the current week
def canteen_week():
    global CACHE

    print(request.remote_addr)


    today = datetime.datetime.today().strftime('%d/%m/20%y')
    print(today)
    if today not in CACHE.keys():
        print("not in cache")
        try:
            r = requests.get(FENIX_CANTEEN_URL)
            save_CACHE(r.json())
            data = CACHE
            app.logger.info('{} - Uncached Request on Default canteen handler'.format(request.remote_addr))
        except requests.exceptions.InvalidURL:
            app.logger.info('{} - Invalid URL on default Canteen request'.format(request.remote_addr))
            data = r.status_code
    else:
        data = CACHE
        app.logger.info('{} - Cached request on Canteen default handler'.format(request.remote_addr))
    return jsonify(data)

@app.route('/canteen/<day>') # return lunch and dinner for a given day
def canteen_day(day):
    global CACHE

    day = day.replace("-", "/") # day must come with dd-mm-yyyy format
    if day in CACHE:
        data = CACHE[day]
        app.logger.info('{} - Cached request on Canteen Day handler for day: {}'.format(request.remote_addr, day))
    else:
        try:
            r = requests.get(FENIX_CANTEEN_URL + "?day="+day)
            data = 404
            for i in r.json():
                if day in i.values():
                    data = {i['day']: i['meal']}
                    break
            app.logger.info('{} - Uncached request on Canteen Day handler for day: {}'.format(request.remote_addr, day))
        except requests.exceptions.InvalidURL:
            app.logger.info('{} - Invalid URL on Canteen Day handler for day: {}'.format(request.remote_addr, day))
            data = r.status_code    #changed to status_code

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
