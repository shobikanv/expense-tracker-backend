from datetime import date, timedelta
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from expensecore.models import Transaction


class ReportView(APIView):
    def get(self, request, format=None):
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        report_type = request.GET.get('type', None)
        report=None
        transactions = Transaction.objects.all()
        if year is not None:
            year = int(year)
            transactions = transactions.filter(date__year=year)
            if month is not None:
                month = int(month)
                transactions = transactions.filter(date__month=month)
                if report_type == 'daily':
                    report = self.get_daily_report(transactions, year, month)
                else:
                    report = self.get_monthly_report(transactions, year, month, report_type)
            else:
                report = self.get_yearly_report(transactions, year, report_type)
        else:
            report = {'error': 'Year is required'}
        return Response(report)

    def get_daily_report(self, transactions, year, month):
        days_in_month = (date(year, month + 1, 1) - timedelta(days=1)).day
        daily_report = {}
        for day in range(1, days_in_month + 1):
            daily_transactions = transactions.filter(date__day=day)
            daily_report[day] = self.get_report_data(daily_transactions)
        return daily_report

    def get_monthly_report(self, transactions, year, month, report_type):
        monthly_report = {}

        if report_type == 'expenses_income':
            monthly_report = self.get_expenses_income_report(transactions)

        elif report_type == 'expenses_tags':
            monthly_report = self.get_expenses_tags_report(transactions)

        elif report_type == 'net_worth':
            monthly_report = self.get_net_worth_report(transactions)

        elif report_type == 'net_income':
            monthly_report = self.get_net_income_report(transactions)

        else:
            monthly_report = {'error': 'Invalid report type'}

        return monthly_report

    def get_yearly_report(self, transactions, year, report_type):
        yearly_report = {}

        if report_type == 'expenses_income':
            yearly_report = self.get_expenses_income_report(transactions)

        elif report_type == 'expenses_tags':
            yearly_report = self.get_expenses_tags_report(transactions)

        elif report_type == 'net_worth':
            yearly_report = self.get_net_worth_report(transactions)

        elif report_type == 'net_income':
            yearly_report = self.get_net_income_report(transactions)

        else:
            yearly_report = {'error': 'Invalid report type'}

        # Get monthly report data
        for month in range(1, 13):
            month_str = str(month).zfill(2)
            month_transactions = transactions.filter(date__year=year, date__month=month)
            monthly_report = self.get_report_data(month_transactions)
            yearly_report[month_str] = monthly_report

        return yearly_report

    def get_report_data(self, transactions):
        report_data = {}
        report_data['total_expenses'] = transactions.filter(transaction_type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
        report_data['total_income'] = transactions.filter(transaction_type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
        report_data['tags'] = transactions.filter(transaction_type='EXPENSE').values_list('tags__name').annotate(total=Sum('amount')).order_by('-total')
        report_data['net_worth'] = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
        report_data['net_income'] = report_data['total_income'] - report_data['total_expenses']
        return report_data

    def get_expenses_income_report(self, transactions):
        expenses = transactions.filter(transaction_type='EXPENSE')
        incomes = transactions.filter(transaction_type='INCOME')
        report_data = {}
        report_data['total_expenses'] = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        report_data['total_income'] = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
        return report_data

    def get_expenses_tags_report(self, transactions):
        expenses = transactions.filter(transaction_type='EXPENSE')
        report_data = {}
        report_data['total_expenses'] = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        for tag in expenses.values_list('tags__name', flat=True).distinct():
            tag_expenses = expenses.filter(tags__name=tag)
            tag_data = {}
            tag_data['total_expenses'] = tag_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
            tag_data['percentage'] = round(tag_data['total_expenses'] / report_data['total_expenses'] * 100, 2)
            report_data[tag] = tag_data
        return report_data

    def get_net_worth_report(self, transactions):
        report_data = {}
        report_data['net_worth'] = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
        return report_data

    def get_net_income_report(self, transactions):
        expenses = transactions.filter(transaction_type='EXPENSE')
        incomes = transactions.filter(transaction_type='INCOME')
        report_data = {}
        income_sum = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
        expense_sum = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        report_data['net_income'] = income_sum - expense_sum
        return report_data



