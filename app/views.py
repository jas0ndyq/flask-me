# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for
from app import app, db
from models import User, Content, Media
from forms import MyForm, UsernamePasswordForm, ContentForm, MediaForm
from flask.ext.login import login_user, logout_user, login_required, current_user



@app.route('/')
def index():
	index_show = Content.query.order_by(Content.pub_date.desc()).all()

	return render_template('index.html', index_show=index_show)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
	form = UsernamePasswordForm()
	
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first_or_404()
		if user.is_correct_password(form.password.data):
			login_user(user)
			username = current_user.username
			location = '/user/%s' % username
			return redirect(location) 
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

@app.route('/accounts/settings', methods=['POST', 'GET'])
@login_required
def show():
	username = current_user.username
	user_content = Content.query.filter_by(user_name=username).order_by(Content.pub_date.desc()).first()
	form = ContentForm()
	if form.validate_on_submit():
		if user_content == None:
			new_content = Content(
				body = form.contentbox.data,
				user = current_user
				)
			db.session.add(new_content)
			db.session.commit()
		#return new_content
			return redirect('/')
		else:
			user_content.body = form.contentbox.data
			db.session.commit()
			return redirect('/')

	form_media = MediaForm()
	user_media = Media.query.filter_by(user_name=username).first()
	if form_media.validate_on_submit():
		if user_media == None:
			media_setting = Media(
				user = current_user,
				weibo = form_media.weibo.data,
				weixin = form_media.weixin.data,
				douban = form_media.douban.data,
				)
			db.session.add(media_setting)
			db.session.commit()
		if form_media.weibo.data != '' and user_media != None:
			user_media.weibo = form_media.weibo.data
			db.session.commit()
		if form_media.weixin.data != '' and user_media != None:
			user_media.weixin = form_media.weixin.data
			db.session.commit()
		if form_media.douban.data != '' and user_media != None:
			user_media.douban = form_media.douban.data
			db.session.commit()
			



		return redirect('/accounts/settings')
	return render_template('/accounts/settings.html', form=form, user_content=user_content, form_media=form_media, user_media=user_media)


@app.route('/user/<username>', methods=['GET'])
def show_user(username):
	user_media = Media.query.filter_by(user_name=username).first()
	user_content = Content.query.filter_by(user_name=username).order_by(Content.pub_date.desc()).first()
	return render_template('/user.html', user_content=user_content, user_media=user_media, username=username)	