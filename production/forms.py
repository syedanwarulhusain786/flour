# forms.py
from sales.models import *
from accounting.models import *
from django import forms
from .models import ProductionRow,ProducedRow

class ProductionRowForm(forms.ModelForm):
    class Meta:
        model = ProductionRow
        fields = ['product',  'package', 'packageQuantity', 'quantityPerPackage','TotalQuantity','TotalCost']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.exclude(category__name='Packaging')
        # Filter products by category 'packaging'
        packaging_products = Product.objects.filter(category=ProductCategory.objects.get(name='Packaging'))
        # Update the queryset for the 'product' field
        self.fields['package'].queryset = packaging_products

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class PostProductionRowForm(forms.ModelForm):
    class Meta:
        model = ProducedRow
        fields = ['product',  'package', 'packageQuantity', 'quantityPerPackage','TotalQuantity','TotalCost']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.exclude(category__name='Packaging')
        # Filter products by category 'packaging'
        packaging_products = Product.objects.filter(category=ProductCategory.objects.get(name='Packaging'))
        # Update the queryset for the 'product' field
        self.fields['package'].queryset = packaging_products

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})