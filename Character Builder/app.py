from flask import (Flask, render_template, 
                   redirect, url_for, request, make_response)
from options import DEFAULTS
import webbrowser
import threading
import json

port = 8000
url = "http://127.0.0.1:{}".format(port)
app = Flask(__name__)

def get_saved_data():
    try:
        data = json.loads(request.cookies.get("character"))
    except TypeError:
        data = {}
    return data

@app.route("/")
def index():
    data = get_saved_data()
    return render_template("index.html", saves=data)

@app.route("/builder")
def builder():
    return render_template(
        "builder.html",
        saves=get_saved_data(),
        options=DEFAULTS
    )
    

@app.route("/save", methods=["POST"])
def save():
    response = make_response(redirect(url_for("builder")))
    data = get_saved_data()
    data.update(dict(request.form.items()))
    response.set_cookie("character", json.dumps(data))
    return response

threading.Timer(1.25, lambda: webbrowser.open(url) ).start()
app.run(debug=True, port=port, host='0.0.0.0')