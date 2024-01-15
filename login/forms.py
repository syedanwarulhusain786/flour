# forms.py
from django import forms
from .models import Billing_Company

# forms.py
from django import forms
from .models import Billing_Company

class BillingCompanyForm(forms.ModelForm):
    class Meta:
        model = Billing_Company
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }
