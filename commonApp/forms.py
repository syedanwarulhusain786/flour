# forms.py
from django import forms
from .models import Material

from .models import Product

class ProductDetailsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        
        
        
        

from django import forms
from commonApp.models import Service, ServiceCategory,ProductBrand,ProductCategory

class ServiceCategoryForm(forms.ModelForm):
    class Meta:
        model = ServiceCategory
        fields = ['name']
        labels = {'name': 'Category Name'}

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'category', 'price','Qty','costing']
        labels = {
            'name': 'Service Name',
            'description': 'Description',
            'category': 'Category',
            'price': 'Price',
            'Qty': 'Qty',
            'costing': 'Costing',
        }
        
class ProductBrandForm(forms.ModelForm):
    class Meta:
        model = ProductBrand
        fields = ['name', 'description']
        labels = {
            'name': 'ProductBrand Name',
            'description': 'Description',
            
        }
        
        
class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', 'description']
        labels = {
            'name': 'ProductCategory Name',
            'description': 'Description',
           
        }
        
        
        
        
        
# forms.py

from django import forms
from .models import ProductMaterial, Material

class ProductMaterialForm(forms.ModelForm):
    # materials = forms.ModelMultipleChoiceField(
    #     queryset=Material.objects.all(),
    #     widget=forms.SelectMultiple(attrs={'class': 'form-control select2', 'data-placeholder': 'Select materials'}),
    #     required=False,
    # )

    class Meta:
        model = ProductMaterial
        fields = ['product','quantity_per_piece', 'material']
# forms.py
class ProductMaterialEditForm(forms.ModelForm):
    class Meta:
        model = ProductMaterial
        fields = ['product', 'quantity_per_piece', 'material']
        
        
from django import forms
from .models import Material

from .models import Product

from django import forms
from .models import ProductMaterial, Material

        
from django_select2.forms import ModelSelect2MultipleWidget     
        
from django import forms
from .models import Service, ServiceCategory,ProductBrand,ProductCategory
class ProductDetailsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        
        
        
        

class ServiceCategoryForm(forms.ModelForm):
    class Meta:
        model = ServiceCategory
        fields = ['name']
        labels = {'name': 'Category Name'}

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'category', 'price','Qty','costing']
        labels = {
            'name': 'Service Name',
            'description': 'Description',
            'category': 'Category',
            'price': 'Price',
            'Qty': 'Qty',
            'costing': 'Costing',
        }
        
class ProductBrandForm(forms.ModelForm):
    class Meta:
        model = ProductBrand
        fields = ['name', 'description']
        labels = {
            'name': 'ProductBrand Name',
            'description': 'Description',
            
        }
        
        
class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', 'description']
        labels = {
            'name': 'ProductCategory Name',
            'description': 'Description',
           
        }
        
        
        
        
        
# forms.py

class ProductMaterialForm(forms.ModelForm):
    # materials = forms.ModelMultipleChoiceField(
    #     queryset=Material.objects.all(),
    #     widget=forms.SelectMultiple(attrs={'class': 'form-control select2', 'data-placeholder': 'Select materials'}),
    #     required=False,
    # )

    class Meta:
        model = ProductMaterial
        fields = ['product','quantity_per_piece', 'material']
# forms.py
class ProductMaterialEditForm(forms.ModelForm):
    class Meta:
        model = ProductMaterial
        fields = ['product', 'quantity_per_piece', 'material']

class ProductMaterialForm(forms.ModelForm):
    class Meta:
        model = ProductMaterial
        fields = ['product', 'material', 'quantity_per_piece']

    widgets = {
        'product': ModelSelect2MultipleWidget(
            model=Product,
            search_fields=['name__icontains'],
            attrs={'class': 'form-control select2'}
        ),
        'material': ModelSelect2MultipleWidget(
            model=Material,
            search_fields=['name__icontains'],
            attrs={'class': 'form-control select2'}
        ),
        'quantity_per_piece': forms.NumberInput(attrs={'class': 'form-control'}),
    }

            
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'productCost', 'productSelling', 'category', 'brand', 'image0', 'image1', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7', 'image8', 'image9']

    materials = forms.inlineformset_factory(Product, ProductMaterial, form=ProductMaterialForm, extra=1)
    

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'description', 'unit_of_measurement', 'unit_cost']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'unit_of_measurement': forms.Select(attrs={'class': 'form-control'}),
            'unit_cost': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    

class MaterialListForm(forms.Form):
    # You can add any filters or search fields you need for listing materials
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search'}))
    
from django import forms
from .models import MaterialStock, ProductStock

class MaterialStockForm(forms.ModelForm):
    class Meta:
        model = MaterialStock
        fields = ['material', 'quantity', 'cost_of_single']

    def __init__(self, *args, **kwargs):
        super(MaterialStockForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ProductStockForm(forms.ModelForm):
    class Meta:
        model = ProductStock
        fields = ['product', 'quantity', 'cost_of_single']

    def __init__(self, *args, **kwargs):
        super(ProductStockForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class AddMaterialStockForm(forms.ModelForm):
    class Meta:
        model = MaterialStock
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        super(AddMaterialStockForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class AddProductStockForm(forms.ModelForm):
    class Meta:
        model = ProductStock
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        super(AddProductStockForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'






class ProductStockForm(forms.ModelForm):
    class Meta:
        model = ProductStock
        fields = ['type', 'product', 'quantity', 'cost_of_single']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the form as needed, e.g., set additional attributes or widgets
        packaging_products = Product.objects.filter(category=ProductCategory.objects.get(name='Packaging'))
        # Update the queryset for the 'product' field
        self.fields['product'].queryset = packaging_products
        self.fields['type'].widget.choices = [
            ('purchase', 'Purchase'),
            ('return', 'Return'),
        ]
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
    def clean(self):
        cleaned_data = super().clean()
        # Add any custom validation logic here if needed
        return cleaned_data