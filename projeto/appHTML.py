from flask import Flask
from flask import render_template
from flask import request
import requests

app = Flask(__name__)

APIurl = "http://127.0.0.1:6000/API/"

# main menu
@app.route('/')
def main_page():
    return render_template("mainPage.html")

####################################################################
# canteen microservice
####################################################################

# canteen main menu
@app.route('/canteen')
def canteen():
    return render_template("canteen.html")

# show canteen information for the current week
@app.route('/canteen_week')
def canteen_week():
    try:
        r = requests.get(APIurl+"canteen")
        return render_template("canteen_week.html", result = r.json())
    except requests.exceptions.ConnectionError:
        r = "ConnectionError"
        return render_template("error_manager.html")

# show canteen information for a specific day
@app.route('/canteen_day')
def canteen_day():
    try:
        r = requests.get(APIurl+"canteen/"+request.args['date'])
        return render_template("canteen_day.html", result = r.json())
    except requests.exceptions.ConnectionError:
        r = "ConnectionError"
        return render_template("error_manager.html")


####################################################################
# Services microservice
####################################################################

# show all available services with corresponding ID
@app.route('/services')
def services():
    try:
        r = requests.get(APIurl+"services")
        return render_template("services.html", result = r.json())
    except requests.exceptions.ConnectionError:
        r = "ConnectionError"
        return render_template("error_manager.html")

# show all information for a scpecific service
@app.route('/services_id')
def service_ID():
    try:
        r = requests.get(APIurl+"services/"+request.args['ID'])
        return render_template("services_ID.html", result = r.json())
    except requests.exceptions.ConnectionError:
        r = "ConnectionError"
        return render_template("error_manager.html")

####################################################################
# Rooms microservice
####################################################################

@app.route('/rooms')
def rooms():
    return render_template("mainPage.html")

#@app.errorhandler(404)
#def error_not_found():
   # return render_template("error_not_found.html")

if __name__ == '__main__':
    app.run(debug = True, port=6100)