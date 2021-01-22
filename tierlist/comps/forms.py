from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class CompForm(FlaskForm):
    carries = StringField('Carries')
    synergies = StringField("Synergies")
    lolchess = StringField('Lolchess')
    chosen = StringField('Chosen')
    submit = SubmitField('Save')
