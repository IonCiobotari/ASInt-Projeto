from flask import Flask
from flask import render_template
from flask import request
from flask import Markup
from flask import redirect
from json2html import *
import json
import requests
#import log
import logging.config
import os
import pickle

app = Flask(__name__)
#app.logger = logging.getLogger('defaultLogger')
DB = {}
APIurl = "http://127.0.0.1:6000/API/"

# general html page
@app.route('/<path:path>', methods = ['GET', 'PUT', 'POST', 'DELETE'])
def default_page(path):
    url = APIurl + path
    path = path.split("/")
    data = ""
    
    if request.method == 'POST':
        r = requests.post(url = url, json = request.form)
    elif request.method == 'GET':
        try:
            if request.args['operation'] == 'PUT':
                result = request.args
                r = requests.put(url = url, json = result)
                return redirect("http://127.0.0.1:6100/services/{}".format(path[-1]))
            elif request.args['operation'] == 'DELETE':
                r = requests.delete(url)
                url = APIurl + path[0]
                return redirect("http://127.0.0.1:6100/services")
        except KeyError:
            data += '<h2>An unexpected error ocurred</h2>'
    
    r = requests.get(url)
    data += json2html.convert(json = r.json())
    # if admin
    if path[0] == "services":
        if len(path) == 1:
            data += '<h3>Create new service</h3><form action="/services" method="POST"><p>Name: <input type="text" name="name"></p><p>Location: <input type="text" name="location"></p><p>Hours: <input type="text" name="hours"></p><p>Description: <input type="text" name="description"></p><input type = "submit"></form>'
        else:
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
    # else
    #data += '<href = "/loginAdmin>Login</href>'
    
    
    return render_template("default.html", result = Markup(data))


@app.route('/loginAdmin', methods=['GET', 'Post'])
def loginAdmin():
    if request.form == None:
        return render_template("login.html")
    #TODO do the adming login
    return render_template("login.html")
  

@app.route('/serviceAdmin',methods = ['GET'])
def AdminService():
    r = requests.get(APIurl+"services")
    j = json.loads(r.text)
    #TODO if admin allowed
    #TODO generate list of available IDs and put them on the page
    to_add = ""
    for i in j:
        to_add+='<option value ="{}" \>{}</option>\n'.format(i['ID'],i['ID'])
    return render_template("servicesAdmin.html", Options = Markup(to_add))

@app.route('/serviceChange',methods = ['POST'])
def changeService():
    id = request.form['ID']
    if id =='new':#Post
        return render_template("postService.html", ID=Markup(''),Method = Markup('POST'))
    else: #PUT
        return render_template("postService.html", ID=Markup('/'+id),Method = Markup('PUT'))


 


@app.errorhandler(404)
def error_not_found(error):
    return render_template("error_not_found.html"), 404


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
