# model.py
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, TextAreaField, validators



class UploadForm(FlaskForm):
  title = StringField('Song Title',
                 [validators.DataRequired()])
  author = StringField('Author Name', 
                 [validators.DataRequired()])
  chords = TextAreaField('Song Text & Chords',
                 [validators.DataRequired()])
  source = StringField('Chords Source',
                 [validators.DataRequired()])
  submit = SubmitField('Submit')

class searchForm(FlaskForm):
  query = StringField('', [validators.DataRequired()])
  submit = SubmitField('Submit')  