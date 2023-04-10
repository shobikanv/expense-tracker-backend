from enum import Enum

from django.core.exceptions import ValidationError
from django.db import models
from djmoney.models.fields import MoneyField
import logging

logger = logging.getLogger(__name__)

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
        default_currency='INR',
        default=0,
    )


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    destination_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='destination_transactions', null=True, blank=True)
    transaction_type = models.CharField(
        max_length=255,
        choices=TransactionType.choices(),
        blank=False
    )
    amount = MoneyField(
        max_digits=14, decimal_places=2,
        default_currency='INR',
        default=0,
    )

    date = models.DateField()
    flag = models.BooleanField(default=False)
    tags = models.ManyToManyField("Tag", blank=True)
    note = models.TextField(blank=True)


    def save(self, *args, **kwargs):
        try:
            # Call the super method to save the instance to the database
            super().save(*args, **kwargs)

            # Get the corresponding account instance
            account = self.account

            # Update the balance based on the transaction type
            if self.transaction_type == TransactionType.INCOME.name:
                account.balance += self.amount
            elif self.transaction_type == TransactionType.EXPENSE.name:
                account.balance -= self.amount
            elif self.transaction_type == TransactionType.TRANSFER.name:
                if self.destination_account is None:
                    raise ValueError("Destination account must be specified for transfer transactions")
                if self.destination_account == account:
                    raise ValidationError("Cannot transfer to the same account")
                if account.balance < self.amount:
                    raise ValueError("Not enough balance to make the transfer")
                account.balance -= self.amount
                self.destination_account.balance += self.amount
                self.destination_account.save()

            # Save the updated account instance


            account.save()
            logger.info(f"Account balance updated successfully. New balance: {account.balance}")
        except Exception as e:
            logger.error(f"Error updating account balance: {e}")
            raise

class Tag(models.Model):
    name = models.CharField(max_length=255)
