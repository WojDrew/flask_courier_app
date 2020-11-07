import os

db_user = "user1"
db_pass = "pass"
db_port = "5433"
DATABASE_URL = "postgresql://" + db_user + ":" + db_pass + "@localhost:" + db_port + "/courier_db"

class Config(object):
    DEBUG = True
    CSRF_ENABLED = True
    SECRET_KEY = 'very_secret_key'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
