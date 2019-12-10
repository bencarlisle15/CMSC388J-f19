from flask import Flask, session
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = b'z\x8b\x7fs\xb2\xfa\xeb\x1a\xe6\xa8\xcd\x81\xf2Qq\xdb'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

from flask_app import routes
from flask_app.models import *