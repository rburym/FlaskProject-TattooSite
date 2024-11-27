"""
Модуль для работы с API CrystalPay, использования кассы.
"""

from business_logic.crystalpay_sdk import *
from config import BALogin, BASecret, BSalt

crystalpayAPI = CrystalPAY(BALogin, BASecret, BSalt)


def payment(amount: int):
    """
    Функция создает ссылку на оплату
    :param amount: int (сумму операции)
    :return: url (ссылка на созданную кассу)
    """
    return crystalpayAPI.Invoice.create(int(amount), InvoiceType.purchase, 5, description="TESTPayment").get('url')