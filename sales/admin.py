from django.contrib import admin
from .models import Quotation, ItemRow,Sales

class ItemRowInline(admin.TabularInline):
    model = ItemRow
    extra = 1

class QuotationAdmin(admin.ModelAdmin):
    inlines = [ItemRowInline]

admin.site.register(Quotation, QuotationAdmin)



class salesAdmin(admin.ModelAdmin):
    inlines = [ItemRowInline]

admin.site.register(Sales, salesAdmin)


