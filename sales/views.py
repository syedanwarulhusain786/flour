from django.shortcuts import render, redirect 
# Create your views here.
from django.contrib.auth.decorators import login_required
from .forms import QuotationForm
from .models import *
from django.http import JsonResponse
from django.db.models import Max
from django.db import transaction

from commonApp.models import *
from accounting.models import *
from login.models import *
from django.shortcuts import render, get_object_or_404
from accounting.models import *

def productDetail(request, product_id):
    # Assuming you have a specific product instance
    # product_id = 1  # Replace with the actual product ID
    product = get_object_or_404(Product, pk=product_id)

    # Now, you have product details
    product_details = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': str(product.productSelling),  # Convert DecimalField to string for serialization
        'images': [{'id': i, 'image_url': getattr(product, f'image{i}').url} for i in range(10) if getattr(product, f'image{i}')],
        'image':[{'id': i, 'image_url': getattr(product, f'image{i}').url} for i in range(10) if getattr(product, f'image{i}')][0]
    }

    # 'images' is a list of dictionaries, where each dictionary contains 'id' and 'image_url' keys
    # 'id' is the image ID, and 'image_url' is the URL to the image file

    print(product_details)
    return render(request, 'productDetails.html', {'product_details': product_details})


def get_next_sales_voucher_number(request):
    
    try:
        last_account = Quotation.objects.latest('quotation_number')
        next_account_number = 'Quote-{}'.format(str(int(last_account.quotation_number) + 1))
    except Quotation.DoesNotExist:
        next_account_number = 'Quote-'+str(10000)  # Initial account number

    return JsonResponse({'success': True, 'voucher_numbe': next_account_number})


@login_required(login_url='login')
def home(request):
    return render(request,'salehome.html')
@login_required(login_url='login')
def products(request):

    products_with_images = Product.objects.all()
    products = []

    for product in products_with_images:
        product_images = [getattr(product, f'image{i}').url for i in range(10) if getattr(product, f'image{i}')]

        dt = {
            "productId": product.id,
            "Product_Name": product.name,
            "Description": product.description,
            "Price": product.productSelling,
            "images": ["http://127.0.0.1:8000" + image_url for image_url in product_images]
        }

        products.append(dt)

        # Access images
        
    print(products)
    context={
        'products':products
    }
    return render(request,'products.html',context)

@login_required(login_url='login')
def create_sales(request):
    products=Product.objects.all()
    Ledgers=Ledger.objects.all()
    
    if request.method == 'POST':
        entry='quotations'
        
        # Handle POST request and process the form data
        quotation_number = int(request.POST.get('quotation_number'))
        customer_name = request.POST.get('customer_name')
        ledgerDR = request.POST.get('ledgerDR')
   
        company_name = request.POST.get('company_name')
        
        contact_person = request.POST.get('contact_person')
        
        contact_email = request.POST.get('contact_email')
        
        billing_address = request.POST.get('billing_address')
        shipping_address = request.POST.get('shipping_address')
        
        quotation_date = request.POST.get('bankjournal_date')
        expiry_date = request.POST.get('expiry_date')
        
        advance = float(request.POST.get('advance'))
        transactionType=request.POST.get('bankDr')
        transactionRemark=request.POST.get('transactionRemark')
        
        
        
        
        sub_total_s = float(request.POST.get('s_total'))
        tax_total_s = float(request.POST.get('tax'))
        final_amt_s = float(request.POST.get('final'))
        led=Ledger.objects.get(id=ledgerDR)

        quote=Sales(
            sale_number = quotation_number,
            customer_name = customer_name,
            company_name = company_name,
            contact_person = contact_person,
            contact_email = contact_email,
            billing_address = billing_address,
            shipping_address = shipping_address,
            sale_date = quotation_date,
            delivery_datesale = expiry_date,
            sub_total = sub_total_s,
            tax_total = tax_total_s,
            final_amt = final_amt_s,
            trasactionType=transactionType,
            trasactionDetails=transactionRemark,
            advance=advance,
            ledger=led,
        )
        Sales_form=quote.save()

        # Add a discount field if you intend to use it

        # quotation
        # Process Quotation Items
        for key, value in request.POST.items():
            print(key)
            if key.startswith('dropdown') and value:
                # Extract the index from the key (e.g., dropdown1, dropdown2, etc.)
                index = int(key.replace('dropdown', ''))
                
                ItemRow.objects.create(
                    # quotation=quotation,
                    entry_type=entry,
                    sale=quote,
                    product_name=request.POST.get(f'cat{index}'),
                    product_description=request.POST.get(f'sub{index}'),
                    quantity=request.POST.get(f'qty{index}'),
                    unit_price=request.POST.get(f'ref{index}'),
                    total_price=request.POST.get(f'amt{index}'),
                    
                    # Add other fields as needed
                )
                print(index)



        # Redirect to the detail view for the created quotation
        return redirect('sales_list')

    # Atomically increment the quotation number in the database
    latest_quotation = Sales.objects.order_by().last()
    next_quotation_number = latest_quotation.sale_number + 1 if latest_quotation else 10000

    context = {'sales_number': next_quotation_number,'products':products,'Ledgers':Ledgers}
    return render(request, 'salerOrder.html', context)
@login_required(login_url='login')
def sales_list(request):
        # Accessing the company of the logged-in user
    user = request.user
    company_name = None

    if user.is_authenticated:
        company = user.company
    # Retrieve ItemRow objects with related Sale foreign key
    item_rows_with_sale = ItemRow.objects.select_related('sale').filter(sale__isnull=False)

# Create a dictionary to store sale details along with related item rows
    sales_with_items = {}
    for item_row in item_rows_with_sale:
        sale_key = item_row.sale_id

        # Create a dictionary for the sale foreign key if it doesn't exist in the dictionary
        if sale_key not in sales_with_items:
            sales_with_items[sale_key] = {
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
    return render(request,'salesOrderList.html',{'result_list':result_list,"company":company,'user':user})






from django.db.models import F
def create_quotation(request):
    products=Product.objects.all()
    if request.method == 'POST':
        entry='quotations'
        
        # Handle POST request and process the form data
        quotation_number = request.POST.get('quotation_number')
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        
        contact_person = request.POST.get('contact_person')
        
        contact_email = request.POST.get('contact_email')
        
        billing_address = request.POST.get('billing_address')
        shipping_address = request.POST.get('shipping_address')
        
        quotation_date = request.POST.get('quotation_date')
        expiry_date = request.POST.get('expiry_date')
        
        
        sub_total_s = float(request.POST.get('s_total'))
        tax_total_s = float(request.POST.get('tax'))
        final_amt_s = float(request.POST.get('final'))
        

        quote=Quotation(
            quotation_number = quotation_number,
            customer_name = customer_name,
            company_name = company_name,
            contact_person = contact_person,
            contact_email = contact_email,
            billing_address = billing_address,
            shipping_address = shipping_address,
            quotation_date = quotation_date,
            expiry_date = expiry_date,
            sub_total = sub_total_s,
            tax_total = tax_total_s,
            final_amt = final_amt_s,
        )
        quotation=quote.save()
        print(quotation)
        # Add a discount field if you intend to use it

        # quotation
        # Process Quotation Items
        for key, value in request.POST.items():
            print(key)
            if key.startswith('dropdown') and value:
                # Extract the index from the key (e.g., dropdown1, dropdown2, etc.)
                index = int(key.replace('dropdown', ''))
                
                ItemRow.objects.create(
                    # quotation=quotation,
                    entry_type=entry,
                    quotation=quote,
                    product_name=request.POST.get(f'cat{index}'),
                    product_description=request.POST.get(f'sub{index}'),
                    quantity=request.POST.get(f'qty{index}'),
                    unit_price=request.POST.get(f'ref{index}'),
                    total_price=request.POST.get(f'amt{index}'),
                    
                    # Add other fields as needed
                )
                print(index)



        # Redirect to the detail view for the created quotation
        return redirect('create_quotation')

    # Atomically increment the quotation number in the database
    latest_quotation = Quotation.objects.order_by().last()
    next_quotation_number = latest_quotation.quotation_number + 1 if latest_quotation else 10000

    context = {'quotation_number': next_quotation_number,'products':products}
    return render(request, 'quotation.html', context)



@login_required(login_url='login')
def quoteOrderList(request):
    quotes=Quotation.objects.all()
            # Accessing the company of the logged-in user
    user = request.user
    company_name = None

    if user.is_authenticated:
        company = user.company
    # Retrieve ItemRow objects with related Sale foreign key
    item_rows_with_sale = ItemRow.objects.select_related('quotation').filter(quotation__isnull=False)

# Create a dictionary to store sale details along with related item rows
    sales_with_items = {}
    for item_row in item_rows_with_sale:
        sale_key = item_row.quotation_id

        # Create a dictionary for the sale foreign key if it doesn't exist in the dictionary
        if sale_key not in sales_with_items:
            sales_with_items[sale_key] = {
                'quotation_number': item_row.quotation.quotation_number,
                'customer_name': item_row.quotation.customer_name,
                'company_name': item_row.quotation.company_name,
                'contact_person': item_row.quotation.contact_person,
                'contact_email': item_row.quotation.contact_email,
                'billing_address': item_row.quotation.billing_address,
                'shipping_address': item_row.quotation.shipping_address,
                'quotation_date': item_row.quotation.quotation_date,
                'expiry_date': item_row.quotation.expiry_date,
                'tax_rate': item_row.quotation.tax_rate,
                'terms_and_conditions': item_row.quotation.terms_and_conditions,
                'notes_comments': item_row.quotation.notes_comments,
                'sub_total': item_row.quotation.sub_total,
                'tax_total': item_row.quotation.tax_total,
                'final_amt': item_row.quotation.final_amt,
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
    return render(request,'quotationList.html',{'result_list':result_list,"company":company,'user':user})