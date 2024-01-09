from django import forms
from .models import Ledger

from django import forms
from .models import JournalEntry, JournalEntryRow
class LedgerForm(forms.ModelForm):
    class Meta:
        model = Ledger
        fields = '__all__'
class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = '__all__'  # Include all fields from the model


# forms.py
