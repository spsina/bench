from django.db import models
from django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete, post_save
from django.db import transaction


class Account(models.Model):
    name = models.CharField(max_length=255)

    parity = models.IntegerField(default=0)

    @property
    def balance(self):
        account = self

        all_deposit = account.transactions.filter(is_deposit=True).aggregate(Sum('amount'))['amount__sum']
        all_withdrawal = account.transactions.filter(is_deposit=False).aggregate(Sum('amount'))['amount__sum']
        
        if all_deposit is None:
            all_deposit = 0
        
        if all_withdrawal is None:
            all_withdrawal = 0

        return all_deposit - all_withdrawal

    @classmethod
    def withdraw(cls, the_account, amount, ip):
        with transaction.atomic():
            account = Account.objects.get(pk=the_account.pk)

            balance = account.balance

            if balance >= amount:
                account.parity -= amount
                Transaction.objects.create(amount=amount, account=account, is_deposit=False, ip=ip)
                account.save()
                return True
            return False


class Transaction(models.Model):
    amount = models.PositiveIntegerField()
    is_deposit = models.BooleanField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")

    ip = models.CharField(max_length=50, default=0)


@receiver(pre_save, sender=Transaction)
def transaction_balance_check(sender, instance, *args, **kwargs):
    # raise Exception("hey fuck you")
    print("___________________________________________________________")
    if not instance.is_deposit:
        with transaction.atomic():
            account = Account.objects.select_for_update().get(pk=instance.account.pk)

            balance = account.balance

            print("Balance: " + str(balance), "Amount: " + str(instance.amount))

            if balance >= instance.amount:
                account.parity -= instance.amount
                account.save()
            else:
                raise Exception("Under Balance")


@receiver(post_delete, sender=Transaction)
def transaction_pre_save(sender, instance, **kwargs):
    if not instance.is_deposit:
        with transaction.atomic():
            account = Account.objects.select_for_update().get(pk=instance.account.pk)

            if instance.is_deposit:
                account.parity -= instance.amount
            else:
                account.parity += instance.amount

            account.save()


