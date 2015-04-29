from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email

from util.validators import Unique
from models import User

class MyForm(Form):
	name = StringField('Name', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email(), 
		Unique(User, User.email, message='There is already an account with that email. ')])
	password = PasswordField('Password', validators=[DataRequired()])
	invitation = StringField('Invitation', validators=[DataRequired()])

class UsernamePasswordForm(Form):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	