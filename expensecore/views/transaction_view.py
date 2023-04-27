from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
import json,csv
import requests
import requests
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from expensecore.models import Transaction, Account
from expensecore.serializers.transaction_serializer import TransactionSerializer
from django_filters import rest_framework as filters

logger = logging.getLogger(__name__)
class TransactionFilter(filters.FilterSet):
    from_date = filters.DateFilter(field_name="date", lookup_expr='gte')
    to_date = filters.DateFilter(field_name="date", lookup_expr='lte')
    tags = filters.CharFilter(method='filter_tags')
    transaction_type = filters.CharFilter(field_name="transaction_type", lookup_expr='icontains')
    accounts = filters.CharFilter(field_name="account__name", lookup_expr='icontains')
    year = filters.NumberFilter(method='filter_year')
    month = filters.NumberFilter(method='filter_month')

    def filter_tags(self, queryset, name, value):
        tags = value.split(',')
        return queryset.filter(tags__name__in=tags)

    def filter_year(self, queryset, name, value):
        if value is not None:
            queryset = queryset.filter(date__year=value)
        return queryset

    def filter_month(self, queryset, name, value):
        if value is not None:
            queryset = queryset.filter(date__month=value)
        return queryset

    class Meta:
        model = Transaction
        fields = ['from_date', 'to_date', 'tags', 'transaction_type', 'accounts', 'year', 'month']


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
