import os

DATABASE_URL = "postgresql://localhost/courier_db"

class Config(object):
    DEBUG = True
    CSRF_ENABLED = True
    SECRET_KEY = 'key'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
