from django import forms
from .models import Quotation, ItemRow

class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = '__all__'

class ItemRowForm(forms.ModelForm):
    class Meta:
        model = ItemRow
        fields = '__all__'
