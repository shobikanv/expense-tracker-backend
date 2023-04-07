from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from expensecore.models import Transaction
from expensecore.serializers.transaction_serializer import TransactionSerializer
from django_filters import rest_framework as filters

class TransactionFilter(filters.FilterSet):
    from_date = filters.DateFilter(field_name="date", lookup_expr='gte')
    to_date = filters.DateFilter(field_name="date", lookup_expr='lte')
    tags = filters.CharFilter(field_name="tags__name", lookup_expr='icontains')
    transaction_type = filters.CharFilter(field_name="transaction_type", lookup_expr='icontains')

    class Meta:
        model = Transaction
        fields = ['from_date', 'to_date', 'tags', 'transaction_type']

class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = TransactionFilter
    pagination_class = PageNumberPagination

    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TransactionDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Transaction, pk=pk)

    def get(self, request, pk, format=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        transaction = self.get_object(pk)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
