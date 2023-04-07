from enum import Enum
from django.db import models
from djmoney.models.fields import MoneyField


class AccountGroup(str, Enum):
    CASH = "Cash"
    BANK_ACCOUNT = "Bank Account"
    DEPOSIT = "Deposit"
    CREDIT = "Credit"
    ASSET = "Asset"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class TransactionType(str, Enum):
    INCOME = "Income"
    EXPENSE = "Expense"
    TRANSFER = "Transfer"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Account(models.Model):
    name = models.CharField(max_length=255)
    group = models.CharField(
        max_length=255,
        choices=AccountGroup.choices(),
        blank=False
    )
    balance = MoneyField(
        max_digits=14, decimal_places=2,
        default_currency='USD',
        default=0,
    )


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=255,
        choices=TransactionType.choices(),
        blank=False
    )
    amount = MoneyField(
        max_digits=14, decimal_places=2,
        default_currency='USD',
        default=0,
    )

    date = models.DateField()
    flag = models.BooleanField(default=False)
    tags = models.ManyToManyField("Tag", blank=True)
    note = models.TextField(blank=True)



class Tag(models.Model):
    name = models.CharField(max_length=255)
