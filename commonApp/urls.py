"""
URL configuration for erp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('force/<int:my_id>/', views.force, name='force'),
    path('add_product_stock/', views.add_product_stock, name='add_product_stock'),
    path('acceptedsales_list/', views.acceptedsales_list, name='acceptedsales_list'),
    path('allocate/<int:sales_id>/', views.allocate, name='allocate'),
    path('start_production/<str:sales_id>/', views.start_production, name='start_production'),
    path('stock_report/', views.stock_report, name='stock_report'),
    path('create_material_stock/',  views.create_material_stock, name='create_material_stock'),
    path('create_product_stock/',  views.create_product_stock, name='create_product_stock'),
    path('add_material_stock/<int:material_id>/',  views.add_material_stock, name='add_material_stock'),
    path('add_product_stock/<int:product_id>/',  views.add_product_stock, name='add_product_stock'),
    
    path('material_stock_list/', views.material_stock_list, name='material_stock_list'),
    path('product_stock_list/', views.product_stock_list, name='product_stock_list'),

    
    
    
    
    path('inventory/', views.inventory, name='inventory'),
    path('material_list/',  views.material_list, name='material_list'),
    path('create_material/',  views.create_material, name='create_material'),
    path('delete_material/<int:material_id>/',  views.delete_material, name='delete_material'),
    
    
    #################################################Products Urls ##########################
    
    
    path('products/', views.ProductListView, name='product_list'),
    # path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', views.product_form, name='product_create'),
    path('products/<int:pk>/update/', views.product_update_form , name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    ######################product material###########
    path('product-materials/', views.productMaterials, name='product-materials'),
    path('product-materials/create/', views.productMaterials_form, name='product_materials_create'),
    path('product-materials/<int:pk>/update/', views.productMaterials_update_form , name='product_materials_update'),
    path('product-materials/<int:pk>/delete/', views.productMaterials_delete, name='product_materials_delete'),
    
    
    
    #################################################Services Url ##########################
    
    
    path('services/', views.list_services, name='list_services'),
    path('services/add/', views.add_service, name='add_service'),
    path('services/edit/<int:service_id>/', views.edit_service, name='edit_service'),
    path('services/delete/<int:service_id>/', views.delete_service, name='delete_service'),
    
    
    
    
    
    
    
    
    #################################################brand and Category Urls##########################
    
    #################################################brand ##########################
    
    path('brands-category/', views.brand_category, name='brand_category'),
    path('brands/add/', views.add_brands, name='add_brands'),
    path('brands/edit/<int:service_id>/', views.edit_brands, name='edit_brands'),
    path('brands/delete/<int:service_id>/', views.delete_brands, name='delete_brands'),
    
    #################################################Category Urls##########################
    
    
    path('category/add/', views.add_category, name='add_category'),
    path('category/edit/<int:service_id>/', views.edit_category, name='edit_category'),
    path('category/delete/<int:service_id>/', views.delete_category, name='delete_category'),

]
