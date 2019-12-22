from flask import Flask
from flask import render_template
from flask import request
from flask import Markup
from flask import redirect
from flask import session
from flask import url_for
from json2html import *
import json
import requests
#import log
import logging.config
import os
import pickle

app = Flask(__name__)
app.config["SECRET_KEY"] = 'OgyJj3f-Rp4pNckcw2Ztjw'
#app.logger = logging.getLogger('defaultLogger')

users = {'master': {'username' : "master", 'password':"password"}, 
         'admin1': {'username' : "admin1", 'password':"password1"}}

APIurl = "http://127.0.0.1:6000/API/"

@app.route('/<path:path>')
def default_page(path):
    url = APIurl + path

    try:
        r = requests.get(url)
        data = json2html.convert(json = r.json())
        if data == "":
            data = "No informaiton available"
    except requests.exceptions.ConnectionError:
        data = '<h2>Connection error with proxy</h2>'
        return render_template("default.html", result = Markup(data))

    return render_template("default.html", result=Markup(data))


# general html page
@app.route('/Admin/<path:path>', methods = ['GET', 'PUT', 'POST', 'DELETE'])
def admin_page(path):
    url = APIurl + path
    path = path.split("/")
    if path[0] == "Admin":
        del path[0]

    try:
        r = requests.get(url)
        data = json2html.convert(json = r.json())
        if data == "":
            data = "No informaiton available"
    except requests.exceptions.ConnectionError:
        data = '<h2>Connection error with proxy</h2>'
        return render_template("default.html", result = Markup(data))

    if not session.get("USERNAME") is None: # only admin are allowed to use post, put and delete methods
        if request.method == 'POST':
            r = requests.post(url = url, json = request.form)
        elif request.method == 'GET':
            if request.args != {}:
                if request.args['operation'] == 'PUT':
                    result = request.args
                    r = requests.put(url = url, json = result)
                    return redirect("http://127.0.0.1:6100/services/{}".format(path[-1]))
                elif request.args['operation'] == 'DELETE':
                    r = requests.delete(url)
                    url = APIurl + path[0]
                    return redirect("http://127.0.0.1:6100/services")
        
        if path[0] == "services":
            if len(path) == 1: # /services
                data += '<h3>Create new service</h3><form action="/services" method="POST"><p>Name: <input type="text" name="name"></p><p>Location: <input type="text" name="location"></p><p>Hours: <input type="text" name="hours"></p><p>Description: <input type="text" name="description"></p><input type = "submit"></form>'
            else: # /services/<id>
                data += '<h3>Update service</h3>'
                data += '<form action="/services/{}" method="GET">'.format(path[-1])
                data += '<p>Name: <input type="text" name="name"/></p>'
                data += '<p>Location: <input type="text" name="location"/></p>'
                data += '<p>Hours: <input type="text" name="hours"/></p>'
                data += '<p>Description: <input type="text" name="description"/></p>'
                data += '<p><input type="hidden" name="operation" value="PUT"/></p>'
                data += '<input type = "Submit"/>'
                data += '</form>'
                data += '<h3>Delete service</h3><form action="/services/{}" method="GET"><input type = "hidden" name = "operation" value="DELETE"><input type = "submit"></form>'.format(path[-1])
        data+= '<form action="/logoutAdmin"><input type="submit" value="Logout"/></form>'
    else:
        data += '<form action="/loginAdmin"><input type="submit" value="Login"/></form>'
        
    return render_template("default.html", result = Markup(data))


@app.route('/')
def mainpage():
    return render_template("mainPage.html")


@app.route('/loginAdmin', methods=['GET','Post'])
def loginAdmin():
    data = ""
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username in users:
            if users[username]["password"] == password:
                session["USERNAME"] = username
                data = '<h2>Login successful</h2>'
                data += '<a href="/logoutAdmin">Logout</a>'
                return render_template("default.html", result = Markup(data))
            else:
                data = "<h2>Invalid password</h2>"
        else:
            data = "<h2>Invalid username</h2>"

    return render_template("login.html", result = Markup(data))

@app.route('/logoutAdmin')
def logoutAdmin():
    session.pop("USERNAME", None)

    return redirect(url_for('loginAdmin'))


@app.route('/QRcode')
def QRcode():
    return render_template("qrcode.html")


@app.errorhandler(404)
def error_not_found(error):
    message = '<h2>Page not found</h2>'
    return render_template("default.html", result = Markup(message)), 404


if __name__ == '__main__':
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