from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField

class MyForm(FlaskForm):
    state = TextAreaField(u'State')
    city = TextAreaField(u'City')
    zip_code = TextAreaField(u'Zip Code')
    submit = SubmitField('Search Data')

