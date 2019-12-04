# utilizar GET

# considerar implementar uma cache


from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import requests

app = Flask(__name__)

#@app.route('/')
#def main():

@app.route('/canteen')
# menu da semana
def canteen_week():
    #/canteen?day=dd/mm/yyyy para saber menu da semana do dia dd/mm/yyyy
    #/canteen retorna o menu da semana atual
    try:
        r = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen")
    except requests.exceptions.InvalidURL:
        return jsonify("Fenix service is down")
    print(r.status_code)
    data = r.json()
    print(data)
    return jsonify(str(r.json()))

#dia tem de estar em dd-mm-yyyy
@app.route('/canteen/<day>')
def canteen_day(day):
    day = day.replace("-", "/")
    print(day)
    try:
        r = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen?day="+day)
    except requests.exceptions.InvalidURL:
        return jsonify("Fenix service is down")

    print(r.status_code)
    if int(r.status_code) != 200:
        return jsonify("Invalid date")
    else:
        data = r.json()
        print(data)

        result = None
        for i in range(len(data)):
            if day in data[i].values():
                result = data[i]
                break
        return jsonify(str(result))

if __name__ == "__main__":
    app.run(debug=True, port=5000)

