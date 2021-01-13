# app.py
#!bin/python
from flask import Flask, request, render_template
from models import RegForm, UploadForm
from flask_bootstrap import Bootstrap
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient("mongodb://singer:inMyDefence@kvarken.it:27017/?authSource=songscrypt&authMechanism=SCRAM-SHA-256")
db = client['songscrypt'] 
users = db['users']
songs = db['songs']


app.config.from_mapping(
    SECRET_KEY=b'myPL%9$7Ae5S%CTpwS^M4TNGGkND$Z5f')
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        users.insert_one({'username': username, 'name': name, \
                               'password': password,'email':email})
        return render_template('registrationdone.html', name=name)
    return render_template('registration.html', form=form)

@app.route('/uploadsong', methods=['GET', 'POST'])
def uploadsong():
    form = UploadForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        title = request.form['title']
        author = request.form['author']
        chords = request.form['chords']
        songs.insert_one({'title': title, 'author': author, \
                          'chords': chords})
        return render_template('uploadsongdone.html', title=title, author=author)
    return render_template('uploadsong.html', form=form)

@app.route('/allsongs',)
def allsongs():
    songslist = songs.find()
    return render_template('allsongs.html', songslist=songslist)

if __name__ == '__main__':
    app.run()
