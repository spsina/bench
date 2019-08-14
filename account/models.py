from django.db import models
from django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import pre_save


class Account(models.Model):
    name = models.CharField(max_length=255)

    parity = models.IntegerField(default=0)

    @property
    def balance(self):
        all_deposit = self.transactions.filter(is_deposit=True).aggregate(Sum('amount'))['amount__sum']
        all_withdrawal = self.transactions.filter(is_deposit=False).aggregate(Sum('amount'))['amount__sum']
        
        if all_deposit is None:
            all_deposit = 0
        
        if all_withdrawal is None:
            all_withdrawal = 0

        return all_deposit - all_withdrawal


class Transaction(models.Model):
    amount = models.PositiveIntegerField()
    is_deposit = models.BooleanField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")

    ip = models.CharField(max_length=50, default=0)


@receiver(pre_save, sender=Transaction)
def check_balance(sender,instance, **kwargs):
    if instance.is_deposit:
        instance.account.parity += instance.amount
        instance.account.save()
    else:
        instance.account.parity -= instance.amount
        instance.account.save()

        if instance.account.balance < instance.amount:
            raise Exception("Under Balance")
