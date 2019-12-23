from flask import Flask,request
import datetime
import os

import logging.config

app = Flask(__name__)

logging.config.fileConfig('logging.cfg')
app.logger = logging.getLogger('defaultLogger')


@app.route('/log', methods=['Post'])
def logText():
    d= datetime.datetime.today()
    try:
        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        rel_path = "Logs/LogService.LOG"
        abs_file_path = os.path.join(script_dir, rel_path)
        with open(abs_file_path, 'a+') as file:
            log_text = request.args.get('text')
            file.write("{} -> {}\n".format(d,log_text))
            return "i did it"
    except Exception as ex:
        print("Woops something went wrong when logging|{}|{}".format(d,ex))
    return "i didnt do it to em"


if __name__ == "__main__":
    app.run(debug=True, port=4000)
