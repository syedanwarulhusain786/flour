from django import forms
from .models import Ledger

from django import forms
from .models import JournalEntry, JournalEntryRow
# forms.py
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from login.models import CustomUser
class CustomPasswordChangeForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
         # Check if the 'old_password' field exists before trying to delete it
        if 'old_password' in self.fields:
            del self.fields['old_password']
class LedgerForm(forms.ModelForm):
    class Meta:
        model = Ledger
        fields = '__all__'
class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = '__all__'  # Include all fields from the model


# forms.py
