from django.db.models.signals import post_save
from django.dispatch import receiver
from expensecore.models import Transaction

@receiver(post_save, sender=Transaction)
def update_account_balance(sender, instance, **kwargs):
    if instance.transaction_type == 'INCOME':
        instance.Account.balance += instance.amount
        instance.Account.save()
    elif instance.transaction_type == 'EXPENSE':
        instance.Account.balance -= instance.amount
        instance.Account.save()
    elif instance.transaction_type == 'TRANSFER':
        instance.Account.balance -= instance.amount
        instance.Account.save()
        if instance.destination_account:
            instance.destination_account.balance += instance.amount
            instance.destination_account.save()
