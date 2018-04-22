from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('currency/<slug:currency>/', views.DashboardView.as_view(), name='dashboard'),
    path('sales/', views.SalesByMonthView.as_view(), name='sales'),
    path('products/', views.SalesByProductView.as_view(), name='products'),
    path('load-data/', views.LoadDataView.as_view(), name='load-data'),
]