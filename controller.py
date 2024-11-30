"""
Модуль Controller для сайта на Flask.

Этот модуль содержит представления, которые обрабатывают запросы от
 пользователя и возвращают соответствующие ответы.
Он взаимодействует с моделями для получения данных и передает эти данные
в шаблоны для отображения пользователям.
Каждое представление ассоциировано с одним или несколькими URL-адресами.

Функции:
- index(): Отображает главную страницу сайта.
- email_confirm(): Подтверждение почты при регистрации.
- register(): Регистрирует нового пользователя в системе.
- login(): Авторизует пользователя в системе.
- personal_cab(): Позволяет пользователю просматривать свой профиль.
- passw(): Позволяет сбросить пароль.
- about(): Отображает страницу сайта "О нас".
- works(): Отображает страницу сайта "Наши работы"
- contacts(): Отображает страницу сайта "Контакты"
- chatpage(): Генерирует и отображает ответы ChatGpt на запросы пользователя.
- tattoopay(): Выводит кастомные ссылки на оплату.
- logout(): Выполняет выход пользователя из системы.
- redirect_to_sign(): Перенаправляет неавторизованных пользователей на
 страницу входа.
Только функция personal_cab() использует декоратор @login_required для
ограничения доступа только для авторизованных пользователей.
"""

import random
import string

from http.client import responses
from flask import render_template, request, redirect, url_for, abort, flash
from flask_login import login_required, login_user, logout_user
from app import app, db
from business_logic.chat import chatrequest
from business_logic.billing import payment
from models import User, EmailConfirm
from mail import send_email
from error import *


@app.route('/')
def index():
    """
    Views для главной страницы.
    """
    return render_template('Tattoomain.html')


@app.route('/email-confirm/<url>')
def email_confirm(url):
    """
    В случае если пользователь переходит по ссылки для подтверждения
    регистрации, то сохраняет данные пользователя для регистрации

    :return: redirect(url_for('index')) в случае если регистрация успешная
             redirect(url_for('register')) в случае если регистрация не прошла
    """
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
    """
    Views для страницы регистрации пользователя.

    GET запрос:
    Возвращает страницу с формой для регистрации и авторизации.

    POST запрос:
    Извлекает из запроса данные формы, включая 'login', 'password' и 'email'.
    Проверяет, что пароль, логи и почта проходят условия. Обращается к функции
    email_confirm, в случае подтверждения регистрации сохраняет пользователя.
    Иначе выдает ошибку error500.html.

    :return: render_template('Tattooreg.html') в случае GET
    запроса или ошибки регистрации, redirect(url_for('index')) в случае
    успешной регистрации.
    """
    if request.method == 'GET':
        return render_template('Tattooreg.html')
    email = request.form.get('email')
    login = request.form.get('login')
    password = request.form.get('password')
    if not (4 < len(email) < 32 and 4 < len(login) < 32 and 4 < len(password) < 32):
        return render_template('Tattooreg.html')
    if login.lower() == 'admin':
        flash({'title': "Ошибка", 'message': "Такой логин не "
         "допустим"}, 'error')
        return render_template('Tattooreg.html')
    user = User(email=email, login=login, password=password)
    db.session.add(user)
    url = ''
    for i in range(32):
        url += random.choice(string.ascii_letters)
    email_confirm = EmailConfirm(login=login, url=url)
    db.session.add(email_confirm)
    db.session.commit()
    send_email(
        f'Приветствуем! Спасибо за регистрацию! Подтвердите'
        f' свою почту, кликнув на ссылку: '
        f'http://127.0.0.1:5000{
        url_for('email_confirm', url=url)}',
        email,'Подтверждение регистрации TattooSite')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Views для страницы авторизации пользователя.

    GET запрос:
    Возвращает страницу с формой для регистрации и авторизации.

    POST запрос:
    Извлекает из запроса 'login' и 'password'. Проверяет наличие пользователя
    с такими данными в базе данных. Если пользователь найден, происходит его
    авторизация. В случае успешной авторизации перенаправление в личный
    кабинет. Иначе возвращает на форму регистрации.

    :return: render_template('TattooLogin.html') в случае GET запроса,
             redirect(url_for('personal_cab')) при успешной авторизации,
             return redirect(url_for('register')) в остальных случаях.
    """
    if request.method == 'GET':
        return render_template('TattooLogin.html')
    login = request.form.get('login')
    password = request.form.get('password')
    if login == "admin":
        abort(403)
    user = User.query.filter_by(login=login, password=password).first()
    if user and user.is_confirm:
        login_user(user, remember=True)
        flash({'title': "Авторизация", 'message':
            "Успешная авторизация"}, 'success')
        return redirect(url_for('personal_cab'))
    else:
        return redirect(url_for('register'))


@app.route('/about')
def about():
    """
    Views для страницы "О нас".
    """
    return render_template('Tattooabout.html')


@app.route('/works')
def works():
    """
    Views для страницы "Наши работы".
    """
    return render_template('TattooWorks.html')


@app.route('/contact')
def contact():
    """
    Views для страницы "Контакты".
    """
    return render_template('TattooContact.html')


@app.route('/passw', methods=['GET', 'POST'])
def passw():
    """
    Views для формы "Забыли пароль?" в "login" формы авторизации.
    """
    return render_template('TattooPass.html')


@app.route('/chatpage', methods=['GET', 'POST'])
def chatpage():
    """
    Views для страницы интеграции с ChatGpt.

    GET запрос:
    Возвращает страницу с формой интеграции.

    POST запрос:
    Извлекает из запроса 'inprequest'. Кидает запрос на api.proxyapi,
    получает ответ от сервиса и помещает его в форму answer на странице.

    :return: render_template('chatpage.html') в случае GET запроса,
             render_template('chatpage.html', answer=answer)
    при успешной авторизации,
    """
    if request.method == 'POST':
        inprequest = request.form.get('inputrequest')
        answer = chatrequest(inprequest)
        return render_template('chatpage.html', answer=answer)
    return render_template('chatpage.html')


@app.route('/tattoopay', methods=['GET', 'POST'])
def tattoopay():
    """
    Views для страницы оплаты услуг.

    GET запрос:
    Возвращает страницу оплаты услуг.

    POST запрос:
    Извлекает из запроса 'amount', проверка что введенная сумма является
    числом. Если введеное значение число, создает ссылку на оплату на
    указанную сумму, переадресация на эту ссылку в новой вкладке.

    :return: render_template('TattooPay.html') в случае GET запроса,
             redirect(new_url) в случае ввода правильной суммы.
    """
    if request.method == 'GET':
        return render_template('TattooPay.html')
    amount = request.form.get('amount')
    if amount and amount.isdigit():
        new_url = payment(amount)
        return redirect(new_url)
    else:
        flash({'title': "Ошибка", 'message':
            "Введено нечисловое значение!"}, 'error')
        return render_template('TattooPay.html')


@app.route('/perscab')
@login_required
def personal_cab():
    """
    Views для личного кабинета пользователя.
    """
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
