from app import db
import time

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(8))
	email = db.Column(db.String(120), unique=True)

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = password

	def is_correct_password(self, passtext):
		return self.password == passtext

	def is_authenticated(self):
        		return True
 
	def is_active(self):
        		return True
 
	def is_anonymous(self):
        		return False
 
	def get_id(self):
        		return unicode(self.id)

class Content(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	body = db.Column(db.Text)
	pub_date = db.Column(db.String(80))
	user = db.relationship('User', backref=db.backref('pose_set', lazy='dynamic'))
	user_name = db.Column(db.String, db.ForeignKey('user.username'))

	def __init__(self, body, user, pub_date=None):
		self.body = body
		self.user = user
		if pub_date == None:
			pub_date = time.time()
		self.pub_date = pub_date

	def __repr__(self):
		return '<Content %r>' % self.body
