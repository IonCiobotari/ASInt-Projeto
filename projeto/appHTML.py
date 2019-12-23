from flask import Flask
from flask import render_template
from flask import request
from flask import Markup
from flask import redirect
from flask import session
from flask import url_for
from flask import jsonify
from json2html import *
import json
import requests
#import log
import logging.config
import os
import pickle
import random
import string


users = {'master': {'username' : "master", 'password':"password"}, 
         'admin1': {'username' : "admin1", 'password':"password1"}}

APIurl = "http://127.0.0.1:6000/API/"
URL_log = "http://127.0.0.1:4000/log"

client_id = "1695915081465958"
redirect_uri = "http://127.0.0.1:6100/userAuth"
client_secret = "JuVlEYUP21AHAGoXkNo5veg9pxqd4qJ9Pq81zgrjf6Mw9fMceyDIGUbroRx++8L64VDNtQ8Z8WkOSD4uqZnbDw=="
fenixLoginpage= "https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=%s&redirect_uri=%s"
fenixacesstokenpage = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'

FENIX_user = {}
USER_STACK = {}

app = Flask(__name__)
app.config["SECRET_KEY"] = 'OgyJj3f-Rp4pNckcw2Ztjw'
#app.logger = logging.getLogger('defaultLogger')



def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))



@app.route('/')
def mainpage():
    return render_template("mainPage.html")



@app.route('/<path:path>')
def default_page(path):
    url = APIurl + path
    print(url)
    requests.post(url=URL_log, json={
        'text': 'APPHTML recognized request from {}, method = {}'.format(request.remote_addr, request.method)})
    print("here")
    try:
        r = requests.get(url)
        data = json2html.convert(json = r.json())
        print(data)
        if data == "":
            data = "No informaiton available"
    except requests.exceptions.ConnectionError:
        print("except")
        data = '<h2>Connection error with proxy</h2>'
        return render_template("default.html", result = Markup(data))
    print("done")
    return render_template("default.html", result=Markup(data))


# general html page
@app.route('/Admin/<path:path>', methods = ['GET', 'PUT', 'POST', 'DELETE'])
def admin_page(path):
    url = APIurl + path
    path = path.split("/")
    if path[0] == "Admin":
        del path[0]

    requests.post(url=URL_log, json={
        'text': 'APPHTML Admin request from {}, method = {}'.format(request.remote_addr, request.method)})
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
                if 'operation' in request.args.keys():
                    if request.args['operation'] == 'PUT':
                        result = request.args
                        r = requests.put(url = url, json = result)
                        return redirect("http://127.0.0.1:6100/Admin/services/{}".format(path[-1]))
                    elif request.args['operation'] == 'DELETE':
                        r = requests.delete(url)
                        url = APIurl + path[0]
                        return redirect("http://127.0.0.1:6100/Admin/services")
        
        if path[0] == "services":
            if len(path) == 1: # /services
                data += '<h3>Create new service</h3><form action="/Admin/services" method="POST">'
                data +='<p>Name: <input type="text" name="name"></p>'
                data +='<p>Location: <input type="text" name="location"></p>'
                data +='<p>Hours: <input type="text" name="hours"></p>'
                data+='<p>Description: <input type="text" name="description"></p><input type = "submit"></form>'
            else: # /services/<id>
                data += '<h3>Update service</h3>'
                data += '<form action="/Admin/services/{}" method="GET">'.format(path[-1])
                data += '<p>Name: <input type="text" name="name"/></p>'
                data += '<p>Location: <input type="text" name="location"/></p>'
                data += '<p>Hours: <input type="text" name="hours"/></p>'
                data += '<p>Description: <input type="text" name="description"/></p>'
                data += '<p><input type="hidden" name="operation" value="PUT"/></p>'
                data += '<input type = "Submit"/>'
                data += '</form>'
                data += '<h3>Delete service</h3><form action="/Admin/services/{}" method="GET"><input type = "hidden" name = "operation" value="DELETE"><input type = "submit"></form>'.format(path[-1])
        data+= '<form action="/logoutAdmin"><input type="submit" value="Logout"/></form>'
    else:
        data += '<form action="/loginAdmin"><input type="submit" value="Login"/></form>'
        
    return render_template("default.html", result = Markup(data))



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

                requests.post(url=URL_log, json={
                    'text': 'APPHTML Valid login from {}, method = {}'.format(request.remote_addr,
                                                                                     request.method)})
                return render_template("default.html", result = Markup(data))
            else:
                data = "<h2>Invalid password</h2>"
        else:
            data = "<h2>Invalid username</h2>"

        requests.post(url=URL_log, json={
            'text': 'APPHTML INVALID login from {}, method = {}'.format(request.remote_addr, request.method)})
    return render_template("login.html", result = Markup(data))

@app.route('/logoutAdmin')
def logoutAdmin():
    session.pop("USERNAME", None)

    return redirect(url_for('loginAdmin'))


@app.route('/QRcode')
def QRcode():
    return render_template("qrcode.html")


@app.route('/Secret', methods=['GET', 'POST'])
def Secret():
    if not session.get('Fenix') is None:
        try:
            loginName = session.get('Fenix')
        except KeyError:
            return redirect('/Secretlogout')
        
        if request.method == "POST":
            if(request.is_json):
                try:
                    req_code = request.json["code"]
                except KeyError:
                    return jsonify("No code inserted")

                username = ""
                name = ""
                photo = ""
                for i in FENIX_user.keys():
                    if FENIX_user[i]['secret_code'] == req_code:
                        username = FENIX_user[i]['username']
                        name = FENIX_user[i]['name']
                        photo = FENIX_user[i]['photo']['data']
                        FENIX_user[username]['secret_code'] = None
                        break
                
                if username == "":
                    data = "Invalid code"
                else:
                    if loginName != username:
                        USER_STACK[username] = FENIX_user[loginName]

                    data ='<h2>Requested user: {} - {}</h2>'.format(username, name)
                    data +='<div><img src="data:image/png;base64,{}"/></div>'.format(photo)

                return jsonify(data)
            else:
                return "ERROR"
        else:
            try:
                name = FENIX_user[loginName]['name']
            except KeyError:
                return redirect('/Secretlogout')

            code = FENIX_user[loginName]['secret_code']
            if None == None:
                FENIX_user[loginName]['secret_code'] = randomStringDigits()
                code = FENIX_user[loginName]['secret_code']

            return render_template("secret.html", username=loginName, name=name, code=code)
    else:
        redPage = fenixLoginpage % (client_id, redirect_uri)
        return redirect(redPage)


@app.route('/Secretlistener')
def secret_listener():
    if not session.get('Fenix') is None:
        loginName = session.get('Fenix')

        if loginName not in USER_STACK.keys():
            return redirect('/Secretlogout')

        while USER_STACK[loginName] == None:
            pass
        
        username = USER_STACK[loginName]['username']
        name = USER_STACK[loginName]['name']
        photo = USER_STACK[loginName]['photo']['data']
        USER_STACK[loginName] = None
        FENIX_user[username]['secret_code'] = randomStringDigits()
        
        data ='<h2>Requested user: {} - {}</h2>'.format(username, name)
        data +='<div><img src="data:image/png;base64,{}"/></div>'.format(photo)   

        return jsonify(data)
    else:
        return redirect("/Secret")


@app.route('/userAuth')
def userAuthentication():
    code = request.args['code']

    payload = {'client_id': client_id, 'client_secret': client_secret, 'redirect_uri' : redirect_uri, 'code' : code, 'grant_type': 'authorization_code'}
    response = requests.post(fenixacesstokenpage, params = payload)
    if(response.status_code == 200):
        r_token = response.json()

        params = {'access_token': r_token['access_token']}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
        r_info = resp.json()
        loginName = r_info['username']
        s_code = randomStringDigits()
        session['Fenix'] = loginName
        FENIX_user[loginName] = {'username':loginName, 'name':r_info['name'], 'photo':r_info['photo'], 'secret_code':s_code, 'token':r_token['access_token']}
        USER_STACK[loginName] = None
        requests.post(url=URL_log, json={
            'text': 'APPHTML Successful token request from {}, method = {}'.format(request.remote_addr, request.method)})
        return redirect('/Secret')
    else:
        requests.post(url=URL_log, json={
            'text': 'APPHTML Unsuccessful token request from {}, method = {}'.format(request.remote_addr, request.method)})
        return render_template("error_manager.html")


@app.route('/Secretlogout')
def secret_logout():
    if session.get('Fenix') in FENIX_user.keys():
        del FENIX_user[session.get('Fenix')]

    session.pop('Fenix', None)

    return redirect('/')

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