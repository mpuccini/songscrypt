# model.py
from wtforms import SubmitField, BooleanField, StringField, PasswordField, TextAreaField, validators
from flask_wtf import Form


class RegForm(Form):
  username = StringField('Username', 
                 [validators.DataRequired()])
  name = StringField('Complete Name', 
                 [validators.DataRequired()])
  email = StringField('Email Address', [validators.DataRequired(), 
             validators.Email(), validators.Length(min=6, max=35)])
  password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', 
                           message='Passwords must match')
        ])
  confirm = PasswordField('Repeat Password')
  submit = SubmitField('Submit')

class UploadForm(Form):
  title = StringField('Song Title',
                 [validators.DataRequired()])
  author = StringField('Author Name', 
                 [validators.DataRequired()])
  chords = TextAreaField('Song Text & Chords',
                 [validators.DataRequired()])
  source = StringField('Chords Source',
                 [validators.DataRequired()])
  submit = SubmitField('Submit')

class Login(Form):
  username = StringField('name',
                 [validators.DataRequired()])
  password = PasswordField('Password', 
                 [validators.DataRequired()])
  login = SubmitField('Login')

