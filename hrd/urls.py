
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
# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('hr/', views.hr_department, name='hr_department'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('employee/<int:employee_id>/edit/',views.employee_edit, name='employee_edit'),
    path('employee/<int:employee_id>/delete/', views.employee_delete, name='employee_delete'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),

    # ... your existing URLs

    path('month-wise-attendance/', month_wise_attendance, name='month_wise_attendance'),
    
    path('upload-attendance-page/', upload_attendance_page, name='upload_attendance_page'),
   
]

