from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app_instance = Flask(__name__)
app_instance.config.from_object(Config)
db = SQLAlchemy(app_instance)
login = LoginManager(app_instance)

from app import routes, models