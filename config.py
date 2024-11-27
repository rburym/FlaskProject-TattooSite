"""
Этот модуль предоставляет функциональность для настройки, установку доступа
и взаимодействия API с функциями сайта.

Конфигурации:

    os.getenv('BALogin') - Логин кассы CrystalPay.
    os.getenv('BASecret') - Секретный ключь кассы CrystalPay.
    os.getenv('BSalt') - Salt кассы CrystalPay.
    os.getenv('APIKEY') - Ключ API proxyapi
    os.getenv('EMAIL') - Почта с которой будут отправки писем.
    os.getenv('EPASS') - Пароль приложения от почты.
    os.getenv('SecretKey') - Секретный ключ для поддержания безопасности сессий и cookies.


Для работы с ProxyAPI необходимо установить библиотеку openai:

    pip install openai
"""

import os

BALogin = os.getenv('BALogin')
BASecret = os.getenv('BASecret')
BSalt = os.getenv('BSalt')
API_KEY = os.getenv('APIKEY')
EMAIL_FROM = os.getenv('EMAIL')
EMAIL_PAS = os.getenv('EPASS')
SecretKey = os.getenv('SecretKey')
