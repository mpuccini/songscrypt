# SongsCrypt
A simple repository for the chords of my favorite songs.  
Data are assumed to be stored with mongoDB into a database named `songscrypt` that contains two collections:  
 - `songs`: the song chords archive
 - `users`: that stores registered users
 
## Clone repository
```
git clone https://gitea.kvarken.it/mpuccini/songscrypt.git
```

## Create a virtualenv
```
cd songscrypt
```
```
python3 -m venv <venvname>
```

## Install dependencies
```
source songscrypt/<venvname>/bin/activate
```
```
pip3 install -r requirements.txt
```

## Hot to run app
```
/songscrypt/<venvname>/bin/python3 /songscrypt/<venvname>/bin/gunicorn --workers 3 --bind unix:/songscrypt/songscrypt.sock -m 007 wsgi:app
```

## ToDo
 - [X] Add registration form
 - [X] Add upload form
 - [X] Add list of all songs
 - [ ] Add a navbar
 - [ ] Add a login
 - [ ] Add a search
