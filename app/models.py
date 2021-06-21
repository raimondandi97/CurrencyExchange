"""
Definition of models.
"""

from django.db import models

# Create your models here.


class Currency(models.Model):
    
    name = models.CharField(max_length=30, default='')
    symbol = models.CharField(max_length=10, default='')
    abv = models.CharField(max_length=10, default='')
    active = models.BooleanField(default=False)
    country_code = models.CharField(max_length=10, default='')
    flag_link = models.CharField(max_length=100, default='')
    rate = models.FloatField(default=1)