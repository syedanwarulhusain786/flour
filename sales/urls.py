
"""
URL configuration for erp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('sales-home/', views.home, name='sales-home'),
    path('product/', views.products, name='products'),
    
    path('sales/', views.create_sales, name='sales'),
    path('sales_list/', views.sales_list, name='sales_list'),
    
    path('create_quotation/', views.create_quotation, name='create_quotation'),
    path('quote-list/', views.quoteOrderList, name='quotelist'),
    
    path('get_next_sales_voucher_number/', views.get_next_sales_voucher_number, name="get_next_sales_voucher_number"),
    
    path('productDetail/<int:product_id>/', views.productDetail, name='productDetail'),

    
]
