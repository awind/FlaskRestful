from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth
import config

app = Flask(__name__)
databaseurl = 'mysql://%s:%s@%s:%s/%s' %(config.MYSQL_USER, config.MYSQL_PASS, config.MYSQL_HOST, config.MYSQL_PORT, config.MYSQL_DB)
app.config['SQLALCHEMY_DATABASE_URI'] = databaseurl
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'secret_key'
ma = Marshmallow(app)
auth = HTTPBasicAuth()

db = SQLAlchemy(app)

#create database
from .model import User
db.create_all()

from app import apis, model


