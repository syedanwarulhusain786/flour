from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from accounting.models import *
from django.shortcuts import render, get_object_or_404
from commonApp.models import *
from django.shortcuts import render, redirect
from commonApp.models import *
from django.utils.dateparse import parse_date
from decimal import Decimal
from login.models import *
# Create your views here.
def customer_home(request):
    Orders= SalesQuotation.objects.select_related('customer').prefetch_related('items').filter(approval__in =['Approved','disapproved','inProduction','produced','deliverPending','Completed'])
    print(Orders)
    # return render(request, 'customerOrder/adminOrder/approved.html', )
    return render(request,'customerhome.html',{'orders': Orders})

# supplier/views.py
from django.shortcuts import render

def sale_order_page(request):
    products=Product.objects.filter(category=ProductCategory.objects.get(name='Sales'))
    if request.method=='POST':
        
        quotation_number = request.POST.get('quotation_number')

        
        
        billing_address = request.POST.get('billing_address')
        shipping_address = request.POST.get('shipping_address')
   
        delivery_date = request.POST.get('delivery_date')
        
      
        
        
        sub_total_s = float(request.POST.get('s_total',0))
        terms = request.POST.get('terms')
        comment = request.POST.get('notes')
        
        
        quote=SalesQuotation(
            quotation_number = quotation_number,
            customer=CustomUser.objects.get(username=request.user),
            billing_address = billing_address,
            shipping_address = shipping_address,
            sub_total = sub_total_s,
            terms_and_conditions=terms,
            notes_comments=comment,
            delivery_date=delivery_date,
            approval='Pending'
        )
        quote.save()
        # Add a discount field if you intend to use it

        # quotation
        # Process Quotation Items

        for key, value in request.POST.items():
            if key.startswith('dropdown') and value:
                # Extract the index from the key (e.g., dropdown1, dropdown2, etc.)
                index = int(key.replace('dropdown', ''))
                productPk = request.POST.get(f'dropdown{index}')
                SalesItemRow.objects.create(
                    # quotation=quotation,
                    entry_type='agent',
                    product=Product.objects.get(id=productPk),
                    quotation=quote,
                    product_name=request.POST.get(f'cat{index}'),
                    product_description=request.POST.get(f'sub{index}'),
                    quantity=request.POST.get(f'qty{index}'),
                    unit_price=request.POST.get(f'ref{index}'),
                    total_price=request.POST.get(f'amt{index}'),
                    
                    # Add other fields as needed
                )

    latest_quotation = SalesQuotation.objects.order_by().last()
    next_quotation_number = latest_quotation.quotation_number + 1 if latest_quotation else 10000

    context = {
        'products':products,
        'next_quotation_number':next_quotation_number
    }

    return render(request, 'sales_order_page.html',context)



def purchase_quote(request):
    if request.method=='POST':
    
        quotation_number = request.POST.get('quotation_number')
        supplier_name = request.POST.get('supplier_name')
        
        billing_address = request.POST.get('billing_address')
        shipping_address = request.POST.get('shipping_address')
        cgst = request.POST.get('tax1')
        sgst = request.POST.get('tax2')
        delivery_date = request.POST.get('delivery_date')
        
      
        
        
        sub_total_s = float(request.POST.get('s_total',0))
        final_amt_s = float(request.POST.get('final',0))
        terms = request.POST.get('terms')
        comment = request.POST.get('notes')
        Others=request.POST.get('other',0)
        
        
        quote=PurchaseQuotation(
            quotation_number = quotation_number,

            billing_address = billing_address,
            shipping_address = shipping_address,
            sub_total = sub_total_s,
            final_amt = final_amt_s,
            csgst_total = cgst,
            sgst_total=sgst,
            terms_and_conditions=terms,
            notes_comments=comment,
            Others=Others,
            status = True,
            delivery_date=delivery_date,
            
        )
        quotation=quote.save()
        # Add a discount field if you intend to use it

        # quotation
        # Process Quotation Items

        for key, value in request.POST.items():
            if key.startswith('dropdown') and value:
                # Extract the index from the key (e.g., dropdown1, dropdown2, etc.)
                index = int(key.replace('dropdown', ''))
                SalesItemRow.objects.create(
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

        # Broadcast a WebSocket update to connected clients
        quotation_data = {
            'quotation_number': quote.quotation_number,
            'data':quote,
            'created_at': datetime.now(),
            # Add other fields as needed
        }
        consumer_instance = PurchaseQuotationConsumer()
        consumer_instance.broadcast_purchase_quotation_update(quotation_data)
        # PurchaseQuotationConsumer.broadcast_purchase_quotation_update(quotation_data)

        # Redirect to the detail view for the created quotation
        return redirect('purchase_quote')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    latest_quotation = PurchaseQuotation.objects.order_by().last()
    next_quotation_number = latest_quotation.quotation_number + 1 if latest_quotation else 10000
    company = get_object_or_404(Company, name=request.user.company)
    terms = get_object_or_404(TermsAndCondition,company=company,name='SHIPPING')
    tax = Tax.objects.all()
    
    
    
    context = {'PurchaseQuotation': next_quotation_number,'suppliers':supplier,'products':products,'terms':terms,'tax':tax}
    return render(request, 'purchase\PurchaseOrder\purchaseOrder.html',context)























def bidwon(request):
    return render(request, 'allbids.html')

def mybids(request):
    return render(request, 'bidswon.html')
def purchase_quotation_detail(request, quotation_number):
    purchase = get_object_or_404(PurchaseQuotation.objects.prefetch_related('items'), quotation_number=quotation_number, status=True)
    
    return render(request, 'purchase_quotation_detail.html', {'purchase': purchase})

def startdelivery(request,order_id):
    Orders=Order.objects.filter(id=order_id,is_approved='approved' ,user=CustomUser.objects.get(username=request.user))
    delivery=DeliveryDetails.objects.filter(order=Orders[0].id)
    try:
        latest_delivery = DeliveryDetails.objects.filter(order__id=order_id, row_type='delivery')[0].created_at
    except:
        latest_delivery=''
    if request.method=='POST':
        order = request.POST.get('order')
        
        vehicle = request.POST.get('vehicle')
        allBags = int(request.POST.get('allBags', 0))
        deliveryDate = request.POST.get('deliveryDate')
        
        quantity = int(request.POST.get('quantity'))
        jute = int(request.POST.get('jute'))
        plastic = int(request.POST.get('plastic'))
        fssi = int(request.POST.get('fssi'))
        loose = int(request.POST.get('loose'))
        tObj=Order.objects.get(id=order)
        order = DeliveryDetails(
            user=CustomUser.objects.get(username=request.user),
            order=tObj,
            row_type='dispatch',
            vehicle_number=vehicle,
            date_of_delivery=deliveryDate,
            no_of_bags=allBags,
            quantity=quantity,
            jute_bags = jute,
            plastic_bags = plastic,
            fssi = fssi,
            loose = loose,
        )
        order.save()
        
        
        
        
    return render(request, 'supplierOrderside/startdelivery.html', {'Orders': Orders[0],'delivery':delivery,'last':latest_delivery})  
# def place_bid(request, quotation_number):
#     purchase = get_object_or_404(PurchaseQuotation, quotation_number=quotation_number)
#     active_quotations = PurchaseQuotation.objects.filter(status=True).prefetch_related('items')

#     if request.method == 'POST':
#         # Process the bid placement form data here
#         # You can use Django forms for handling the form data
#         for i in range(1,20):
#             prod = request.POST.get('prod{}')
#             price = request.POST.get('price{}')
#             product = request.POST.get('product{}')
#             print(product,prod,price)
            
            
        
#     return render(request, 'place_bid.html', {'purchase': purchase})


def customercompleted(request):
    Orders= SalesQuotation.objects.select_related('customer').prefetch_related('items').filter(approval='completed')
  
    return render(request, 'customerOrderside/approved.html', {'orders': Orders})





def customerapproved(request):
    Orders= SalesQuotation.objects.select_related('customer').prefetch_related('items').filter(approval='approved')
    print('hii')
    return render(request, 'customerOrderside/approved.html', {'orders': Orders})  
def customerdisapproved(request):
    Orders=SalesQuotation.objects.select_related('customer').prefetch_related('items').filter(approval='disapproved')
 
    return render(request, 'customerOrderside/disapproved.html', {'orders': Orders})  


def CustomerQuotationDetailView(request,pk):

    sales_quotation_with_items = SalesQuotation.objects.select_related('customer').prefetch_related('items').filter(quotation_number=pk).first()
    delivery=SalesDeliveryDetails.objects.filter(OrderFk__quotation_number=pk)
    # print(sales_quotation_with_items.items.all())

   
    return render(request, 'customerOrderside\orderdetail.html', {'sales_quotation': sales_quotation_with_items,'delivery':delivery})  



def salesaccept(request,order_id):
    tObj=SalesDeliveryDetails.objects.get(id=order_id)
    deliverydate = tObj.date_of_delivery.strftime('%Y-%m-%d')
    
    if request.method=='POST':
        order = request.POST.get('order')
        
        vehicle = request.POST.get('vehicle')
        allBags = int(request.POST.get('allBags', 0))
        deliveryDate = request.POST.get('deliveryDate')
        
        quantity = int(request.POST.get('quantity'))
        jute = int(request.POST.get('jute'))
        plastic = int(request.POST.get('plastic'))
        fssi = int(request.POST.get('fssi'))
        loose = int(request.POST.get('loose'))
        item=SalesItemRow.objects.get(id=tObj.order.id)
        item.quantity_left=item.quantity_left-quantity
        tObj.status='delivered'
        
        orders = SalesDeliveryDetails(
            user=CustomUser.objects.get(username=request.user),
            OrderFk=SalesQuotation.objects.get(quotation_number=order),
            order=SalesItemRow.objects.get(id=item.id),
            row_type='delivery',
            vehicle_number=vehicle,
            date_of_delivery=deliveryDate,
            no_of_bags=allBags,
            quantity=quantity,
            jute_bags = jute,
            plastic_bags = plastic,
            fssi = fssi,
            loose = loose,
            status='delivered'
        )
        orders.save()
        tObj.save()
        item.save()
        if SalesDeliveryDetails.objects.filter(OrderFk=SalesQuotation.objects.get(quotation_number=order), status='delivered').count() == SalesDeliveryDetails.objects.filter(OrderFk=SalesQuotation.objects.get(quotation_number=order)).count():
            app=SalesQuotation.objects.get(quotation_number=order)
            app.approval='completed'
            app.save()
            
        ledger_entry=LedgerEntry(
            salesdelivery=tObj,
            saleorder = SalesQuotation.objects.get(quotation_number=order),
            account = Ledger.objects.get(ledger_name='CUSTOMER SALES'),
          
            description = f"For Sales OrderId:-{tObj.OrderFk.quotation_number} DeliveryID:-{tObj.id}" ,
            debit_amount =0 ,
            credit_amount = Decimal(tObj.order.total_price),
        ).save()
        ledger_entry=LedgerEntry(
            salesdelivery=tObj,
            saleorder = SalesQuotation.objects.get(quotation_number=order),
            account = Ledger.objects.get(ledgerUser=request.user),
          
            description = f"For Sales OrderId:-{tObj.OrderFk.quotation_number} DeliveryID:-{tObj.id}" ,
            debit_amount = Decimal(tObj.order.total_price),
            credit_amount = 0,
        ).save()
        return redirect('salesapproved')
    return render(request, 'customerOrderside/acceptdeliver.html',{'orders':tObj,"formatted_date":deliverydate})