from django.http import HttpResponse
from django.contrib import admin
import csv
from .models import (
    Primary_Group,
    Group,
    Ledger,
    Customer,
    Supplier,
    PurchaseQuotation,
    PurchaseItemRow,
    JournalEntry,
    JournalEntryRow,
    PaymentEntry,
    ContraEntry,
    ContraEntryRow,
    SalesEntry,
    SalesEntryRow,
    PurchaseEntry,
    PurchaseEntryRow,
    CreditNoteEntry,
    creditNoteEntryRow,
    DebitNoteEntry,
    DebitNoteEntryRow,
    VoucherLedgerVisibility,
    RecieptEntry,
    Tax,SalesDeliveryDetails,SalesItemRow,SalesQuotation,LedgerEntry
)
def download_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)

    # Get model fields dynamically
    fields = [field.name for field in modeladmin.model._meta.fields]

    # Write headers
    writer.writerow(fields)

    # Write data to the CSV
    for obj in queryset:
        row = [getattr(obj, field) for field in fields]
        writer.writerow(row)

    return response
download_csv.short_description = "Download selected items as CSV"
class GroupInline(admin.TabularInline):
    model = Group

class LedgerInline(admin.TabularInline):
    model = Ledger

class PurchaseItemRowInline(admin.TabularInline):
    model = PurchaseItemRow

class PurchaseQuotationAdmin(admin.ModelAdmin):
    inlines = [PurchaseItemRowInline]
    actions = [download_csv]

class JournalEntryRowInline(admin.TabularInline):
    model = JournalEntryRow
class JournalEntryAdmin(admin.ModelAdmin):
    inlines = [JournalEntryRowInline]
    actions = [download_csv]






class ContraEntryRowInline(admin.TabularInline):
    model = ContraEntryRow
    actions = [download_csv]

class ContraEntryAdmin(admin.ModelAdmin):
    inlines = [ContraEntryRowInline]

class SalesEntryRowInline(admin.TabularInline):
    model = SalesEntryRow
    actions = [download_csv]

class SalesEntryAdmin(admin.ModelAdmin):
    inlines = [SalesEntryRowInline]

class PurchaseEntryRowInline(admin.TabularInline):
    model = PurchaseEntryRow
    actions = [download_csv]

class PurchaseEntryAdmin(admin.ModelAdmin):
    inlines = [PurchaseEntryRowInline]

class CreditNoteEntryRowInline(admin.TabularInline):
    model = creditNoteEntryRow
    actions = [download_csv]

class CreditNoteEntryAdmin(admin.ModelAdmin):
    inlines = [CreditNoteEntryRowInline]

class DebitNoteEntryRowInline(admin.TabularInline):
    model = DebitNoteEntryRow
    actions = [download_csv]

class DebitNoteEntryAdmin(admin.ModelAdmin):
    inlines = [DebitNoteEntryRowInline]

# # Register your models with the admin site
admin.site.register(Primary_Group)
admin.site.register(VoucherLedgerVisibility)
admin.site.register(Tax)


admin.site.register(Group)
admin.site.register(SalesQuotation)

admin.site.register(SalesItemRow)

admin.site.register(SalesDeliveryDetails)

admin.site.register(RecieptEntry)
admin.site.register(Ledger)
admin.site.register(LedgerEntry)
admin.site.register(PaymentEntry)

admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(PurchaseQuotation, PurchaseQuotationAdmin)
admin.site.register(JournalEntry, JournalEntryAdmin)
admin.site.register(ContraEntry, ContraEntryAdmin)
admin.site.register(SalesEntry, SalesEntryAdmin)
admin.site.register(PurchaseEntry, PurchaseEntryAdmin)
admin.site.register(CreditNoteEntry, CreditNoteEntryAdmin)
admin.site.register(DebitNoteEntry, DebitNoteEntryAdmin)

