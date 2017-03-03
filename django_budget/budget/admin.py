from django.contrib import admin

# Register your models here.
from .models import Institution, Account, BudgetCategory, MintCategory, Transaction

admin.site.register(Institution)
admin.site.register(Account)
admin.site.register(BudgetCategory)
admin.site.register(MintCategory)
admin.site.register(Transaction)
