from django.db import models


# Create your models here.
class Institution(models.Model):
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    name = models.CharField(max_length=50)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class BudgetCategory(models.Model):
    class Meta:
        verbose_name = "budget category"
        verbose_name_plural = "budget categories"
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category


class MintCategory(models.Model):
    class Meta:
        verbose_name_plural = "mint categories"
    mint_category = models.CharField(max_length=50)
    budget_category = models.ForeignKey(BudgetCategory, on_delete=models.SET_NULL, null=True)
    buffer_fund = models.BooleanField(default=False)

    def __str__(self):
        return self.mint_category


class Transaction(models.Model):
    CREDIT = 'CR'
    DEBIT = 'DB'
    TRANSACTION_TYPE_CHOICES = (
        (CREDIT, 'credit'),
        (DEBIT, 'debit'),
    )
    date = models.DateField
    description = models.CharField(max_length=200, blank=True)
    original_description = models.CharField(max_length=200, blank=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    transaction_type = models.CharField(
        max_length=2,
        choices=TRANSACTION_TYPE_CHOICES,
    )
    category = models.ForeignKey(MintCategory, on_delete=models.SET_NULL, null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    labels = models.CharField(max_length=200, blank=True)
    notes = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.description
