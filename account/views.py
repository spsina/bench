from django.shortcuts import render
from .models import *
from django.http import HttpResponse


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_balance(request):
    t = Account.objects.first()

    return HttpResponse(t.balance)


def withdrawal(request, amount):
    t = Account.objects.first()
    r = Account.withdraw(t,int(amount),get_client_ip(request))
    if r:
        return HttpResponse("withdrawaled: " + str(amount))
    else:
        return HttpResponse("withdraw failed: " + str(amount))
