from django.shortcuts import render
from accounting.models import *
from django.shortcuts import render, get_object_or_404
from commonApp.models import *
from django.shortcuts import render, redirect
from commonApp.models import *
from django.utils.dateparse import parse_date
from decimal import Decimal

# Create your views here.
def supplier_home(request):
    active_quotations = PurchaseQuotation.objects.filter(status=True).prefetch_related('items')
    return render(request,'supplierhome.html',{"purchase":active_quotations})

# supplier/views.py
from django.shortcuts import render

def purchase_order_page(request):
    products=Product.objects.filter(category=ProductCategory.objects.get(name='Purchase'))
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity', 0))
        price = Decimal(request.POST.get('price', 0))
        end_delivery_date = request.POST.get('endDelivery')
  
        
        supplier_type = request.POST.get('radio-stacked')
        commission = Decimal(request.POST.get('commision', 0))
        # Perform your calculations here based on supplier_type
        total = quantity * price
        if supplier_type == '1':
            total += quantity * commission
            supplier_type='agent'
            
        else:
            total = quantity * price
            supplier_type='supplier'
        productObj=Product.objects.get(id=product_id)
        total=float(total)

        order = Order(
            user=CustomUser.objects.get(username=request.user),
            product=productObj,
            product_name=productObj.name,
            quantity=quantity,
            supplier_type=supplier_type,
            price_per_quantal=price,
            quantity_left=quantity,
            end_delivery_date=end_delivery_date,
            agent_commission_per_quantal=commission,
            final_price=total
        )
        order.save()

        return redirect('supplierapproved')  

  

    context = {
        'products':products,
    }

    return render(request, 'purchase_order_page.html',context)


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








def supplierapproved(request):
    Orders=Order.objects.filter(is_approved='approved',user=request.user)
    return render(request, 'supplierOrderside/approved.html', {'Orders': Orders})  
def supplierdisapproved(request):
    Orders=Order.objects.filter(is_approved='disapproved')
    return render(request, 'supplierOrderside/disapproved.html', {'Orders': Orders})  
