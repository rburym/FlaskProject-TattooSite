"""
Модуль приложения Flask для сайта.

Этот модуль отвечает за инициализацию основного объекта Flask приложения, его
конфигурацию, а также подключение и настройку различных расширений Flask.
Включает в себя настройку подключения к базе данных, управление
пользовательскими сессиями и отображение всплывающих уведомлений.

Конфигурации:
    SECRET_KEY (str): Секретный ключ для поддержания безопасности и cookies.
    SQLALCHEMY_DATABASE_URI (str): URI для подключения к базе данных.
    TOASTR_POSITION_CLASS(str): Расположение выводимого уведомления Flash.

Атрибуты:
    app (Flask): Экземпляр приложения Flask.
    db (SQLAlchemy): Объект для работы с базой данных через ORM.
    manager (LoginManager): Менеджер для управления пользовательскими сессиями.
    toastr (Toastr): Система уведомлений для фронтенда.
"""
import uuid

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_toastr import Toastr
from config import SECRETKEY


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb1.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = str(uuid.uuid4())
manager = LoginManager(app)
app.config['SECRET_KEY'] = SECRETKEY
app.config['TOASTR_POSITION_CLASS'] = 'toast-top-left'
toastr = Toastr(app)

