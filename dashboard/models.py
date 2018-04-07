from django.contrib.auth.models import AbstractUser
from django.db import models


class Product(models.Model):
    amount = models.IntegerField()
    name = models.CharField(max_length=128)
    total_local = models.IntegerField()
    total_usd = models.IntegerField()


class Sale(models.Model):
    date = models.DateField()
    products = models.ForeignKey(Product, on_delete=None)


class Store(models.Model):
    cod = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    sales = models.ForeignKey(Sale, on_delete=None)


class User(AbstractUser):
    purchases = models.ForeignKey(Sale, on_delete=None, null=True, blank=True)




