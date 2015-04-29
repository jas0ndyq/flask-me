# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for
from app import app, db
from models import User, Content
from forms import MyForm, UsernamePasswordForm
from flask.ext.login import login_user, logout_user



@app.route('/')
def index():
	index_show = Content.query.order_by(Content.pub_date).all()


	return render_template('index.html', index_show=index_show)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	form = UsernamePasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first_or_404()
		if user.is_correct_password(form.password.data):
			login_user(user)
			return redirect('/')
		else:
			return redirect('/signin')
	return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
	logout_user()
	return redirect('/')

#注册系统
@app.route('/accounts/create', methods=['GET', 'POST'])
def create_account():
	form = MyForm()
	invitation_no = app.config['INVITATION']
	if form.validate_on_submit():
		user = User(
			email = form.email.data,
			username = form.name.data,
			password = form.password.data,			
		)
		#验证邀请码
		invitation = form.invitation.data
		if invitation == invitation_no:
			db.session.add(user)
			db.session.commit()
			return redirect('/')
		else:
			return redirect('/404')

	return render_template('accounts/create.html', form=form)