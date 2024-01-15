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
    path('', views.index, name='login'),
    path('log/', views.logou, name='logout'),
    path('create/', views.create_billing_company, name='create_billing_company'),
    path('list/', views.billing_company_list_view, name='billing_company_list'),
    path('<int:pk>/update/', views.billing_company_update_view, name='update_billing_company'),
    path('<int:pk>/delete/', views.billing_company_delete_view, name='delete_billing_company'),
    
]
