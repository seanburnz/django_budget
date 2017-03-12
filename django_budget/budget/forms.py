from django import forms
from .models import Transaction


class UploadTransactionsForm(forms.Form):
    title = forms.CharField(max_length=200)
    file = forms.FileField()

    def upload_transactions(self):
        Transaction.mint_csv_import()
