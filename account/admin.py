from django.contrib import admin
from .models import *
import locale


# Register your models here.

def int_with_commas(x):
    if type(x) not in [type(0), ]:
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + int_with_commas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)


class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'balance']

    @staticmethod
    def balance(instance):
        return int_with_commas(instance.balance)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account__name', 'amount', 'is_deposit']

    @staticmethod
    def account__name(instance):
        return instance.account.name


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
