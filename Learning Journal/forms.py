from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField
from wtforms.validators import DataRequired, Optional


class NewEntry(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    date = DateField("Date", validators=[Optional()])
    time_spent = IntegerField("Time Spent", validators=[DataRequired()])
    learned = StringField("Learned", validators=[DataRequired()])
    resources = StringField("Resources", validators=[DataRequired()])
    