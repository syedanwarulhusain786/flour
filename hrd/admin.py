from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position', 'salary', 'working_days')
    search_fields = ('first_name', 'last_name', 'position', 'pan_card')
