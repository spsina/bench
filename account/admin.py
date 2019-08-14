from django.contrib import admin
from .models import  *
# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'balance']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account__name', 'amount', 'is_deposit']

    @staticmethod
    def account__name(instance):
        return instance.account.name


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)

