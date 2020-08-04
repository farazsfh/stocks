from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class AddStockForm(FlaskForm):
    ticker = StringField('Ticker')
    submit = SubmitField('Add')