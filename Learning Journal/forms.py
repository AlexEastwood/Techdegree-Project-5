from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Optional
from datetime import datetime


class NewEntry(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    date = DateField("Date", format="%d/%m/%Y", default=datetime.today,
                     validators=[Optional()])
    time_spent = IntegerField("Time Spent", validators=[DataRequired()])
    learned = TextAreaField("Learned", validators=[DataRequired()])
    resources = TextAreaField("Resources (separate with a comma)",
                              validators=[DataRequired()])
    tags = StringField("Tags (separate with a comma)", validators=[Optional()])
