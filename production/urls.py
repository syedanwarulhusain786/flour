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
    path('daily-report/', views.production_report, name='production_report'),
    path('orderstatus/', views.orders, name='orderstatus'),
    path('pendingOrder/', views.pendingOrder, name='pendingOrder'),
    path('produced/<int:quotation_number>/', views.producedProduct, name='producedproduction'),
     path('send_to_inventory/<int:quotation_number>/',  views.send_to_inventory, name='send_to_inventory'),
     path('delete_produced/<int:quotation_number>/', views.delete_produced, name='delete_produced'),
    
    path('in-production/', views.orders, name='in-production'),
    path('startproduction/', views.Startproduction, name='startproduction'),
    # path('startproduction/', views.Startproduction, name='startproduction'),
    path('allocateproduction/<int:quotation_number>/', views.allocateproduction, name='allocateproduction'),
     path('delete_production/<int:quotation_number>/', views.delete_production, name='delete_production'),
     
     path('send_for_production/<int:quotation_number>/',  views.send_for_production, name='send_for_production'),
]
