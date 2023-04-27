import csv
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from expensecore.models import Transaction, Account
from expensecore.serializers.transaction_serializer import TransactionSerializer

class TransactionImport(APIView):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, format=None):
        csv_file = request.FILES.get('file')
        if not csv_file:
            return HttpResponseBadRequest('CSV file is required')

        # Parse the CSV file
        try:
            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
        except csv.Error as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Create transactions from the CSV data
        transactions = []
        for row in reader:
            account_name = row.get('Account')
            transaction_type = row.get('Type')
            amount = row.get('Amount')
            date = row.get('Date')
            note = row.get('Note')
            tags = row.get('Tags')

            if not all([account_name, transaction_type, amount, date]):
                continue

            account = Account.objects.filter(name=account_name).first()
            if not account:
                continue

            tags = [tag.strip() for tag in tags.split(',')] if tags else []
            transaction = Transaction(
                account=account,
                transaction_type=transaction_type,
                amount=amount,
                date=date,
                note=note,
            )
            transactions.append(transaction)

        # Bulk create the transactions to improve performance
        Transaction.objects.bulk_create(transactions)

        return Response({'message': f'{len(transactions)} transactions created'}, status=status.HTTP_201_CREATED)
