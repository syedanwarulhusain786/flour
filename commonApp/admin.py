# admin.py
from django.contrib import admin
from .models import Material, ProductCategory, Product,DeliveryDetails, ServiceCategory, Service,ProductBrand,ProductMaterial,Order,ProductStock

class ProductDetailsAdmin(admin.ModelAdmin):
    list_display = ('name', 'productCost', 'productSelling', 'category')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)
    ordering = ('name',)
    # readonly_fields = ('image0', 'image1', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7', 'image8', 'image9')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_of_measurement','unit_cost')
    search_fields = ('name',)
    list_filter = ('unit_of_measurement',)

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'Qty', 'costing')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)
    ordering = ('name',)

admin.site.register(Product, ProductDetailsAdmin)


class ProductMaterialAdmin(admin.ModelAdmin):
    list_display = ('product','quantity_per_piece')
    search_fields = ('product__name', 'material__name')  # Add fields you want to search by

admin.site.register(ProductMaterial, ProductMaterialAdmin)
admin.site.register(Order)
admin.site.register(DeliveryDetails)
admin.site.register(ProductStock)



    
