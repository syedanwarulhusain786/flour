from django.db import models

# Create your models here.
from sales.models import *
from accounting.models import *


class ProductionRow(models.Model):
    ROW_TYPE_CHOICES = [
    ('Raw', 'Raw'),
    ('Package', 'Package'),
    ]
    
    sales_order = models.ForeignKey(SalesQuotation, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='sale_product', on_delete=models.CASCADE)
    row_type = models.CharField(max_length=20, choices=ROW_TYPE_CHOICES)
    package = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    packageQuantity = models.PositiveIntegerField(default=0)
    quantityPerPackage = models.PositiveIntegerField(default=0)
    TotalQuantity = models.PositiveIntegerField()
    TotalCost =  models.DecimalField(max_digits=50, decimal_places=2)
    
    production_date = models.DateField(auto_now_add=True)
    
    

    def save(self, *args, **kwargs):
        # Calculate total price before saving the ProductionRow
        super().save(*args, **kwargs)
class ProducedRow(models.Model):
    ROW_TYPE_CHOICES = [
    ('Raw', 'Raw'),
    ('Package', 'Package'),
    ]
    sales_order = models.ForeignKey(SalesQuotation, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='post_product', on_delete=models.CASCADE)
    row_type = models.CharField(max_length=20, choices=ROW_TYPE_CHOICES)
    package = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    packageQuantity = models.PositiveIntegerField(default=0)
    quantityPerPackage = models.PositiveIntegerField(default=0)
    TotalQuantity = models.PositiveIntegerField()
    TotalCost =  models.DecimalField(max_digits=50, decimal_places=2)
    
    production_date = models.DateField(auto_now_add=True)
    production_time = models.TimeField(auto_now_add=True)
    
    

    def save(self, *args, **kwargs):
        # Calculate total price before saving the ProductionRow
        super().save(*args, **kwargs)
