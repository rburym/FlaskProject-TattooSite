"""
Модуль для обработки ошибок
"""

from flask import render_template
from app import app

@app.errorhandler(403)
def error403(e):
    """
    Функция обрабатывает ошибку HTTP 403.

    :return: error403.html (Шаблон страницы ошибки)
    """
    return render_template('errors/error403.html')

@app.errorhandler(404)
def error404(e):
    """
    Функция обрабатывает ошибку HTTP 404.

    :return: error404.html (Шаблон страницы ошибки)
    """
    return render_template('errors/error404.html')

@app.errorhandler(500)
def error500(e):
    """
    Функция обрабатывает ошибку HTTP 500.

    :return: error500.html (Шаблон страницы ошибки)
    """
    return render_template('errors/error500.html')
