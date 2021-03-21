from flask import (Flask, render_template, 
                   redirect, url_for, request, make_response, flash)
from options import DEFAULTS
import json

app = Flask(__name__)
app.secret_key = "1#234[p;5jonkcnv902354['123i515'3/zcv#,9840[7['AOHJA9sHFA0[934Y5T2-]]"

def get_saved_data():
    try:
        data = json.loads(request.cookies.get("character"))
    except TypeError:
        data = {}
    return data

@app.route("/")
def index():
    stream = models.Post.select().limit(100)

@app.route("/builder")
def builder():
    return render_template("builder.html", saves=get_saved_data(), options=DEFAULTS)

@app.route("/save", methods=["POST"])
def save():
    flash("Alright!")
    response = make_response(redirect(url_for("builder")))
    data = get_saved_data()
    data.update(dict(request.form.items()))
    response.set_cookie("character", json.dumps(data))
    return response


app.run(host="localhost", port=8000, debug=True)