#coding: utf8
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import basedir


app = Flask(__name__, static_folder='static')
app.config.from_object('config')
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
from . import views, models
from news.get_news import *

#runTask(get_news)
