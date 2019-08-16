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


def withdrawal(request, amount, mode):
    t = Account.objects.first()

    if mode == "true":
        Transaction.objects.create(amount=amount, account=t, is_deposit=False, ip=get_client_ip(request))

        return HttpResponse("withdrawal: " + str(amount))

    else:
        r = Account.withdraw(t, int(amount), get_client_ip(request))
        if r:
            return HttpResponse("withdrawaled: " + str(amount))
        else:
            return HttpResponse("withdraw failed: " + str(amount))
