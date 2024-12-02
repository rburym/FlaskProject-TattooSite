"""
Модуль для работы с API CrystalPay, использования кассы.
"""

import requests
import json
import hashlib


class InvoiceType:
    """Класс типов оплаты"""
    TOPUP = "topup"
    PURCHASE = "purchase"



class PayoffSubtractFrom:
    """Проверка откуда списывается средства"""
    BALANCE = "balance"
    AMOUNT = "amount"


class CrystalUtils:
    """Дополнительный класс, содержащий в себе дополнительные функции для работы SDK."""

    @staticmethod
    def concat_params(concat_list, kwargs):
        """Соединяет необязательные параметры с обязательными."""
        temp = concat_list
        for key, param in kwargs:
            temp[key] = param
        return temp

    @staticmethod
    def requests_api(method, function, params):
        """Отправка запроса на API."""
        response = json.loads(
            requests.post(
                f"https://api.crystalpay.io/v2/{method}/{function}/",
                data=params,
                headers={'Content-Type': 'application/json'}
            ).text
        )
        if response["error"]:
            raise Exception(response['errors'])
        del response["error"]
        del response["errors"]
        return response


class CrystalPay:
    """Главный класс для работы с CrystalApi."""

    def __init__(self, auth_login, auth_secret, salt):
        """Создание подклассов."""
        self.Me = self.Me(auth_login, auth_secret, CrystalUtils())
        self.Method = self.Method(auth_login, auth_secret, CrystalUtils())
        self.Balance = self.Balance(auth_login, auth_secret, CrystalUtils())
        self.Invoice = self.Invoice(auth_login, auth_secret, CrystalUtils())
        self.Payoff = self.Payoff(auth_login, auth_secret, salt, CrystalUtils())
        self.Ticker = self.Ticker(auth_login, auth_secret, CrystalUtils())

    class Me:
        """Класс для работы с информацией о кассе."""

        def __init__(self, auth_login, auth_secret, crystal_utils):
            self.__auth_login = auth_login
            self.__auth_secret = auth_secret
            self.__crystal_utils = crystal_utils

        def get_info(self):
            """Получение информации о кассе."""
            response = self.__crystal_utils.requests_api(
                "me",
                "info",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret
                })
            )
            return response

    class Method:
        """Класс для работы с методами оплаты."""

        def __init__(self, auth_login, auth_secret, crystal_utils):
            self.__auth_login = auth_login
            self.__auth_secret = auth_secret
            self.__crystal_utils = crystal_utils

        def get_list(self):
            """Получение информации о методах оплаты."""
            response = self.__crystal_utils.requests_api(
                "method",
                "list",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret
                })
            )
            return response

        def edit(self, method, extra_commission_percent, enabled):
            """Изменение настроек метода оплаты."""
            response = self.__crystal_utils.requests_api(
                "method",
                "edit",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret,
                    "method": method,
                    "extra_commission_percent": extra_commission_percent,
                    "enabled": enabled
                })
            )
            return response

    class Balance:
        """Класс для работы с балансом кассы."""

        def __init__(self, auth_login, auth_secret, crystal_utils):
            self.__auth_login = auth_login
            self.__auth_secret = auth_secret
            self.__crystal_utils = crystal_utils

        def get_info(self, hide_empty=False):
            """Получение баланса кассы."""
            response = self.__crystal_utils.requests_api(
                "balance",
                "info",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret,
                    "hide_empty": hide_empty
                })
            )
            return response["balances"]

    class Invoice:
        """Класс для работы с счетами."""

        def __init__(self, auth_login, auth_secret, crystal_utils):
            self.__auth_login = auth_login
            self.__auth_secret = auth_secret
            self.__crystal_utils = crystal_utils

        def get_info(self, invoice_id):
            """Получение информации о счёте."""
            response = self.__crystal_utils.requests_api(
                "invoice",
                "info",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret,
                    "id": invoice_id
                })
            )
            return response

        def create(self, amount, type_, lifetime, **kwargs):
            """Выставление счёта на оплату."""
            response = self.__crystal_utils.requests_api(
                "invoice",
                "create",
                json.dumps(
                    self.__crystal_utils.concat_params(
                        {
                            "auth_login": self.__auth_login,
                            "auth_secret": self.__auth_secret,
                            "amount": amount,
                            "type": type_,
                            "lifetime": lifetime
                        },
                        kwargs.items()
                    )
                )
            )
            return response

    class Payoff:
        """Класс для работы с заявками на вывод средств."""

        def __init__(self, auth_login, auth_secret, salt, crystal_utils):
            self.__auth_login = auth_login
            self.__auth_secret = auth_secret
            self.__salt = salt
            self.__crystal_utils = crystal_utils

        def create(self, amount, method, wallet, subtract_from, **kwargs):
            """Создание заявки на вывод средств."""
            signature_string = f"{amount}:{method}:{wallet}:{self.__salt}"
            signature = hashlib.sha1(str.encode(signature_string)).hexdigest()

            response = self.__crystal_utils.requests_api(
                "payoff",
                "create",
                json.dumps(
                    self.__crystal_utils.concat_params(
                        {
                            "auth_login": self.__auth_login,
                            "auth_secret": self.__auth_secret,
                            "signature": signature,
                            "amount": amount,
                            "method": method,
                            "wallet": wallet,
                            "subtract_from": subtract_from
                        },
                        kwargs.items()
                    )
                )
            )
            return response

        def submit(self, request_id):
            """Подтверждение заявки на вывод средств."""
            signature_string = f"{request_id}:{self.__salt}"
            signature = hashlib.sha1(str.encode(signature_string)).hexdigest()

            response = self.__crystal_utils.requests_api(
                "payoff",
                "submit",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret,
                    "signature": signature,
                    "id": request_id,
                })
            )
            return response

        def cancel(self, request_id):
            """Отмена заявки на вывод средств."""
            signature_string = f"{request_id}:{self.__salt}"
            signature = hashlib.sha1(str.encode(signature_string)).hexdigest()

            response = self.__crystal_utils.requests_api(
                "payoff",
                "cancel",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret,
                    "signature": signature,
                    "id": request_id,
                })
            )
            return response

        def get_info(self, request_id):
            """Получение информации о заявке на вывод средств."""
            response = self.__crystal_utils.requests_api(
                "payoff",
                "info",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret,
                    "id": request_id,
                })
            )
            return response

    class Ticker:
        """Класс для работы с тикерами валют."""

        def __init__(self, auth_login, auth_secret, crystal_utils):
            self.__auth_login = auth_login
            self.__auth_secret = auth_secret
            self.__crystal_utils = crystal_utils

        def get_list(self):
            """Получение списка тикеров."""
            response = self.__crystal_utils.requests_api(
                "ticker",
                "list",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret,
                })
            )
            return response["tickers"]

        def get(self, tickers):
            """Получение курса валют по отношению к рублю."""
            response = self.__crystal_utils.requests_api(
                "ticker",
                "get",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret,
                    "tickers": tickers
                })
            )
            return response
