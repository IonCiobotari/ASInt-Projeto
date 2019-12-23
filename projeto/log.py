from flask import Flask,request,jsonify
import datetime
import os

import logging.config

app = Flask(__name__)

@app.route('/log', methods=['GET','POST'])
def logText():
    if request.method == 'POST':
        d= datetime.datetime.today()
        try:
            script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
            rel_path = "Logs/LogService.LOG"
            abs_file_path = os.path.join(script_dir, rel_path)
            with open(abs_file_path, 'a+') as file:
                #log_text = request.args.get('text')
                log_text = request.json['text']
                file.write("{} @ {} -> {}\n".format(d,request.remote_addr,log_text))
                return "i did it"
        except Exception as ex:
            print("Woops something went wrong when logging|{}|{}".format(d,ex))
        return "i didnt do it to em"
    else:
        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        rel_path = "Logs/LogService.LOG"
        abs_file_path = os.path.join(script_dir, rel_path)
        to_json = {}
        to_json['logs']=[]
        with open(abs_file_path, 'r') as file:
            log = file.readline()
            while log:
                to_json['logs'].append(log)
                log = file.readline()
            #split = log.split('->')
        return jsonify(to_json)

if __name__ == "__main__":
    app.run(debug=True, port=4000)
