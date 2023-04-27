from djmoney.models.fields import CURRENCY_CHOICES
from rest_framework.views import APIView
from rest_framework.response import Response

class CurrencyListView(APIView):
    def get(self, request):
        return Response(CURRENCY_CHOICES)
