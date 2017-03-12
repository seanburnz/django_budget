from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from csv import DictReader
from decimal import Decimal
import datetime


# Create your models here.
class Institution(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    name = models.CharField(max_length=50, unique=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class BudgetCategory(models.Model):
    class Meta:
        verbose_name = "budget category"
        verbose_name_plural = "budget categories"
    category = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category


class MintCategory(models.Model):
    class Meta:
        verbose_name_plural = "mint categories"
    mint_category = models.CharField(max_length=50, unique=True)
    budget_category = models.ForeignKey(BudgetCategory, on_delete=models.SET_NULL, null=True)
    buffer_fund = models.BooleanField(default=False)

    def __str__(self):
        return self.mint_category

    @classmethod
    def import_categories(cls, categoryfile):
        with open(categoryfile) as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                mint_category = row["Mint Category"]
                try:
                    budget_category = BudgetCategory.objects.get(category=row["Budget Category"])
                except BudgetCategory.DoesNotExist:
                    budget_category = BudgetCategory(category=row["Budget Category"])
                    budget_category.save()

                entry = MintCategory(
                    mint_category=mint_category,
                    budget_category=budget_category,
                )
                entry.save()

class Transaction(models.Model):
    CREDIT = 'CR'
    DEBIT = 'DB'
    TRANSACTION_TYPE_CHOICES = (
        (CREDIT, 'credit'),
        (DEBIT, 'debit'),
    )
    trans_date = models.DateField
    description = models.CharField(max_length=200, blank=True)
    original_description = models.CharField(max_length=200, blank=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    transaction_type = models.CharField(
        max_length=2,
        choices=TRANSACTION_TYPE_CHOICES,
    )
    category = models.ForeignKey(MintCategory, on_delete=models.SET_NULL, null=True, blank=True)
    account_name = models.ForeignKey(Account, on_delete=models.CASCADE)
    labels = models.CharField(max_length=200, blank=True)
    notes = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.description

    @classmethod
    def mint_csv_import(cls, mint_csv_file, append=False):
        with open(mint_csv_file) as csvfile:
            reader = DictReader(csvfile) #, delimiter=',', quotechar='"')

            if not append: Transaction.objects.all().delete()

            # "Date","Description","Original Description","Amount","Transaction Type","Category","Account Name","Labels","Notes"
            for row in reader:
                dt = [int(n) for n in row['Date'].split('/')]
                trans_date = datetime.date(dt[2],dt[0],dt[1])  # Mint 'Date' format m/d/y
                transaction_type = ''
                for choice in Transaction.TRANSACTION_TYPE_CHOICES:
                    if row['Transaction Type'] == choice[1]: transaction_type = choice[0]
                amount = Decimal(row['Amount'])
                try:
                    category = MintCategory.objects.get(mint_category=row['Category'])
                except ObjectDoesNotExist:
                    budget_category = BudgetCategory(category=row['Category'])
                    budget_category.save()
                    category = MintCategory(mint_category=row['Category'], budget_category=budget_category)
                    category.save()
                try:
                    account_name = Account.objects.get(name=row['Account Name'])
                except ObjectDoesNotExist:
                    account_name = Account(name=row['Account Name'])
                    account_name.save()

                entry = Transaction()
                entry.trans_date = trans_date
                entry.description = row['Description']
                entry.original_description = row['Original Description']
                entry.amount = amount
                entry.transaction_type = transaction_type
                entry.category = category
                entry.account_name = account_name
                entry.labels = row['Labels']
                entry.notes = row['Notes']
                entry.save()
