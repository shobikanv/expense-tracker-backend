from django.urls import path
from expensecore.views.account_view import AccountList, AccountDetail
from expensecore.views.currency_choices import CurrencyListView
from expensecore.views.reports_view import ReportView
from expensecore.views.tags_view import TagList
from expensecore.views.transaction_view import TransactionList, TransactionDetail
from expensecore.views.transactions_import_view import TransactionImport

urlpatterns = [
    path('accounts/', AccountList.as_view(),name='account-list-create'),
    path('accounts/<int:pk>/', AccountDetail.as_view(),name='account-retrieve-update-destroy'),
    path('transactions/', TransactionList.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', TransactionDetail.as_view(),
         name='transaction-retrieve-update-destroy'),
    path('transactions/import/', TransactionImport.as_view(), name='transaction-import'),
    path('tags/', TagList.as_view()),
    path('currencies/',CurrencyListView.as_view()),
    path('reports/', ReportView.as_view(), name='reports'),
]
