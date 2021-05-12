from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required
from models import Entry, Tag, EntryTags, initialize, User, DoesNotExist
import forms

#Variables for hosting the website locally
DEBUG = True
PORT = 8000
HOST = "localhost"

app = Flask(__name__)
app.secret_key = "0a9s8dyfnsd87906asd087-09D86Yd-89gasd-G--84y5bpkzfgh#'flgjsd"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"

@login_manager.user_loader
def load_user(user_id):
    try: 
        User.get(User.user_id == user_id)
    except DoesNotExist:
        return None

#Deletes all tags currently associated with an entry, then writes the new set of tags
def set_tags(tags, title):
    
    EntryTags.delete().where(
        EntryTags.entry == Entry.get(
            Entry.title == title)).execute()
    
    tags = tags.split(", ")
    for tag in tags:
        print(tag)
        try:
            Tag.create_entry(tag_name=tag)
        except ValueError:
            print("That tag already exists")

        EntryTags.create(
            entry=Entry.get(Entry.title == title),
            tag=Tag.get(Tag.tag_name == tag)
        )

@app.route("/")
def index():
    entries = Entry.select()
    
    user = User.get(User.username == "alexeastwood")
    login_user(user)
    
    return (render_template("index.html", entries=entries))


@app.route("/entries")
def entries():
    return index()


@app.route("/entries/<tag>")
def tag_index(tag):
    entries = []
    for entry in EntryTags.select():
        if entry.tag.tag_name == tag:
            entries.append(entry.entry)
        
    return (render_template("index.html", entries=entries))


@app.route("/entries/new", methods=("GET", "POST"))
@login_required
def create_entry():
    form = forms.NewEntry()
    if form.validate_on_submit():
        Entry.create_entry(title=form.title.data.strip(),
                                  time_spent=form.time_spent.data,
                                  learned=form.learned.data.strip(),
                                  resources=form.resources.data.strip())
        if form.tags.data:
            set_tags(form.tags.data, form.title.data.strip())

        return redirect(url_for("index"))
    return render_template("new.html", form=form)


@app.route("/entries/<int:entry_id>")
def detailed_entry(entry_id):
    entry = Entry.get(Entry.entry_id == entry_id)
    return render_template("detail.html", entry=entry)


@app.route("/entries/<int:entry_id>/edit", methods=("GET", "POST"))
@login_required
def edit_entry(entry_id):
    entry = Entry.get(Entry.entry_id == entry_id)
    
    tags = ""
    for tag in entry.get_tags():
        tags = tags + tag.tag_name +", "
    tags = tags[:-2]
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
            
            if form.tags.data:
                set_tags(form.tags.data, form.title.data.strip())
            return redirect(url_for("index"))
    return render_template("edit.html", entry=entry, form=form, tags=tags)

if __name__ == "__main__":
    initialize()

    try:
        Entry.create_entry(
            title="Test Title",
            time_spent="123",
            learned="What I learned today is...",
            resources="These are the test resources, This is also a test resource"
        )
    except ValueError:
        pass
    
    try:
        User.create_user(
            username="alexeastwood",
            password="password"
        )
    except ValueError:
        print("You exist")
    else:
        print("You didn't exist but now you do")
    
    


    app.run(host=HOST, port=PORT, debug=DEBUG)
