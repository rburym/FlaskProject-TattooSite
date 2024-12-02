"""
Модуль для работы с API CrystalPay, использования кассы.
"""

from business_logic.crystalpay_sdk import *
from config import BSALT, BALOGIN, BASECRET

crystalpayAPI = CrystalPay(BALOGIN, BASECRET, BSALT)


def payment(amount: int) -> str:
    """
    Функция создает ссылку на оплату
    :param amount: int (сумму операции)
    :return: str (ссылка на созданную кассу)
    """
    return crystalpayAPI.Invoice.create(int(amount), InvoiceType.PURCHASE, 5, description="TESTPayment").get('url')