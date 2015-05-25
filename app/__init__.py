# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('config')



db = SQLAlchemy(app)

bcrypt = Bcrypt(app)



from app import views, forms, models

from app.models import User


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

@login_manager.user_loader
def load_user(userid):
	return User.query.filter(User.id == userid).first()