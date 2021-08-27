# app.py
#!bin/python
from flask import Flask, request, render_template
from models import UploadForm, searchForm
from pymongo import MongoClient, results
import logging
from config import Config
from langdetect import detect

app = Flask(__name__)
app.config.from_object(Config)

## Logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

def connect2mongo(configuration, collection):
    '''
    Establishes connection with mongoDB

    Parameters
    ----------
    collection : str
        collection name where to store data on mongoDB

    Returns 
    -------
    collection : str
        returns a connection to defined collresultection
    '''
    c = configuration
    try:
        client = MongoClient(c.mongo_uri)
        coll = client['songscrypt'][collection]
    except Exception:
        log.error("Cannot connect to mongo (check if you're under ENEA VPN)")
        raise Exception("Cannot connect to mongo")
    
    log.info("Connection to mongo succeded!")

    return coll

def upload2mongo(doc):
    '''
    Upload document to mongoDB collection

    Returns 
    -------
    none
    '''
    c = Config()    


    # Don't known if "doc" is printable (check __repr__ magic method)
    log.debug("Uploading %s to mongoDB", doc)
    
    try:
        log.debug("Connecting to songscrypt db")
        coll = connect2mongo(c, 'songs')
    except Exception as e:
        # Better catch more significative exception types
        # (if connect2mongo() raises some)
        log.error("Cannot connect to mongo: %s", e)
        return

    log.debug("Inserting new document")    
    coll.insert_one(doc) 

def getAllSongs():
    '''
    Get list of all songs

    Returns 
    -------
    songlist
    '''
    c = Config()    


    # Don't known if "doc" is printable (check __repr__ magic method)
    log.debug("Get songs from mongoDB")
    
    try:
        log.debug("Connecting to songscrypt db")
        coll = connect2mongo(c, 'songs')
    except Exception as e:
        # Better catch more significative exception types
        # (if connect2mongo() raises some)
        log.error("Cannot connect to mongo: %s", e)
        return

    log.debug("Inserting new document")    
    songlist = coll.find() 

    return songlist

def search(query):
    '''
    Full text search in mongoDB

    Returns 
    -------
    results
    '''
    c = Config()    


    # Don't known if "doc" is printable (check __repr__ magic method)
    log.debug("Search %s in mongoDB", query)
    
    try:
        log.debug("Connecting to songgscrypt db")
        coll = connect2mongo(c, 'songs')
    except Exception as e:
        # Better catch more significative exception types
        # (if connect2mongo() raises some)
        log.error("Cannot connect to mongo: %s", e)
        return

    log.debug("Inserting new document")    
    results = coll.find({'$text':{'$search':query}})
    
    return results



def getSong(title):
    '''
    Get single song from mongoDB

    Returns 
    -------
    results
    '''
    c = Config()    


    # Don't known if "doc" is printable (check __repr__ magic method)
    log.debug("Search %s in mongoDB", title)
    
    try:
        log.debug("Connecting to songgscrypt db")
        coll = connect2mongo(c, 'songs')
    except Exception as e:
        # Better catch more significative exception types
        # (if connect2mongo() raises some)
        log.error("Cannot connect to mongo: %s", e)
        return

    log.debug("Inserting new document")    
    results = coll.find_one({'title':title})
    
    return results





@app.route('/', methods=['GET', 'POST'])
def index():
    form = searchForm(request.form)
    if  request.method == 'POST' and form.validate_on_submit(): 
        collection = connect2mongo(Config(), 'songs')
        query = request.form['query']
        res = collection.find({'$text':{'$search':query}})
        return render_template('allsongs.html', songslist=list(res))
    return render_template('index.html', form=form)

@app.route('/uploadsong', methods=['GET', 'POST'])
def uploadsong():
    form = UploadForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        doc = {}
        doc['title'] = request.form['title']
        doc['author'] = request.form['author']
        chords = request.form['chords']
        doc['original_chords'] = chords
        doc['language'] = detect(chords)
        chords = chords.replace(' ', '&nbsp')
        doc['chords'] = chords.replace('\r\n','<br />')
        doc['source'] = request.form['source']
        upload2mongo(doc)
        return render_template('uploadsongdone.html')
    return render_template('uploadsong.html', form=form)

@app.route('/allsongs',)
def allsongs():
    songslist = getAllSongs()
    return render_template('allsongs.html', songslist=songslist)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = searchForm(request.form)
    if  request.method == 'POST' and form.validate_on_submit():
        res = search(request.form['query'])
        return render_template('results.html', results=list(res))
    return render_template('search.html', form=form)

@app.route('/getsong/<title>')#, methods=['GET', 'POST'])
def getsong(title):
   song = getSong(title)
   return render_template('song.html', song=song)


if __name__ == '__main__':
    app.run(debug=True)
