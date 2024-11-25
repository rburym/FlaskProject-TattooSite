from business_logic.crystalpay_sdk import *
import os

BALogin = os.getenv('BALogin')
BASecret = os.getenv('BASecret')
BSalt = os.getenv('BSalt')

crystalpayAPI = CrystalPAY(BALogin, BASecret, BSalt)

# print(crystalpayAPI.Me.getinfo())
# # print(crystalpayAPI.Balance.getinfo(hide_empty=False))
# print(crystalpayAPI.Invoice.create(100, InvoiceType.purchase, 5, description="TESTPayment"))
# print(crystalpayAPI.Invoice.create(100, InvoiceType.purchase, 5, description="TESTPayment").get('url'))

def payment(amount):
    return crystalpayAPI.Invoice.create(int(amount), InvoiceType.purchase, 5, description="TESTPayment").get('url')