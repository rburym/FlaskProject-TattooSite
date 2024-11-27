"""
Модуль моделей приложения Flask для сайта.

Этот модуль отвечает за определение моделей данных, используемых в приложении.
Включает в себя методы для управления данными, такие как создание и сохранение
записей в базе данных.

Классы:
    User: Модель пользователя, содержащая информацию о пользователе, включая
    логин, электронную почту и пароль.
    EmailConfirm: Модель содержащая информацию о подтверждении регистрации
    пользователя по почте.

Функции:
    load_user(user_id): Функция для загрузки пользователя по его
    идентификатору, используется flask_login для управления пользовательскими
    сессиями.

Зависимости:
    Модуль зависит от Flask, Flask-Login, Flask-SQLAlchemy для работы с
    приложением, управления сессиями и взаимодействия с базой данных.
"""


from datetime import datetime
from flask_login import UserMixin
from app import manager, db, app


class User(db.Model, UserMixin):
    """
    Модель пользователя.

    Args:
        id(int): Id пользователя.
        login (str): Логин пользователя. Уникальный и обязательный.
        email (str): Электронная почта. Уникальная и обязательная.
        password (str): Пароль пользователя. Обязательный.
        is_confirm (Boolean): Метка о подтверждении почты.
        created_at (datetime): Дата занесения пользователя в бд.
    """
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(32))
    email = db.Column(db.String(64), unique=True)
    is_confirm = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EmailConfirm(db.Model):
    """
    Модель почты.

    Args:
        login (str): Логин пользователя. Уникальный и обязательный.
        url(str): Созданная ссылка.
    """
    login = db.Column(db.String(20), primary_key=True)
    url = db.Column(db.String(32), unique=True)

@manager.user_loader
def load_user(user_id):
    """
    Callback функция для Flask-Login, которая используется для загрузки
    объекта пользователя.

    Args:
        user_id (str): Строковый идентификатор пользователя, используемый для
                       поиска в базе данных.

    Returns:
        User: Объект пользователя, соответствующий идентификатору. Возвращает
              None, если пользователь не найден.
    """
    return User.query.get(user_id)

with app.app_context():
    db.create_all()
