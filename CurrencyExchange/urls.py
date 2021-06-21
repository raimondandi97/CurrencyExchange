"""
Definition of urls for CurrencyExchange.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('getallsymbols', views.get_all_symbols, name='get symbols'),
    path('arhivedcurrencies', views.get_arhived_currencies, name='get symbols'),
    path('activatecurrencies', views.activate_currencies, name='activate currencies'),
    path('archivecurrency/<str:code>', views.archive_currency, name='archive currency'),
    path('saverates', views.save_rates, name='save rates'),
]
