
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
from django.urls import path
from accounting.consumers import PurchaseQuotationConsumer
urlpatterns = [
    path('supplier-home/', views.supplier_home, name='supplier-home'),
    path('all-orders/', views.supplier_home, name='myorders'),
    path('suppliercompleted/', views.suppliercompleted, name='suppliercompleted'),
    path('startdelivery/<int:order_id>/<str:flag>', views.startdelivery, name='startdelivery'),
    
    path('createorder/', views.purchase_order_page, name='createorder'),
    #  path('purchase_quotations/<int:quotation_number>/place_bid/', views.place_bid, name='place_bid'),
    
    path('mybids/', views.mybids, name='mybids'),
    path('bidwon/', views.bidwon, name='bidwon'),
    path('purchase_quotations/<int:quotation_number>/', views.purchase_quotation_detail, name='purchase_quotation_detail'),
    #  path('purchase_quotations/<int:quotation_number>/place_bid/', views.place_bid, name='place_bid'),
    path('approved/', views.supplierapproved, name='supplierapproved'),
    path('disapproved/', views.supplierdisapproved, name='supplierdisapproved'),
    path('pending/', views.supplierpending, name='supplierpending'),
    
    
    
    
    # path('ws/purchase_orders/', PurchaseQuotationConsumer.as_asgi()),
    
    # path('product/', views.products, name='products'),
    
    # path('sales/', views.create_sales, name='sales'),
    # path('sales_list/', views.sales_list, name='sales_list'),
    
    # path('create_quotation/', views.create_quotation, name='create_quotation'),
    # path('quote-list/', views.quoteOrderList, name='quotelist'),
    
    # path('get_next_sales_voucher_number/', views.get_next_sales_voucher_number, name="get_next_sales_voucher_number"),
    
    # path('productDetail/<int:product_id>/', views.productDetail, name='productDetail'),

    
]
