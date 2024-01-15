from django.shortcuts import render
from accounting.models import *
from django.shortcuts import render, get_object_or_404
from commonApp.models import *
from django.shortcuts import render, redirect
from commonApp.models import *
from django.utils.dateparse import parse_date
from decimal import Decimal
from login.models import *
from django.db.models import Sum, F, ExpressionWrapper, fields
from datetime import timedelta
# Create your views here.
def supplier_home(request):
    one_year_ago = timezone.now() - timedelta(days=365)
    active_quotations = Order.objects.filter(is_approved='pending',user=request.user)
    total_orders = Order.objects.filter(user=request.user,order_date__gte=one_year_ago,).exclude(is_approved__in=['disapproved'])
    order_count = total_orders.count()
    total_final_amount = total_orders.aggregate(Sum('final_price'))['final_price__sum'] or 0

    total_commission = total_orders.aggregate(
    commission_sum=ExpressionWrapper(
        Sum(F('agent_commission_per_quantal') * F('quantity'), output_field=fields.DecimalField()),
        output_field=fields.DecimalField()
        )
    )['commission_sum'] or 0
    return render(request,'supplierhome.html',{"orders":active_quotations,'order_count':order_count,'total_commission':total_commission,'total_final_amount':total_final_amount})

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

def startdelivery(request,order_id,flag=None):
    
    user=CustomUser.objects.get(username=request.user)
    if str(user.account_type) == 'ACCOUNTANT':
        Orders=Order.objects.filter(id=order_id)
        delivery=DeliveryDetails.objects.filter(order=Orders[0].id)
        billing=Billing_Company.objects.all()
    else:
        Orders=Order.objects.filter(id=order_id,user=CustomUser.objects.get(username=request.user))
        delivery=DeliveryDetails.objects.filter(order=Orders[0].id)
        billing=Billing_Company.objects.all()
    try:
        latest_delivery = DeliveryDetails.objects.filter(order__id=order_id, row_type='delivery')[0].created_at
    except:
        latest_delivery=''
    if request.method=='POST':
        order = request.POST.get('order')
        
        vehicle = request.POST.get('vehicle')
        allBags = int(request.POST.get('allBags', 0))
        deliveryDate = request.POST.get('deliveryDate')
        quantity = Decimal(request.POST.get('quantity'))
        jute = int(request.POST.get('jute'))
        plastic = int(request.POST.get('plastic'))
        fssi = int(request.POST.get('fssi'))
        loose = int(request.POST.get('loose'))
        tObj=Order.objects.get(id=order)
        billing=request.POST.get('billing_company')
        partyname=request.POST.get('partyName')
        partaddress=request.POST.get('partyAddress')
        
        
        
        order = DeliveryDetails(
            user=CustomUser.objects.get(username=request.user),
            billing_company = Billing_Company.objects.get(id=billing) ,
            partyName =partyname ,
            partyAddress =partaddress ,
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
        
        
        
        
    return render(request, 'supplierOrderside/startdelivery.html', {'completed':flag,'billing':billing,'Orders': Orders[0],'delivery':delivery,'last':latest_delivery})  
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





def suppliercompleted(request):
    
    user=CustomUser.objects.get(username=request.user)
    if str(user.account_type) == 'ACCOUNTANT':
        Orders=Order.objects.filter(is_approved='completed')
    else:
        Orders=Order.objects.filter(is_approved='completed',user=request.user)
        
        
    return render(request, 'supplierOrderside/supplier_completed.html', {'Orders': Orders,'user':user}) 


def supplierapproved(request):
    Orders=Order.objects.filter(is_approved='approved',user=request.user)
    return render(request, 'supplierOrderside/approved.html', {'Orders': Orders})  
def supplierdisapproved(request):
    Orders=Order.objects.filter(is_approved='disapproved')
    return render(request, 'supplierOrderside/disapproved.html', {'Orders': Orders})  
