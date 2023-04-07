from django.contrib import admin
from expensecore.models import Tag,Transaction,Account

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Tag)