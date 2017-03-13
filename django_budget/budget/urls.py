# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.TransactionListView.as_view(),
        name='transaction-list'
    ),
    url(
        regex=r'^transaction/(?P<pk>[0-9]+)/$',
        view=views.TransactionDetailView.as_view(),
        name='transaction-detail'
    ),
    url(
        regex=r'^upload/$',
        view=views.upload_transactions,
        name='transaction-upload'
    ),
    url(
        regex=r'^account/$',
        view=views.AccountListView.as_view(),
        name='account-list'
    ),
    url(
        regex=r'^account/(?P<pk>[0-9]+)/$',
        view=views.AccountDetailView.as_view(),
        name='account'
    ),
]
