from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    cod = models.CharField(max_length=32, unique=True)


class Store(models.Model):
    cod = models.CharField(max_length=32)
    name = models.CharField(max_length=64, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=None, null=True)

    def __str__(self):
        return '{0}, Owner {1}'.format(self.name, self.owner)


class ProductType(models.Model):
    name = models.CharField(max_length=128)

    @property
    def total_local_sales(self):
        total = 0
        for sale in self.sale_set.all():
            total += sale.total_local
        return round(total, 2)
    
    @property
    def total_usd_sales(self):
        return round(float(self.total_local_sales) / 3.25, 2) 
    
    @property
    def total_sales(self):
        return self.sale_set.count()

    @property
    def sales_range(self, start, end):
        return self.sale_set.filter(date__range=[start, end])

    def __str__(self):
        return 'Name - {0} - ID - {1}'.format(self.name, self.pk)


class Sale(models.Model):
    amount = models.IntegerField()
    client = models.ForeignKey(User, on_delete=None, null=True)
    date = models.DateField()
    product_type = models.ForeignKey(ProductType, on_delete=None, null=True)
    total_local = models.DecimalField(max_digits=13, decimal_places=2)
    total_usd = models.DecimalField(max_digits=13, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=None, null=True)

    def __str__(self):
        return 'Sale - {0} - {3}, local {1} - usd {2}'.format(
            self.pk, self.total_local, self.total_usd, self.store
        )