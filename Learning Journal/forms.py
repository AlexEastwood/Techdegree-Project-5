from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Optional
from datetime import datetime


class NewEntry(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    date = DateField("Date", format="%Y-%m-%d", default=datetime.today,
                     validators=[Optional()])
    time_spent = IntegerField("Time Spent", validators=[DataRequired()])
    learned = TextAreaField("Learned", validators=[DataRequired()])
    resources = TextAreaField("Resources", validators=[DataRequired()])
