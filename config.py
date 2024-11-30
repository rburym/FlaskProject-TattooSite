"""
Этот модуль предоставляет функциональность для настройки, установку доступа
и взаимодействия API с функциями сайта.

Конфигурации:
    Константы:
    os.getenv('BALOGIN') - Логин кассы CrystalPay.
    os.getenv('BASECRET') - Секретный ключь кассы CrystalPay.
    os.getenv('BSALT') - Salt кассы CrystalPay.
    os.getenv('APIKEY') - Ключ API proxyapi
    os.getenv('EMAIL') - Почта с которой будут отправки писем.
    os.getenv('EPASS') - Пароль приложения от почты.
    os.getenv('SECRETKEY') - Секретный ключ для поддержания безопасности
сессий и cookies.


Для работы с ProxyAPI необходимо установить библиотеку openai:

    pip install openai
"""

import os

BALOGIN = os.getenv('BALOGIN')
BASECRET = os.getenv('BASECRET')
BSALT = os.getenv('BSALT')
API_KEY = os.getenv('APIKEY')
EMAIL_FROM = os.getenv('EMAIL')
EMAIL_PAS = os.getenv('EPASS')
SECRETKEY = os.getenv('SECRETKEY')

