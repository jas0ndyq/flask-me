# -*- coding: utf-8 -*-
from app import db
from datetime import datetime, date, timedelta
import time

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(8))
	email = db.Column(db.String(120), unique=True)
	avatar = db.Column(db.String(), default='default.jpg')
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
	pub_date = db.Column(db.DateTime, default=datetime.now)
	user = db.relationship('User', backref=db.backref('pose_set', lazy='dynamic'))
	user_name = db.Column(db.String, db.ForeignKey('user.username'))
	vote_count = db.Column(db.Integer, default=0)

	def __init__(self, body, user, pub_date=None):
		self.body = body
		self.user = user
		self.pub_date = pub_date

	def __repr__(self):
		return '<Content %r>' % self.body

	@staticmethod
	def get_content_by_date(day):
		pieces = Content.query.filter(db.func.date(Content.pub_date) == day).order_by(Content.pub_date.desc())
		if day == date.today():
			date_string = '今天'
		elif day == date.today() - timedelta(days=1):
			date_string = '昨天'
		else:
			date_string = "%s年%s月%s日" % (day.year, day.month, day.day)

		return {
			'date': day,
			'date_string': date_string,
			'pieces': pieces,
		}

class Media(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	weibo = db.Column(db.String)
	weixin = db.Column(db.String)
	douban = db.Column(db.String)
	twitter = db.Column(db.String)
	github = db.Column(db.String)
	zhihu = db.Column(db.String)
	user = db.relationship('User', backref=db.backref('pose_set2', lazy='dynamic'))
	user_name = db.Column(db.String, db.ForeignKey('user.username'))

	def __init__(self, weibo, weixin, douban, twitter, github, zhihu, user):
		self.weibo = weibo
		self.weixin = weixin
		self.douban = douban
		self.twitter = twitter
		self.github = github
		self.zhihu = zhihu
		self.user = user

class VoteStat(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	create_at = db.Column(db.DateTime, default=datetime.now)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', backref=db.backref('voted_pieces',
                                                      lazy='dynamic',
                                                      order_by='desc(VoteStat.create_at)'))
	content_id = db.Column(db.Integer, db.ForeignKey('content.id'))
	content = db.relationship('Content', backref=db.backref('voted_content',
				lazy='dynamic',
				order_by='asc(VoteStat.create_at)'))