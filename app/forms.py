from flask_wtf import Form
from wtforms import StringField, PasswordField, TextField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Email

from util.validators import Unique
from models import User



class MyForm(Form):
	name = StringField('Name', validators=[DataRequired(),
		Unique(User, User.username, message='There is already an account with this username!')])
	email = StringField('Email', validators=[DataRequired(), Email(), 
		Unique(User, User.email, message='There is already an account with that email. ')])
	password = PasswordField('Password', validators=[DataRequired()])
	invitation = StringField('Invitation', validators=[DataRequired()])

class UsernamePasswordForm(Form):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	
class ContentForm(Form):
	contentbox = TextField('Content', validators=[DataRequired()])

class MediaForm(Form):
	weibo = StringField('Content')
	weixin = StringField('Content')
	douban = StringField('Content')
	twitter = StringField('Content')
	github = StringField('Content')
	zhihu = StringField('Content')


