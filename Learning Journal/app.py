from flask import Flask, render_template, redirect, url_for

import models, forms

DEBUG = True
PORT = 8000
HOST = "localhost"

app = Flask(__name__)
app.secret_key = "0a9s8dyfnsd87906asd087-09D86Yd-89gasd-8D6G-DS9A8G6-98F7Y-87yy-df8g7dfs-g8ysdf-84y5bpkzfgh#'flgjsd"

@app.route("/")
def index():
    entries = models.Entry.select()
    return (render_template("index.html", entries=entries))

@app.route("/entries")
def entries():
    return index()

@app.route("/entries/new", methods=("GET", "POST"))
def create_entry():
    form = forms.NewEntry()
    models.Entry.create(title=form.title.data.strip(),
                        date=form.date.data.strip(),
                        time_spent=form.time_spent.data.strip(),
                        learned=form.learned.data.strip(),
                        resources=form.resources.data.strip())
    return render_template("new.html")

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
    
