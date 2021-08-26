import os

class Config(object):
    mongo_uri = os.getenv('MONGO_URI')

    SECRET_KEY = os.urandom(32)
