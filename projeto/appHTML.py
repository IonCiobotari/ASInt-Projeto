from flask import Flask
from flask import render_template
from flask import request
import requests

app = Flask(__name__)

APIurl = "http://127.0.0.1:6000/API/"

@app.route('/')
def main_page():
    return render_template("mainPage.html")

@app.route('/canteen')
def canteen():
    return render_template("canteen.html")

@app.route('/canteen_week')
def canteen_week():
    try:
        r = requests.get(APIurl+"canteen")
        return render_template("canteen_week.html", keys = r.json())
    except requests.exceptions.ConnectionError:
        r = "ConnectionError"
        return render_template("error_manager.html")

@app.route('/canteen_day')
def canteen_day():
    pass

#@app.errorhandler(404)
#def error_not_found():
   # return render_template("error_not_found.html")

if __name__ == '__main__':
    app.run(debug = True, port=6100)