from flask import Flask
from flask import render_template
from flask import request
from flask import Markup
from json2html import *
import requests

app = Flask(__name__)

APIurl = "http://127.0.0.1:6000/API/"

# main menu
@app.route('/')
def main_page():
    return render_template("mainPage.html")


def decode_path(path):
    #path = path.split("/")
    try:
        r = requests.get(APIurl + path)
    except requests.exceptions.InvalidURL:
        return "Invalid URL"

    return json2html.convert(json = r.json())


@app.route('/<path:path>')
def get_general_page(path):
    result = decode_path(path)

    print(request.remote_addr)

    return render_template("default.html", result = Markup(result))

if __name__ == '__main__':
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