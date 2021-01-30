from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    picture = FileField('Attach picture', validators=[
                        FileAllowed(['jpg', 'png', 'jpeg'])])
    delete_pic = BooleanField('Delete current picture')
    submit = SubmitField("Post")
