from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class TierlistPropertiesForm(FlaskForm):
    name = StringField('Name', validators=[
                       DataRequired(), Length(min=1, max=20)])
    is_public = BooleanField('Public')
    submit = SubmitField('Save')
