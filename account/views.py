from django.shortcuts import render
from .models import *
from django.http import HttpResponse


def get_balance(request):
    t = Account.objects.first()

    return HttpResponse(t.balance)

def deposit(request, amount):
    t = Account.objects.first()
    Transaction.objects.create(amount=amount, account=t, is_deposit=True)

    return HttpResponse("deposited: " + str(amount))

def withdrawal(request, amount):
    t = Account.objects.first()
    Transaction.objects.create(amount=amount, account=t, is_deposit=False)

    return HttpResponse("withdrawaled: " + str(amount))