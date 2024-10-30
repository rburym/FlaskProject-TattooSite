from http.client import responses

from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, login_user, logout_user
from app import app, db
from models import User


@app.route('/')
def index():
    return render_template('Tattoomain.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        mail = request.form.get('mail')
        login = request.form.get('login')
        password = request.form.get('password')
        print(mail, login, password)
        if 4 < len(mail) < 32 and 4 < len(login) < 32 and 4 < len(password) < 64:
            print('Введен корректный пароль.')
            user = User(mail=mail, login=login, password=password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
    return render_template('Tattooreg.html')

@app.route('/about')
@login_required
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        user = User.query.filter_by(login=login, password=password).first()  # .all()
        if user:
            print(user.login, user.password, user.created_at)
            login_user(user)
            return redirect(url_for('index'))
        elif user.login == 'admin':
            abort(403)
        else:
            return redirect(url_for('register'))
    return render_template('TattooLK.html')


@app.route('/Lk')
def personal_cab():
    return render_template('Lkmainpage.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('register'))
    return response