from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField


class ManageTierlistForm(FlaskForm):
    name = StringField('Name')
    is_public = BooleanField('Public')
    submit = SubmitField('Save')
