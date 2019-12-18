from flask import Flask
from flask import render_template
from flask import request
from flask import Markup
from json2html import *
import requests
import log
import logging.config

app = Flask(__name__)
app.logger = logging.getLogger('defaultLogger')
DB = {}
APIurl = "http://127.0.0.1:6000/API/"

# general html page
@app.route('/<path:path>')
def default_page(path):
    url = APIurl + path
    r = requests.get(url)
    data = json2html.convert(json = r.json())

    return render_template("default.html", result = data)


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
