from http.client import responses
from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, login_user, logout_user
from app import app, db
from models import User, EmailConfirm
import random
import string
from  mail import send_email
from error import *

@app.route('/')
def index():
    return render_template('Tattoomain.html')


@app.route('/email-confirm/<url>')
def email_confirm(url):
    email_confirm = EmailConfirm.query.filter_by(url=url).first()
    if email_confirm:
        user = User.query.filter_by(login=email_confirm.login).first()
        user.is_confirm = True
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return redirect(url_for('register'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        login = request.form.get('login')
        password = request.form.get('password')
        print(email, login, password)
        if 4 < len(email) < 32 and 4 < len(login) < 32 and 4 < len(password) < 64:
            print('Введен корректный пароль.')
            user = User(email=email, login=login, password=password)
            db.session.add(user)
            url = ''
            for i in range(32):
                url += random.choice(string.ascii_letters)
            email_confirm = EmailConfirm(login=login, url=url)
            db.session.add(email_confirm)
            db.session.commit()

            send_email(
                f'Подтвердите регистрацию: http://127.0.0.1:5000{url_for('email_confirm', url=url)}',
                email,
                'Подтверждение регистрации')

            return redirect(url_for('index'))
    return render_template('Tattooreg.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        user = User.query.filter_by(login=login, password=password).first()  # .all()
        if user and user.is_confirm:
            print(user.login, user.password, user.created_at)
            login_user(user, remember = True)
            return redirect(url_for('personal_cab'))
        elif user.login == 'admin':
            abort(403)
        else:
            return redirect(url_for('register'))
    return render_template('TattooLogin.html')


@app.route('/about')
# @login_required
def about():
    return render_template('Tattooabout.html')


@app.route('/works')
def works():
    return render_template('TattooWorks.html')


@app.route('/contact')
def contact():
    return render_template('TattooContact.html')


@app.route('/passw', methods=['GET', 'POST'])
def passw():
    if request.method == 'POST':
        mail = request.form.get('mail')
        code = request.form.get('code')
        print(mail, code)
    return render_template('TattooPass.html')


@app.route('/gigachat')
def gigachat():
    return render_template('gigachatpage.html')


@app.route('/perscab')
@login_required
def personal_cab():
    return render_template('personalcabinet.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('login'))
    return response