from __future__ import absolute_import, unicode_literals

from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, FormView
from .forms import UploadTransactionsForm

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Transaction, Account
from .forms import UploadTransactionsForm


# Create your views here.
class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction


class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction


class TransactionImportView(LoginRequiredMixin, FormView):
    model = Transaction
    template_name = 'transaction_upload.html'
    form_class = UploadTransactionsForm
    success_url = '/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return HttpResponseRedirect('transaction-list')


def upload_transactions(request):
    if request.method == 'POST':
        form = UploadTransactionsForm(request.POST, request.FILES)
        if form.is_valid():
            Transaction.mint_csv_import(request.FILES['file'])
            return HttpResponseRedirect('transaction-list')
    else:
        form = UploadTransactionsForm()
    return render(request, 'budget/transaction_upload.html', {'form': form})


class AccountListView(LoginRequiredMixin, ListView):
    model = Account


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
