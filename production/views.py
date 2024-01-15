from django.shortcuts import render
from sales.models import *
from accounting.models import *
from .forms import ProductionRowForm,PostProductionRowForm
from django.shortcuts import render, redirect,get_object_or_404
from .models import ProductionRow,ProducedRow
from decimal import Decimal
# Create your views here.
def pendingOrder(request):
    # Your delete logic here
    orders=SalesQuotation.objects.filter(approval='inProduction')
    template_name = 'pendingorder.html'  # Replace with your actual template name
    context = {'orders':orders}
    return render(request, template_name, context)


def producedProduct(request, quotation_number):
    # Fetch the SalesQuotation instance based on the quotation_number
    sales_quotation = SalesQuotation.objects.get(quotation_number=quotation_number)
    ProductionRows= ProductionRow.objects.filter(sales_order=quotation_number)
    ProductionRo= ProducedRow.objects.filter(sales_order=quotation_number)
    
    

    if request.method == 'POST':
        production_row_form = PostProductionRowForm(request.POST)
        # Manually set the sales_order field with the SalesQuotation instance
        production_row_form = PostProductionRowForm(request.POST, initial={'sales_order': sales_quotation})
        if production_row_form.is_valid():
            production_row = production_row_form.save(commit=False)
            production_row.sales_order = sales_quotation
            production_row.save()

            # Redirect or do other actions as needed
            return redirect('producedproduction' , quotation_number=quotation_number )
        else:
            # Print form errors to the console
            print(production_row_form.errors)
    else:
        production_row_form = PostProductionRowForm()

    context = {
        'sales_quotation': sales_quotation,
        'production_form': production_row_form,
        'ProductionRow':ProductionRows,
        'ProducedRow':ProductionRo
    }

    template_name = 'produced.html'  # Replace with your actual template name
    return render(request, template_name, context)

def delete_produced(request, quotation_number):
    production = get_object_or_404(ProducedRow, pk=quotation_number)

   
        # Perform the deletion logic
    production.delete()

    # Redirect to a relevant page after deletion
    return redirect('producedproduction' , quotation_number=production.sales_order.quotation_number )



def send_to_inventory(request, quotation_number):
    sales_quotation = get_object_or_404(SalesQuotation, quotation_number=quotation_number)
     # Add logic to mark the order as sent for production
    sales_quotation.approval = 'produced'
    productionrows = ProducedRow.objects.filter(sales_order=quotation_number)

    for row in productionrows:
        sock=ProductStock()
       
        sock.product = Product.objects.get(name=row.product.name)
        
        sock.type='purchase'
        sock.quantity =row.TotalQuantity
        sock.cost_of_single =row.TotalCost/ row.TotalQuantity
        sock.save()
        
    sales_quotation.save()

    # You can add additional logic here, such as creating a Production instance, etc.

    return redirect('pendingOrder')

from datetime import datetime, date


def production_report(request):
    today = date.today()
    products= Product.objects.filter(category=ProductCategory.objects.get(name='Sales'))
    # Filter ProducedRow objects for today's date
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())

    # Filter ProducedRow objects for today's date
    produced = ProducedRow.objects.filter(production_date__range=(today_start, today_end))
      # Get products filtered by category
    products = Product.objects.filter(category=ProductCategory.objects.get(name='Sales'))

    # Create a dictionary mapping product names to a tuple of (packaging list, length of the list)
    product_name_packaging_dict = {
        product.name: (list(product.packaging_products.all()), len(product.packaging_products.all()))
        for product in products
    }
    # head=[]
    # for product in products:
    #     for prod in product.packaging_products.all():
    #         head.append(prod.name)  
    #         head=list(set(head))  

    # Filter ProducedRow objects for today's production_date
    # produced_rows_today = ProducedRow.objects.filter(production_date=today) 
    print(produced)
    
    context = {
        'today':today,
        'product':products,
        'produced': produced,
        'product_name_heading_dict':product_name_packaging_dict,
        'produced_rows_today':produced
    }
    template_name = 'production_report.html'  # Replace with your actual template name
    return render(request, template_name, context)






















def orders(request):
    # Your delete logic here
    
    
    template_name = 'productandservices/services/add_service.html'  # Replace with your actual template name
    context = {}
    return render(request, template_name, context)

def Startproduction(request):
    # Your delete logic here
    orders=SalesQuotation.objects.filter(approval='approved')
    template_name = 'production.html'  # Replace with your actual template name
    context = {'orders':orders}
    return render(request, template_name, context)
def allocateproduction(request, quotation_number):
    # Fetch the SalesQuotation instance based on the quotation_number
    sales_quotation = SalesQuotation.objects.get(quotation_number=quotation_number)
    ProductionRows= ProductionRow.objects.filter(sales_order=quotation_number)
    

    if request.method == 'POST':
        production_row_form = ProductionRowForm(request.POST)
        # Manually set the sales_order field with the SalesQuotation instance
        production_row_form = ProductionRowForm(request.POST, initial={'sales_order': sales_quotation})
        if production_row_form.is_valid():
            production_row = production_row_form.save(commit=False)
            production_row.sales_order = sales_quotation
            production_row.save()

            # Redirect or do other actions as needed
            return redirect('allocateproduction' , quotation_number=quotation_number )
        else:
            # Print form errors to the console
            print(production_row_form.errors)
    else:
        production_row_form = ProductionRowForm()

    context = {
        'sales_quotation': sales_quotation,
        'production_form': production_row_form,
        'ProductionRow':ProductionRows
    }

    template_name = 'orderdetail.html'  # Replace with your actual template name
    return render(request, template_name, context)

def delete_production(request, quotation_number):
    production = get_object_or_404(ProductionRow, pk=quotation_number)

   
        # Perform the deletion logic
    production.delete()

    # Redirect to a relevant page after deletion
    return redirect('allocateproduction' , quotation_number=production.sales_order.quotation_number )

def send_for_production(request, quotation_number):
    sales_quotation = get_object_or_404(SalesQuotation, quotation_number=quotation_number)
     # Add logic to mark the order as sent for production
    sales_quotation.approval = 'inProduction'
    productionrows = ProductionRow.objects.filter(sales_order=quotation_number)
    for row in productionrows:
        sock=ProductStock()
        if row.package.name.lower().find('raw')>-1:
            sock.product = Product.objects.get(name=row.product.name)
            sock.type='prod'
            sock.quantity =Decimal(row.TotalQuantity)
            sock.cost_of_single =row.TotalCost/ row.TotalQuantity
            sock.save()
        else:
            sock.product = Product.objects.get(name=row.package.name)
            
            sock.type='prod'
            sock.quantity =row.packageQuantity
            sock.cost_of_single =row.TotalCost/ row.packageQuantity
            sock.save()
        
    sales_quotation.save()

    # You can add additional logic here, such as creating a Production instance, etc.

    return redirect('startproduction')

