from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField
from wtforms.validators import DataRequired


class NewEntry(Form):
    title = StringField("Title", validators=[DataRequired()])
    date = DateField("Date")
    time_spent = IntegerField("Time Spent", validators=[DataRequired()])
    learned = StringField("Learned", validators=[DataRequired()])
    resources = StringField("Resources", validators=[DataRequired()])
    