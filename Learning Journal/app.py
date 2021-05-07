from flask import Flask, render_template, redirect, url_for, flash, request

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
    if form.validate_on_submit():
        models.Entry.create_entry(title=form.title.data.strip(),
                            time_spent=form.time_spent.data,
                            learned=form.learned.data.strip(),
                            resources=form.resources.data.strip())
        flash("Entry Created!", "success")
        print(form)
        return redirect(url_for("index"))
    else:
        print(form.errors)
    return render_template("new.html", form=form)

@app.route("/entries/<int:entry_id>")
def detailed_entry(entry_id):
    entry = models.Entry.get(models.Entry.entry_id==entry_id)
    return render_template("detail.html", entry=entry)

@app.route("/entries/<int:entry_id>/edit", methods=("GET", "POST"))
def edit_entry(entry_id):
    entry = models.Entry.get(models.Entry.entry_id==entry_id)
    form = forms.NewEntry()
    if request.method == 'POST':
        if request.form["button"] == "Delete":
            entry.delete_instance()
            return redirect(url_for('index'))
        elif form.validate_on_submit():
            entry.title = form.title.data
            entry.date = form.date.data
            entry.time_spent = form.time_spent.data
            entry.learned = form.learned.data
            entry.resources = form.resources.data
            entry.save()
            return redirect(url_for("index"))
    return render_template("edit.html", entry=entry, form=form)

@app.route("/entries/<int:id>/delete")
def delete_entry():
    pass

if __name__ == "__main__":
    models.initialize()
    
    try:
        models.Entry.create_entry(
            title="Test Title",
            time_spent="123",
            learned="What I learned today is...",
            resources="These are the test resources, This is also a test resource"
        )
    except ValueError:
        pass
    
    app.run(host=HOST, port=PORT, debug=DEBUG)
    
