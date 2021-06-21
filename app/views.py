"""
Definition of views.
"""

from datetime import datetime, date
from django.shortcuts import render
from django.http import HttpRequest
from django.http import JsonResponse
from app.models import Currency
import requests
import base64
import json

def home(request):
    """Renders the home page.
    we do not have endpoints that return symbols and flags, we get that information from the api with the route 
    https://restcountries.eu/rest/v2/all"""
    assert isinstance(request, HttpRequest)
#    all_currencies = Currency.objects.all()
#    if len(all_currencies) == 0:
#       url = 'http://api.exchangeratesapi.io/v1/' + 'symbols' + '?access_key=' + '7eede239249bf05f6b0bc8ec18351424'
#       all_currencies = requests.get(url).json()
#       for code,name in all_currencies['symbols'].items():
#           new_currency = Currency(abv=code,name=name)
#           new_currency.save()
#       all_countries = requests.get('https://restcountries.eu/rest/v2/all').json()

#       for country in all_countries:
#           for country_currency in country['currencies']:
#               currencies = Currency.objects.filter(abv=country_currency['code'])
#               for currency in currencies:
#                   flag_link = country['flag'] if country['flag'] else ''
#                   if len(country['currencies']) == 1 and country['name'] in currency.name:
#                       currency.flag_link = '/static/flag_yellow_high.jpg' if currency.abv == 'EUR' else flag_link
#                   currency.symbol = country_currency['symbol'] if country_currency['symbol'] else currency.abv
#                   currency.save()
#       empty_symbols = Currency.objects.filter(symbol='')
#       for symbol in empty_symbols:
#           symbol.symbol = symbol.abv
#           symbol.flag_link = '/static/world_flag.jpg'
#           symbol.save()
    all_currencies = Currency.objects.filter(active=True)

    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'date': date.today(),
            'data': all_currencies,
        }
    )

def get_all_symbols(request):
    all_currencies = Currency.objects.all()
    data = {
        "symbols": []
    }
    for currency in all_currencies:
        data["symbols"].append(currency.symbol)

    return JsonResponse(data)

def get_arhived_currencies(request):
    arhived_currencies = Currency.objects.filter(active=False)
    data = {
        'arhived_currencies': []
    }
    for currency in arhived_currencies:
        data['arhived_currencies'].append({
            'flag_link': currency.flag_link,
            'abv': currency.abv,
            'name': currency.name,
        })

    return JsonResponse(data)

def activate_currencies(request):
    currencies = request.body.decode('utf-8')
    currencies = json.loads(currencies)
    for currency in currencies['currencies']:
        currency_to_activate = Currency.objects.get(abv=currency)
        currency_to_activate.active = True
        currency_to_activate.save()

def archive_currency(request, code):
    currency_to_archive = Currency.objects.get(abv=code)
    currency_to_archive.active = False
    currency_to_archive.save()

def save_rates(request):
    """The free subscription plan allows us only to gate the exchange rate with the base EUR
    so we save the rate and calculate it again with the new base"""
    data = json.loads(request.body.decode('utf-8'))['data']
    print(data)
    base = data['base']
    amount = float(data['amount'])
    for code, rate in data['currencies'].items():
        currency = Currency.objects.get(abv=code)
        currency.rate = rate
        currency.save()

    base_currency = Currency.objects.get(abv=base)

    active_currencies = Currency.objects.filter(active=True)

    converted_values = {}
    for currency in active_currencies:
        currency.rate = round(currency.rate / base_currency.rate, 4)
        currency.save()
        converted_values[currency.abv] = {
            'rate': currency.rate,
            'amount': round(currency.rate * amount, 4)
        }
    return JsonResponse(converted_values)