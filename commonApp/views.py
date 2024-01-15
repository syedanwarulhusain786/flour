from django.shortcuts import render, redirect 
# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
from django.db.models import Max
from django.db import transaction

from commonApp.models import *
from accounting.models import *
from login.models import *
# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Notification

def get_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user, read=False)
    notifications_data = [{'message': notification.message, 'timestamp': notification.timestamp} for notification in notifications]
    return JsonResponse({'notifications': notifications_data})

def mark_notifications_as_read(request):
    user = request.user
    Notification.objects.filter(user=user, read=False).update(read=True)
    return JsonResponse({'success': True})





from django.shortcuts import render
from production.models import *
from django.contrib import messages
from decimal import Decimal 
from sales.models import *
from django.shortcuts import render
from django.shortcuts import render, redirect 
# Create your views here.
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.http import JsonResponse
from django.db.models import Max
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from commonApp.models import *
from accounting.models import *
from django.db.models import Q
from login.models import *
from accounting.currency import currency_symbols
# Create your views here.
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from django.contrib.staticfiles import finders

from django.views.generic import ListView
from django.shortcuts import render, redirect


from django.contrib.auth.decorators import user_passes_test
from login.models import CustomUser    
    
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.utils.decorators import method_decorator

def department_check(user, allowed_departments):
    """
    Check if the user's department is in the allowed list.
    """
    return user.department.name in allowed_departments

def department_required(allowed_departments):
    """
    Decorator to restrict access based on the user's department.
    """
    return user_passes_test(lambda u: department_check(u, allowed_departments))

from django.shortcuts import render, redirect
from .forms import MaterialStockForm, ProductStockForm, AddMaterialStockForm, AddProductStockForm

def create_material_stock(request):
    if request.method == 'POST':
        form = MaterialStockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('material_stock_list')
    else:
        form = MaterialStockForm()

    return render(request, 'productandservices/sd\material_stock_form.html', {'form': form})

def create_product_stock(request):
    if request.method == 'POST':
        form = ProductStockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_stock_list')
    else:
        form = ProductStockForm()

    return render(request, 'productandservices/sd/product_stock_form.html', {'form': form})

def add_material_stock(request, material_id):
    material = Material.objects.get(pk=material_id)

    if request.method == 'POST':
        form = AddMaterialStockForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.material = material
            stock.save()
            return redirect('material_stock_list')
    else:
        form = AddMaterialStockForm()

    return render(request, 'productandservices/sd/add_material_stock_form.html', {'form': form, 'material': material})

def add_product_stock(request, product_id):
    product = Product.objects.get(pk=product_id)

    if request.method == 'POST':
        form = AddProductStockForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.product = product
            stock.save()
            return redirect('product_stock_list')
    else:
        form = AddProductStockForm()

    return render(request, 'productandservices/sd/add_product_stock_form.html', {'form': form, 'product': product})




def material_stock_list(request):
    material_stocks = MaterialStock.objects.all()
    return render(request, 'inventory/productandservices/sd/material_stock_list.html', {'material_stocks': material_stocks})

def product_stock_list(request):
    product_stocks = ProductStock.objects.all()
    return render(request, 'inventory/productandservices/sd/product_stock_list.html', {'product_stocks': product_stocks})
from django.db.models import F, Sum,ExpressionWrapper, DecimalField,IntegerField,Sum, ExpressionWrapper, F, PositiveIntegerField, DecimalField, Case, When, Value, IntegerField, PositiveIntegerField, Value as V
from django.db.models.functions import Cast, Coalesce
from django.core.validators import MinValueValidator

from django.db.models import Sum
def stock_report(request):
    cat = ProductCategory.objects.all()
    brand = ProductBrand.objects.all()
    product=Product.objects.all()

    sales_product_list = (
        ProductStock.objects
        .filter(product__category__name='Sales')  # Filter products of type 'sales'
        .values('product__name')
        .annotate(
            total_quantity_sales=Sum(
                Case(
                    When(type='purchase', then=F('quantity')),
                    When(type__in=['return', 'prod'], then=-F('quantity')),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ),
            total_value_sales=Sum(
                Case(
                    When(type='purchase', then=F('cost_of_all')),
                    When(type__in=['return', 'prod'], then=-F('cost_of_all')),
                    default=Value(0),
                    output_field=DecimalField()
                )
            )
        )
    )
    purchase_product_list = (
        ProductStock.objects
        .filter(product__category__name='Purchase')  # Filter products of type 'sales'
        .values('product__name')
        .annotate(
            total_quantity_sales=Sum(
                Case(
                    When(type='purchase', then=F('quantity')),
                    When(type__in=['return', 'prod'], then=-F('quantity')),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ),
            total_value_sales=Sum(
                Case(
                    When(type='purchase', then=F('cost_of_all')),
                    When(type__in=['purchase', 'prod'], then=-F('cost_of_all')),
                    default=Value(0),
                    output_field=DecimalField()
                )
            )
        )
    )
    pack_product_list = (
        ProductStock.objects
        .filter(product__category__name='Package')  # Filter products of type 'sales'
        .values('product__name')
        .annotate(
            total_quantity_sales=Sum(
                Case(
                    When(type='purchase', then=F('quantity')),
                    When(type__in=['return', 'prod'], then=-F('quantity')),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ),
            total_value_sales=Sum(
                Case(
                    When(type='purchase', then=F('cost_of_all')),
                    When(type__in=['purchase', 'prod'], then=-F('cost_of_all')),
                    default=Value(0),
                    output_field=DecimalField()
                )
            )
        )
    )


    context = {
 
        'sales_product_list': sales_product_list,
        'purchase_product_list':purchase_product_list,
        'pack_product_list':pack_product_list,
        'cat': cat,
        'brand': brand,
        'products': product,
    }


    return render(request, 'inventory/stock_report.html', context)






def force(request, my_id):
    # Your logic here
    order=Order.objects.get(id=my_id)
    order.is_approved='completed'
    order.save()
    return redirect('suppliercompleted')



@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login')
def inventory(request):
    return render(request,'inventoryHome.html')
#############products start ##################
@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login')
def ProductListView(request):
    products = Product.objects.all()

    context = {'products': products}
    return render(request, 'productandservices/products/product_list.html', context)
@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login')
def product_update_form(request, pk=None):
    name = request.POST.get('name', '')
    description = request.POST.get('description', '')
    productCost = request.POST.get('productCost', '')
    productSelling = request.POST.get('productSelling', '')
    materials = request.POST.getlist('materials', '')
    primaryCategory = request.POST.get('primaryCategory', '')
    images = request.FILES.getlist('images')
    
    product_form=Material.objects.all()
    category=ProductCategory.objects.all()
    prod=Product.objects.get(pk=pk)
    if request.method == 'POST':
        product_form = Product.objects.get(pk=pk)
        product_form.name = name 
        product_form.description =  description
        product_form.productCost =productCost
        product_form.productSelling = productSelling
        
        product_form.save()
        

        return redirect('product_list')  # Redirect to the product list view

    template_name = 'productandservices/products/product_detail.html'  # Replace with your actual template name
    context = {
        'prod':prod,
        'product_form': product_form,
        'category':category
    }
    return render(request, template_name, context)
@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login')
def product_form(request, pk=None):
    name = request.POST.get('name', '')
    description = request.POST.get('description', '')
    productCost = request.POST.get('productCost', '')
    productSelling = request.POST.get('productSelling', '')
    brandInp = request.POST.get('brand', '')
    
    materials = request.POST.getlist('materials', '')
    primaryCategory = request.POST.get('primaryCategory', '')
    images = request.FILES.getlist('images')
    selected_packaging_products = request.POST.getlist('packagingProducts[]')  # Assuming 'packagingProducts' is the name of your multiple select field
    product_form=Material.objects.all()
    category=ProductCategory.objects.all()
    brand=ProductBrand.objects.all()
    packaging_products=Product.objects.filter(category=ProductCategory.objects.get(name='Package'))
    
    if request.method == 'POST':
        cat=ProductCategory.objects.get(pk=primaryCategory)
        br=ProductBrand.objects.get(pk=brandInp)
        
        product_form = Product()
        product_form.name = name 
        product_form.description =  description
        product_form.productCost =productCost
        product_form.productSelling = productSelling
        product_form.category = cat
        product_form.brand = br
        
        
        
        # product_form.save()
        
        images = request.FILES.getlist('images')  # Assuming you have a file input field named 'images'
        # Iterate through the images and save them to the corresponding image fields
        for i, image in enumerate(images):
            setattr(product_form, f'image{i}', image)

        # Save the updated product with the new images
        product_form.save()
        for packaging_product_id in selected_packaging_products:
            packaging_product = Product.objects.get(pk=packaging_product_id)
            product_form.packaging_products.add(packaging_product)
        return redirect('product_list')  # Redirect to the product list view

    template_name = 'productandservices/products/product_form.html'  # Replace with your actual template name
    context = {
        'product_form': product_form,
        'category':category,
        'brand':brand,
        'packaging_products':packaging_products
    }
    return render(request, template_name, context)
@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login')
def product_delete(request, pk):
    # Your delete logic here
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        # Add any additional processing or redirect as needed
        return redirect('product_list')  # Redirect to the product list view

    template_name = 'productandservices/products/product_confirm_delete.html'  # Replace with your actual template name
    context = {'product': product}
    return render(request, template_name, context)



####################product finished#################

@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login')
def create_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('material_list')  # Redirect to the material list or another page
    else:
        form = MaterialForm()

    return render(request, 'materials\create_material.html', {'form': form})
@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login')
def delete_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    if request.method == 'POST':
        material.delete()
        return redirect('material_list')  # Redirect to the material list or another page

    return render(request, 'materials\delete_material.html', {'material': material})
@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login')  
def material_list(request):
    form = MaterialListForm(request.GET)
    materials = Material.objects.all()

    if form.is_valid() and form.cleaned_data['search']:
        materials = materials.filter(name__icontains=form.cleaned_data['search'])

    return render(request, 'materials\material_list.html', {'form': form, 'materials': materials})    
    
    
    
###########product Material Section############   
@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login')  
def productMaterials(request):
    quotes=ProductMaterial.objects.all()
    # for quote in quotes:
    #     # Extract all materials related to the ProductMaterial instance
    #     materials = quote.material.all()
   
    #     # Iterate through the materials queryset
    #     for material in materials:
    #         print(material.name) 
    return render(request,'productandservices/productmaterial/productmaterial_list.html',{'quotes':quotes})   
    
@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login')     
def productMaterials_update_form(request, pk=None):
   
    product_material = get_object_or_404(ProductMaterial, pk=pk)
    form = ProductMaterialEditForm(instance=product_material)

    if request.method == 'POST':
        form = ProductMaterialEditForm(request.POST, instance=product_material)
        if form.is_valid():
            form.save()
            return redirect('product-materials')

    template_name = 'productandservices/productmaterial/productmaterial_detail.html'
    return render(request, template_name, {'form': form, 'product_material': product_material})

@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login') 
def product_materials_detail(request, product_id):
    # Fetch the specific product
    product = get_object_or_404(Product, pk=product_id)

    # Fetch all ProductMaterial instances for the product
    product_materials = ProductMaterial.objects.filter(product=product)

    # Define your template name (adjust as needed)
    template_name = 'productandservices/productmaterial/material.html'

    # Pass the product and product_materials to the template
    return render(request, template_name, {'product': product, 'product_materials': product_materials})
@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login') 
def productMaterials_form(request, pk=None):
    form = ProductMaterialForm()  # Initialize the form outside the if block

    if request.method == 'POST':
        form = ProductMaterialForm(request.POST)
        if form.is_valid():
            # Create a new ProductMaterial instance with the selected materials
            product_material = form.save(commit=False)

      
            # Save the product_material instance
            product_material.save()

            # Save the materials for the ManyToManyField
            form.save_m2m()

            return redirect('product-materials')  # Redirect to a success page

    template_name = 'productandservices/productmaterial/productmaterial_form.html'  # Replace with your actual template name

    return render(request, template_name, {'form': form})
@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login') 
def productMaterials_delete(request, pk):
    # Your delete logic here
    product = get_object_or_404(ProductMaterial, pk=pk)
    if request.method == 'POST':
        product.delete()
        # Add any additional processing or redirect as needed
        return redirect('product-materials')  # Redirect to the product list view

    template_name = 'productandservices/productmaterial/productmaterial_confirm_delete.html'  # Replace with your actual template name
    context = {'product': product}
    return render(request, template_name, context)


#######################Category and Brands Finished##################

@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login') 
def brand_category(request):
    cat = ProductCategory.objects.all()
    brand = ProductBrand.objects.all()
    
    return render(request, 'productandservices/brandandcategory/productAndcategory.html',{'cat':cat,'brand':brand})
@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login') 
def add_brands(request):
    if request.method=='POST':
        # Retrieve data from the form
        Brand = request.POST.get('BrandName')
        description = request.POST.get('description')

        # Get or create the category
   
        # Create the service
        service = ProductBrand.objects.create(
            name=Brand,
            description=description,
    
        )

        # Redirect to the service detail page or another appropriate page
        return redirect('brand_category')
    return render(request, 'productandservices/brandandcategory/brand/add_brand.html' )


@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login') 
def edit_brands(request, service_id):
    brand = ProductBrand.objects.get(pk=service_id)

    if request.method == 'POST':
        form = ProductBrandForm(request.POST, instance=brand)
        print(form)
        
        if form.is_valid():
            form.save()
            
            return redirect('brand_category')
    else:
        form = ProductBrandForm(instance=brand)

    return render(request, 'productandservices/brandandcategory/brand/edit_brand.html', {'brand_form': form, 'brand': brand})



@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login') 
def delete_brands(request, service_id):
    # Your delete logic here
    
    product = get_object_or_404(ProductBrand, pk=service_id)
    if request.method == 'POST':
        product.delete()
        # Add any additional processing or redirect as needed
        return redirect('brand_category')  # Redirect to the product list view

    template_name = 'productandservices/brandandcategory/brand/brand_confirm_delete.html'  # Replace with your actual template name
    context = {'brand': product}
    return render(request, template_name, context)









@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login') 

def add_category(request):
    if request.method=='POST':
        # Retrieve data from the form
        Brand = request.POST.get('CategoryName')
        description = request.POST.get('description')

        # Get or create the category
   
        # Create the service
        service = ProductCategory.objects.create(
            name=Brand,
            description=description,
    
        )

        # Redirect to the service detail page or another appropriate page
        return redirect('brand_category')
    return render(request, 'productandservices/brandandcategory/category/add_category.html' )


@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login') 
def edit_category(request, service_id):
    category = ProductCategory.objects.get(pk=service_id)

    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, instance=category)
        print(form)
        
        if form.is_valid():
            form.save()
            
            return redirect('brand_category')
    else:
        form = ProductCategoryForm(instance=category)

    return render(request, 'productandservices/brandandcategory/category/edit_category.html', {'category_form': form, 'category': category})


@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login') 
def delete_category(request, service_id):
    # Your delete logic here
    
    product = get_object_or_404(ProductCategory, pk=service_id)
    if request.method == 'POST':
        product.delete()
        # Add any additional processing or redirect as needed
        return redirect('brand_category')  # Redirect to the product list view

    template_name = 'productandservices/brandandcategory/category/category_confirm_delete.html'  # Replace with your actual template name
    context = {'category': product}
    return render(request, template_name, context)


#######################Category and Brands Finished##################
















#######################Services Start##################

@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login')
def list_services(request):
    services = Service.objects.all()
    return render(request, 'productandservices/services/services.html',{'services':services})

@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login')
def add_service(request):
    Category=ProductCategory.objects.all()
    if request.method=='POST':
        # Retrieve data from the form
        service_name = request.POST.get('supplierName')
        description = request.POST.get('description')
        category_name = request.POST.get('primaryGroupName')
        price = request.POST.get('price')
        quantity = request.POST.get('Qty')
        costing = request.POST.get('costing')

        # Get or create the category
        category = ProductCategory.objects.get(name=category_name)
   
        # Create the service
        service = Service.objects.create(
            name=service_name,
            description=description,
            category=category,
            price=price,
            Qty=quantity,
            costing=costing
        )

        # Redirect to the service detail page or another appropriate page
        return redirect('list_services')
    return render(request, 'productandservices/services/add_service.html',{'category':Category} )


@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login')
def edit_service(request, service_id):
    service = Service.objects.get(pk=service_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        print(form)
        
        if form.is_valid():
            form.save()
            
            return redirect('list_services')
    else:
        form = ServiceForm(instance=service)

    return render(request, 'productandservices/services/edit_service.html', {'service_form': form, 'service': service})

# def delete_service(request, service_id):
#     service = Service.objects.get(pk=service_id)
#     service.delete()
#     return redirect('list_services')

@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login')
def delete_service(request, service_id):
    # Your delete logic here
    
    product = get_object_or_404(Service, pk=service_id)
    if request.method == 'POST':
        product.delete()
        # Add any additional processing or redirect as needed
        return redirect('list_services')  # Redirect to the product list view

    template_name = 'productandservices/services/add_service.html'  # Replace with your actual template name
    context = {'product': product}
    return render(request, template_name, context)


#######################Services Finished##################











@login_required(login_url='login')
def acceptedsales_list(request):
        # Accessing the company of the logged-in user
    user = request.user
    company_name = None

    if user.is_authenticated:
        company = user.company
    # Retrieve ItemRow objects with related Sale foreign key
    item_rows_with_sale = ItemRow.objects.select_related('sale').filter(sale__isnull=False,sale__status='Accepted')

# Create a dictionary to store sale details along with related item rows
    sales_with_items = {}
    for item_row in item_rows_with_sale:
        sale_key = item_row.sale_id

        # Create a dictionary for the sale foreign key if it doesn't exist in the dictionary
        if sale_key not in sales_with_items:
            sales_with_items[sale_key] = {
                'status':item_row.sale.status,
                'sale_number': item_row.sale.sale_number,
                'customer_name': item_row.sale.customer_name,
                'company_name': item_row.sale.company_name,
                'contact_person': item_row.sale.contact_person,
                'contact_email': item_row.sale.contact_email,
                'billing_address': item_row.sale.billing_address,
                'shipping_address': item_row.sale.shipping_address,
                'sale_date': item_row.sale.sale_date,
                'delivery_datesale': item_row.sale.delivery_datesale,
                'tax_rate': item_row.sale.tax_rate,
                'terms_and_conditions': item_row.sale.terms_and_conditions,
                'notes_comments': item_row.sale.notes_comments,
                'advance': item_row.sale.advance,
                'sub_total': item_row.sale.sub_total,
                'tax_total': item_row.sale.tax_total,
                'final_amt': item_row.sale.final_amt,
                'ledger': item_row.sale.ledger_id,
                'items': [],
            }

        # Append item row details to the items list of the corresponding sale
        sales_with_items[sale_key]['items'].append({
            'product_name': item_row.product_name,
            'product_description': item_row.product_description,
            'quantity': item_row.quantity,
            'unit_price': item_row.unit_price,
            'total_price': item_row.total_price,
            # Add other fields as needed
        })

    # Now, sales_with_items is a dictionary where keys are sale foreign keys
    # and values are dictionaries containing Sale details along with related ItemRow details

    # You can convert the dictionary values to a list if needed
    result_list = list(sales_with_items.values())

    # Print the result
    return render(request,'Orders\salesOrderList.html',{'result_list':result_list,"company":company,'user':user})


from django.db.models import Sum, F, Case, When, Value, IntegerField

# views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Case, When, Value, IntegerField, F
from .models import   ProductMaterial, MaterialStock, AllocateMaterial, Material

def allocate(request, sales_id):
    sales_orders = ItemRow.objects.select_related('sale').filter(sale__sale_number=sales_id)
    status = get_object_or_404(Sales, sale_number=sales_id).status
    success_messages = messages.get_messages(request) 
    final = []
    count = 1

    for order in sales_orders:
        needed = []
        product_name = order.product_name.strip()
        material = ProductMaterial.objects.filter(product__name=product_name)

        for mat in material:
            material_quantity = (
                MaterialStock.objects
                .filter(material__name=mat.material.name)
                .aggregate(
                    total_quantity=Sum(
                        Case(
                            When(type='purchase', then=F('quantity')),
                            When(type__in=['return', 'prod'], then=-F('quantity')),
                            default=Value(0),
                            output_field=IntegerField()
                        )
                    )
                )
            )['total_quantity'] or 0

            needed.append({
                'material': mat.material.name,
                'unit': mat.material.unit_of_measurement,
                'quantity_per_piece': float(mat.quantity_per_piece),
                'order_quantity': order.quantity,
                'required': (order.quantity) * float(mat.quantity_per_piece),
                'available': material_quantity,
            })

        final.append({
            'id': count,
            'Product': order.product_name.strip(),
            'needed': needed,
        })
        count += 1

    if request.method == 'POST':
        # try:
            for i in final:
                count = len(i['needed'])

                for index in range(1, count + 1):
                    try:
                        material = request.POST.get(f'material_{i["id"]}_{index}')
                        unit = request.POST.get(f'unit_{i["id"]}_{index}')
                        quantity_per_piece = float(request.POST.get(f'quantity_per_piece_{i["id"]}_{index}'))
                        order_quantity = float(request.POST.get(f'order_quantity_{i["id"]}_{index}'))
                        required = float(request.POST.get(f'required_{i["id"]}_{index}'))
                        available = float(request.POST.get(f'available_{i["id"]}_{index}'))
                        allocate = float(request.POST.get(f'allocate_{i["id"]}_{index}'))
                        # Check if the necessary form fields are present before attempting allocation
                        if material is not None and unit is not None and quantity_per_piece is not None \
                                and order_quantity is not None and required is not None and available is not None:
                            # Use get_or_create to either retrieve the existing record or create a new one
                            allo, created = AllocateMaterial.objects.get_or_create(
                                sales=sales_id,
                                material=material,
                                defaults={
                                    'unit': unit,
                                    'quantity_per_piece': quantity_per_piece,
                                    'order_quantity': order_quantity,
                                    'required': required,
                                    'available': available,
                                    'allocated': allocate
                                }
                            )

                            # If the record already exists, update the fields
                            if not created:
                                allo.unit = unit
                                allo.quantity_per_piece = quantity_per_piece
                                allo.order_quantity = order_quantity
                                allo.required = required
                                allo.available = available
                                allo.allocated += allocate

                            allo.save()
                    except:
                        pass
        # except:
        #     pass
    # Fetch the latest allocated data
    allocated_data = AllocateMaterial.objects.filter(sales=sales_id).values()

    # Update the 'needed' list with the latest allocated data
    for product_data in final:
        for material_data in product_data['needed']:
            allocated = next((data['allocated'] for data in allocated_data if data['material'] == material_data['material']), 0)
            material_data['allocated'] = allocated

    return render(request, 'Orders/allocate.html', {'success_messages':success_messages,'final': final, 'sales_id': sales_id, 'status': status})



from django.db.models import Min
def start_production(request, sales_id):
    # Retrieve the allocated materials for the specified sales ID
    sales = Sales.objects.filter(sale_number=sales_id)
    allocated_materials = AllocateMaterial.objects.filter(sales=sales_id)
    # success_messages = messages.get_messages(request)   
    # Check if there are allocated materials
    if allocated_materials.exists():
        # TODO: Add your production logic here
        # For example, you might update a Production model or perform other production-related tasks

        # Update inventory status for allocated materials
        for allocated_material in allocated_materials:
            
            if allocated_material.allocated <1:
                
                print(allocated_material.allocated)
                messages.success(request, 'All Material Have to be Alloted to some Amt')
                return redirect('allocate',sales_id)  
        prod=Production()
        prod.sales_order=Sales.objects.get(sale_number=sales_id)
        prod.save()
        for allocated_material in allocated_materials:
            if allocated_material.allocated>1:
                mat=MaterialStock.objects.filter(material=Material.objects.get(name=allocated_material.material))
                cost_of_single = MaterialStock.objects.filter(
                    material__name=allocated_material.material
                ).aggregate(cost_of_single=Min('cost_of_single'))['cost_of_single']

                
                name=Material.objects.get(name=allocated_material.material)
                material_stock = MaterialStock.objects.get_or_create(
                type='prod',
                material=name,
                quantity=Decimal(allocated_material.allocated),
                cost_of_single=Decimal(cost_of_single),
                )
        messages.success(request, 'Order is Successfully Started')
        
        return redirect('allocate',sales_id)
    #     messages.success(request, 'Materials status updated and production started successfully.')
    # else:
    #     messages.warning(request, 'No materials allocated for production.')

    # Redirect back to the sales order detail page or any other page
def add_product_stock(request):
    if request.method == 'POST':
        form = ProductStockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_product_stock')  # Replace 'success_page' with the actual success page URL
    else:
        form = ProductStockForm()

    return render(request, 'inventory/add_product_stock.html', {'form': form})