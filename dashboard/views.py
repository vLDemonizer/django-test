import json

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core import serializers as sr
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView   
from django.views.generic.edit import FormView
# xlsx libraries

from dateutil.relativedelta import relativedelta
from io import BytesIO
from openpyxl import load_workbook

from rest_framework.views import APIView

from . import forms, models, serializers


class SuperuserPermission(UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_superuser


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        currency = kwargs.get('currency', None)
        start_date = models.Sale.objects.latest('date').date
        end_date = start_date + relativedelta(months=-5)# 5 because we already have 
                                                        # the start date for 6 total
        print(start_date)
        print(end_date)
        if currency:
            # Line chart by month
            context['currency'] = True
            sales_by_month = list(
            models.Sale.objects
                .annotate(month=TruncMonth('date'))
                .order_by('-date')
                .values('month')
                .annotate(sales=Sum('total_usd'))
                .values('month', 'sales')
            )[:6]
            sales_by_month = sales_by_month[::-1]
            # Pie Chart by month

            product_types = sorted(
                models.ProductType.objects.all(),
                key=lambda product_type: product_type.total_sales,
                reverse=True
            )
            top_product_types = product_types[:5] # Get the 5 with most sales
            rest_product_types = product_types[5:] # Rest
            sales_by_product = []
            for top in top_product_types:
                sales_by_product.append({
                    "product": top.name,
                    "sales": float(top.total_usd_sales)
                })  
            total = 0
            for rest in rest_product_types:
                total += rest.total_usd_sales
            total = round(total, 2)
            sales_by_product = sales_by_product + [{"product": "OTHERS", "sales": float(total)}] # Add rest

        else:
            sales_by_month = list(
                models.Sale.objects
                    .annotate(month=TruncMonth('date'))
                    .order_by('-date')
                    .values('month')
                    .annotate(sales=Sum('total_local'))
                    .values('month', 'sales')
            )[:6]
            sales_by_month = sales_by_month[::-1]

            product_types = sorted(
                models.ProductType.objects.all(),
                key=lambda product_type: product_type.total_sales,
                reverse=True
            )
            top_product_types = product_types[:5] # Get the 5 with most sales
            rest_product_types = product_types[5:] # Rest
            sales_by_product = []
            for top in top_product_types:
                sales_by_product.append({
                    "product": top.name,
                    "sales": float(top.total_local_sales)
                })  
            total = 0
            for rest in rest_product_types:
                total += rest.total_local_sales
            total = round(total, 2)
            sales_by_product = sales_by_product + [{"product": "OTHERS", "sales": float(total)}] # Add rest

        context['sales_by_month'] = json.dumps(sales_by_month, cls=DjangoJSONEncoder)
        context['sales_by_product'] = json.dumps(sales_by_product)
        return context


class SalesByMonthView(TemplateView):
    template_name = 'sales_by_month.html'

    def get_context_data(self, **kwargs):
        """
        Get sales ordered by recent date as preview view
        """
        context = super(SalesByMonthView, self).get_context_data(**kwargs)
        context['sales'] = models.Sale.objects.all().order_by('-date')[:100]
        """context['sales_json'] = json.dumps(serializers.SaleSerializer(
                context['sales'],
                many=True
            ).data
        )"""
        sales_by_month = list(
            models.Sale.objects
                .annotate(month=TruncMonth('date'))
                .order_by('-date')
                .values('month')
                .annotate(sales=Count('id'))
                .values('month', 'sales')
        )[:6]
        sales_by_month = sales_by_month[::-1] # So it goes from older to newer
        context['sales_by_month'] = json.dumps(sales_by_month, cls=DjangoJSONEncoder)
        return context


class SalesByProductView(TemplateView):
    template_name = 'sales_by_product.html'

    def get_context_data(self, **kwargs):
        """
        Get sales by product
        """
        context = super(SalesByProductView, self).get_context_data(**kwargs)
        product_types = sorted(
            models.ProductType.objects.all(),
            key=lambda product_type: product_type.total_sales,
            reverse=True
        )
        top_product_types = product_types[:5] # Get the 5 with most sales
        rest_product_types = product_types[5:] # Rest
        sales_by_product = []
        for top in top_product_types:
            sales_by_product.append({
                "product": top.name,
                "sales": top.total_sales
            })  
        total = 0
        for rest in rest_product_types:
            total += rest.total_sales
        sales_by_product = sales_by_product + [{"product": "OTHERS", "sales": total}] # Add rest
        context['product_types'] = product_types
        context['sales_by_product'] = json.dumps(sales_by_product)
        return context


class LoadDataView(SuperuserPermission, FormView):
    form_class = forms.LoadDataForm
    template_name = 'load_data.html'
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        if form.is_valid():
            file_in_memory = request.FILES.get('file').read()
            file = load_workbook(filename=BytesIO(file_in_memory))
            for sheet in file:
                itersheet = iter(sheet)
                # Skip the column name row
                next(itersheet)
                for row in itersheet:
                    # Store
                    store, store_created = models.Store.objects.get_or_create(cod=row[0].value)
                    if store_created:
                        store.name = 'Store-{0}'.format(row[0].value)
                        store.save()            
                    # Client
                    client, client_created = models.User.objects.get_or_create(
                        username=row[1].value, 
                        password=1234567,
                        cod=row[1].value
                    )
                    # Product Type
                    product_type, product_type_created = models.ProductType.objects.get_or_create(
                        name=row[3].value
                    )
                    # Sale
                    total_local = float(row[6].value)
                    sale = models.Sale.objects.create(
                        product_type=product_type,
                        amount=float(row[5].value),
                        total_local=total_local,
                        total_usd=total_local / 3.25,
                        date=row[4].value,
                        client=client,
                        store=store
                    )     
            return self.form_valid(form)

        return self.form_invalid(form)