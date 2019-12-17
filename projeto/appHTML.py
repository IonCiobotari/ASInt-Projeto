from flask import Flask
from flask import render_template
from flask import request
from flask import Markup
import requests
import log
import logging.config

app = Flask(__name__)
app.logger = logging.getLogger('defaultLogger')
DB = {}
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


@app.route('/serviceAdmin',methods = ['POST'])
def changeService():
    r = requests.get(APIurl+"services/")
    #TODO generate list of available IDs and put them on the page

    render_template("error_manager.html", Options = Markup(subs))


@app.errorhandler(404)
def error_not_found(error):
    return render_template("error_not_found.html"), 404



@app.route('/loginAdmin', methods=['Post'])
def loginAdmin():

    #TODO do the adming login
    return "i didnt do it to em"

if __name__ == '__main__':
    global DB
    try:
        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        rel_path = "Pickles/admins.pickle"
        abs_file_path = os.path.join(script_dir, rel_path)
        pickling = open(abs_file_path, "rb+")
        DB = pickle.load(pickling)
        pickling.close()
    except FileNotFoundError:
        DB = {}
    except EOFError:
        DB = {}

    app.run(debug = True, port=6100)

    """
    def jsontoHtml(json, h, html):
    html = ""

    if struct
        for k in json.key:
                html+="<h>"+jsontoHtml(json[k],h+1)+"</h>"

    if array
        html = " <h> "
        for v in json:
            html +=v
    if valor
        html = valor(json)

    return html
"""
