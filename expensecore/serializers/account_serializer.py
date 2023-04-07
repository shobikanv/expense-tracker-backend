from rest_framework import serializers
from expensecore.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name', 'group', 'balance')
