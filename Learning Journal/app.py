from flask import Flask, render_template

import models

DEBUG = True
PORT = 8000
HOST = "localhost"

app = Flask(__name__)

@app.route("/")
def index():
    entries = models.Entry.select()
    return(render_template("index.html", entries=entries))

@app.route("/entries")
def entries():
    return index()

@app.route("/entries/new")
def create_entry():
    pass

@app.route("/entries/<int:entry_id>")
def detailed_entry(entry_id):
    entry = models.Entry.get(models.Entry.entry_id==entry_id)
    return render_template("detail.html", entry=entry)

@app.route("/entries/<int:entry_id>/edit")
def edit_entry(entry_id):
    entry = models.Entry.get(models.Entry.entry_id==entry_id)
    return render_template("edit.html", entry=entry)

@app.route("/entries/<int:id>/delete")
def delete_entry():
    pass

if __name__ == "__main__":
    models.initialize()
    
    try:
        models.Entry.create_entry(
            title="Test Title",
            time_spent="123",
            learned="What I learned in boating school is...",
            resources="These are the test resources, This is also a test resource"
        )
    except ValueError:
        pass
    
    app.run(host=HOST, port=PORT, debug=DEBUG)
    
