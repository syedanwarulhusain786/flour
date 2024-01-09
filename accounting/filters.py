import django_filters
from .models import JournalEntryRow,Ledger,Group
class JournalEntryFilter(django_filters.FilterSet):
    primary_group = django_filters.ModelChoiceFilter(
        field_name='rows__ledger__group__primary_group',
        queryset=Group.objects.all(),
        label='Primary Group'
    )

    group = django_filters.ModelChoiceFilter(
        field_name='rows__ledger__group',
        queryset=Group.objects.all(),
        label='Group'
    )

    ledger = django_filters.ModelChoiceFilter(
        field_name='rows__ledger',
        queryset=Ledger.objects.all(),
        label='Ledger'
    )

    class Meta:
        model = JournalEntryRow
        fields = [
            'entryFk',
            'ledger',
            'comment',
            'debit',
            'credit',
            
        ]
        

import django_filters
from .models import LedgerEntry

class LedgerEntryFilter(django_filters.FilterSet):
    date_range = django_filters.DateFromToRangeFilter(
        field_name='date',
        widget=django_filters.widgets.RangeWidget(attrs={'type': 'date', 'class': 'form-control'}),
        label='Date Range'
    )

    class Meta:
        model = LedgerEntry
        fields = ['date_range']