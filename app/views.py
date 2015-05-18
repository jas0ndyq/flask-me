# -*- coding: utf-8 -*-
import os
from flask import render_template, redirect, url_for, request, send_from_directory,get_template_attribute, json
from app import app, db
from models import User, Content, Media
from forms import MyForm, UsernamePasswordForm, ContentForm, MediaForm
from flask.ext.login import login_user, logout_user, login_required, current_user
from werkzeug import secure_filename

import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入   
sys.setdefaultencoding('utf-8')
import time
import datetime
from datetime import date, timedelta

@app.route('/')
def index():
	index_show = Content.query.order_by(Content.pub_date.desc()).all()

	pieces_data = []
	start_date = None
	for delta in xrange(0, 5):
		target_day = date.today() - timedelta(days=delta)
		pieces_data.append(Content.get_content_by_date(target_day))
		start_date = target_day.strftime('%Y-%m-%d')
		
	return render_template('index.html',
		index_show=index_show,
		pieces_data = pieces_data,
		start_date = start_date,
		timedelta = timedelta
		)


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

ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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
				twitter = form_media.twitter.data,
				github = form_media.github.data,
				zhihu = form_media.zhihu.data,
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
		if form_media.twitter.data != '' and user_media != None:
			user_media.twitter = form_media.twitter.data
			db.session.commit()
		if form_media.github.data != '' and user_media != None:
			user_media.github = form_media.github.data
			db.session.commit()
		if form_media.zhihu.data != '' and user_media != None:
			user_media.zhihu = form_media.zhihu.data
			db.session.commit()
		return redirect('/accounts/settings')

	useravatar = User.query.filter_by(username=username).first()
	if request.method == 'POST':
		global file
		file = request.files['file']
		useravatar.avatar = secure_filename(file.filename)
		db.session.commit()
		if file and allowed_file(file.filename):
			global filename
			filename = secure_filename(file.filename)
			file.save(os.path.join(UPLOAD_FOLDER, filename))
			avatar_url = url_for('uploaded_file', filename=filename)
			return redirect('accounts/settings')
	return render_template('/accounts/settings.html',
		form=form,
		user_content=user_content,
		form_media=form_media,
		user_media=user_media,
		file=file,
		useravatar=useravatar,
		)


@app.route('/upload/<filename>')
def uploaded_file(filename):

    	return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/user/<username>', methods=['GET'])
def show_user(username):
	user = User.query.filter_by(username=username).first_or_404()
	user_avatar = user.avatar
	if user == None:
		return redirect('/404')
	user_media = Media.query.filter_by(user_name=username).first()
	user_content = Content.query.filter_by(user_name=username).order_by(Content.pub_date.desc()).first()
	return render_template('/user.html',
		user_content=user_content,
		user_media=user_media,
		username=username,
		user = user,
		)

@app.route('/json', methods=['POST'])
def pieces_by_date():
	start = request.form.get('start')
	if start:
		start_date = datetime.datetime.strptime(start, '%Y-%m-%d').date()
	else:
		start_date = date.today() - timedelta(days=3)
	days = request.form.get('days', 2, type=int)
	html = ''
	for i in xrange(days):
		target_day = start_date - timedelta(days=i)
		pieces_data = Content.get_content_by_date(target_day)
		test = get_template_attribute('other.html', 'test')
		html += test(pieces_data)
	return html