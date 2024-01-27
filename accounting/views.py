from django.shortcuts import render
from django.shortcuts import render, redirect 
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from commonApp.forms import ProductBrandForm
from datetime import datetime
from .filters import JournalEntryFilter
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
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from commonApp.models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from commonApp.models import Product
from commonApp.forms import ProductDetailsForm  # Replace 'YourProductForm' with your actual form class

from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from django.contrib.staticfiles import finders
from decimal import Decimal
from commonApp.forms import ProductCategoryForm

from django.shortcuts import render, redirect
from commonApp.models import Service
from commonApp.forms import ServiceForm


from django.contrib.auth.decorators import user_passes_test
from login.models import CustomUser
from django.contrib.auth.decorators import login_required
from .forms import CustomPasswordChangeForm
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





def find_max_rows(query):
    row_keys = [key for key in query.keys() if key.startswith(('cat', 'sub', 'ref', 'qty', 'amt'))]

    # Extract the row numbers from the keys and convert them to integers
    row_numbers = [int(key[3:]) for key in row_keys]

    # Find the maximum row number
    max_row_number = max(row_numbers, default=0)

    return max_row_number


##########Order Approval######



@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def  accountingledger(request):
    IndividualAccount_list=Ledger.objects.all()
    group=Group.objects.all()
    primarGroup=Primary_Group.objects.all()
    supplier=CustomUser.objects.filter(account_type=AccountType.objects.get(name='Supplier'))
    customer=CustomUser.objects.filter(account_type=AccountType.objects.get(name='Customer'))
    agent=CustomUser.objects.filter(account_type=AccountType.objects.get(name='Agent'))
    
    
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    
    if request.method=="POST":
        if 'save' in request.POST:
            data = request.POST # Replace with your actual QueryDict data
            primaryGroupName = data.get(f'primaryGroupName')
            GroupName= data.get(f'GroupName')
            opening= data.get(f'opening',0)
            
            dr=Group.objects.get(group_number=primaryGroupName)
          
            
            prime=Ledger(group=dr,
                         ledger_name=GroupName,opening_balance=opening)
            prime.save()
    if request.method=="POST":
        if 'delete' in request.POST:
            account_numberc = request.POST.get('accountNumberc')
            
            # Assuming Primary_Group is your model
            prime_del = get_object_or_404(Ledger, ledger_number=account_numberc)
            prime_del.delete()
    
    return render(request, 'accountingledger.html', context={
            'username':request.user,'IndividualAccount_list':IndividualAccount_list,
            'group':group,'primaryGroup':primarGroup,'currency':currency,'supplier':supplier,
            'customer':customer,'agent':agent
        })
#################Ledger Finish###############




#######################User  Start##################


@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def add_user(request):
    IndividualAccount_list=Ledger.objects.all()
    group=Group.objects.all()
    primarGroup=Primary_Group.objects.all()
    accountType=AccountType.objects.all()


    if request.method == 'POST':
        voucher_no = request.POST.get('voucher_no')
        account_type = request.POST.get('account_type')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('firstName')
        
        last_name = request.POST.get('lastName')
        userCode = request.POST.get('userCode')
       
        
        credit_period = request.POST.get('creditPeriod', 0)
        phone = request.POST.get('phone',None)
        mobile = request.POST.get('mobile',None)
        email = request.POST.get('email',None)
        bank_account = request.POST.get('bankAccount',None)
        ifsc = request.POST.get('IFSC',None) 
        gst_no = request.POST.get('GstNo',None)
        pan = request.POST.get('pan',None)
        opening_balance = request.POST.get('openingBalance', 0)
        pinCode = request.POST.get('areaCode',None)
        address = request.POST.get('address',None)
        commission = request.POST.get('commission',0.0)
        
        # Check if the "Add To Ledger" checkbox is selected
        # add_to_ledger = request.POST.get('enable_options', False)
        ledger=None
        user_name=first_name+' '+last_name
        user_exists = CustomUser.objects.filter(username=username).exists()

        if user_exists:
            messages.error(request, f'An error occurred during user creation.Username already Exist')        
        else:
            try:
                user=CustomUser()
                user.is_superuser=False
                user.username=username
                user.first_name=first_name
                user.last_name=last_name
                user.email=email
                user.is_staff=False
                user.is_active=True
                user.account_type=AccountType.objects.get(name=account_type)
                user.company=Company.objects.get(id=request.user.company.id)
                user.department=Department.objects.get(name='NONE')
                user.ERPUsers_code=userCode
                user.ERPUsers_name=user_name.strip()
                user.credit_period=credit_period
                user.mobile=mobile
                user.phone=phone
                user.email=email
                user.ifsc=ifsc
                user.bank_account=bank_account
                user.gst_no=gst_no
                user.pan=pan
                user.pinCode=pinCode
                user.address=address
                user.commission=Decimal(commission)
                
                
                
                
                
                
                
                
                
                user.set_password(password)
                
                
                
                
                
                user.save()

                
                # if add_to_ledger:
                        # primary_group_number = request.POST.get('primaryGroupName')
                group_number = request.POST.get('GroupName')
                # primary=Primary_Group.objects.get(primary_group_number=primary_group_number)
                groups=Group.objects.get(group_number=group_number)
                ledger=Ledger.objects.create(
                    group=groups,
                    ledgerUser=user,
                    ledger_name=user_name.strip(),
                    opening_balance = opening_balance,

                )
                    
                user=CustomUser.objects.get(id=user.id)    
                user.ledger=ledger
                user.save()
                messages.success(request, 'User created successfully.')
            except Exception as e:
                # Handle exceptions appropriately
            
                # Display error message
                messages.error(request, f'An error occurred during user creation./n{e}')        
        return redirect('add_user')    
   
    latest_user_Id = CustomUser.objects.order_by().last()
    next_user_Id = latest_user_Id.id + 1 if latest_user_Id else 100
    return render(request,'users/add-users.html',context={
            'username':request.user,'IndividualAccount_list':IndividualAccount_list,
            'group':group,'primaryGroup':primarGroup,'next_Supplier_number':next_user_Id,'accountType':accountType
        })

@login_required(login_url='login')
def change_password(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        print(user)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('supplier')  # Replace with your user list view name or URL

    if request.method == 'POST':
        form = CustomPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('supplier')  # Replace with your user list view name or URL
    else:
        form = CustomPasswordChangeForm(user)
    return render(request, 'users/changepassword.html', {'form': form, 'user': user})
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def supplierList(request):
    
    primarGroup=Primary_Group.objects.all()
    Supplier_List=CustomUser.objects.filter(account_type=AccountType.objects.get(name='Supplier'))
    if request.method == 'POST':
        # Supplier_List=Supplier.objects.get()
        accountNumberc = request.POST.get('accountNumberc')
        Supp=CustomUser.objects.get(id=accountNumberc)
        
        Supp.delete()
        
    return render(request,'suppliers/suppliers.html',context={
            'username':request.user,
            'primaryGroup':primarGroup,'Supplier_List':Supplier_List
        })

@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def customerList(request):
    primarGroup=Primary_Group.objects.all()
    customerList=CustomUser.objects.filter(account_type=AccountType.objects.get(name='Customer'))
    if request.method == 'POST':
        # Supplier_List=Supplier.objects.get()
        accountNumberc = request.POST.get('accountNumberc')
        Supp=CustomUser.objects.get(id=accountNumberc)
        
        Supp.delete()
        
    return render(request,'customer/customers.html',context={
            'username':request.user,
            'primaryGroup':primarGroup,'Supplier_List':customerList
        })


@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def agentList(request):
    primarGroup=Primary_Group.objects.all()
    agentList=CustomUser.objects.filter(account_type=AccountType.objects.get(name='Agent'))
    if request.method == 'POST':
        # Supplier_List=Supplier.objects.get()
        accountNumberc = request.POST.get('accountNumberc')
        Supp=CustomUser.objects.get(id=accountNumberc)
        
        Supp.delete()
        
    return render(request,'agent/agent.html',context={
            'username':request.user,
            'primaryGroup':primarGroup,'Supplier_List':agentList
        })
#######################Users Finished##################

#############Supplier Delivery ############
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def approve(request):
    # order=Order.objects.filter(is_approved='pending')
    order=Order.objects.filter(is_approved='pending')
    if request.method=='POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        if action=='approved':
            ord=Order.objects.get(id=order_id)
            ord.is_approved="approved"
            ord.save()
            return redirect('adminapproved')
            
            # Notification.objects.create(user=order.user, message='Admin Just Approved: Order #{order_id}')  
            
        elif action=='disapproved':
            ord=Order.objects.get(id=order_id)
            ord.is_approved="disapproved"
            ord.save()
            return redirect('admindisapproved')
            
            # Notification.objects.create(user=order.user, message=f'Admin Just Disapproved: Order #{order_id}')  
            
        else:
            pass
        
    return render(request,'supplierOrder/order_approval.html',{'orders':order})
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def acceptDelivery(request,order_id):
    
    Orders=Order.objects.filter(id=order_id,is_approved='approved')
    delivery=DeliveryDetails.objects.filter(order=Orders[0].id)
    try:
        latest_delivery = DeliveryDetails.objects.filter(order__id=order_id, user=request.user, row_type='delivery')[0].created_at
    except:
        latest_delivery=''
        
        
        
    return render(request, 'adminOrder/acceptdelivery.html', {'Orders': Orders[0],'delivery':delivery,'last':latest_delivery}) 
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def updateDelivery(request,order_id):
    delivery=DeliveryDetails.objects.get(id=order_id)
    try:
        brk=delivery.quantity*delivery.order.agent_commission_per_quantal
    except:
        brk=0.00
            
    formatted_date = delivery.date_of_delivery.strftime('%Y-%m-%d')
    
    if request.method=='POST':
        current_date = datetime.now()
        supp=CustomUser.objects.get(username=delivery.order.user)
        due_date = current_date + timedelta(days=supp.credit_period)
        order = request.POST.get('order')
        
        vehicle = request.POST.get('vehicle')
        allBags = int(request.POST.get('allBags', 0))
        deliveryDate = request.POST.get('deliveryDate')
        inv = request.POST.get('inv')
        invdate = request.POST.get('invdate')
        
        quantity = Decimal(request.POST.get('aq'))
        jute = int(request.POST.get('jute'))
        plastic = int(request.POST.get('plastic'))
        fssi = int(request.POST.get('fssi'))
        loose = int(request.POST.get('loose'))
        Freight = Decimal(request.POST.get('Freight'))
        Dala = Decimal(request.POST.get('Dala'))
        cd = Decimal(request.POST.get('cd'))
        tds = Decimal(request.POST.get('tds'))
        Bardana = Decimal(request.POST.get('Bardana'))
        Brokerage = Decimal(request.POST.get('Brokerage'))
        Commission = Decimal(request.POST.get('Commission'))
        Kata = Decimal(request.POST.get('Kata'))
        
        
        total = Decimal(request.POST.get('total'))
        final = Decimal(request.POST.get('final'))
        billing=request.POST.get('billing_company')
        partyname=request.POST.get('partyName')
        partaddress=request.POST.get('partyAddress')
        tObj=Order.objects.get(id=order)
        tObj.quantity_left=Decimal(tObj.quantity_left)-Decimal(quantity)
        tObj.save()
        delivery.status='delivered'
        delivery.save()
        
        order = DeliveryDetails(
            user=CustomUser.objects.get(username=request.user),
            billing_company = Billing_Company.objects.get(id=billing) ,
            partyName =partyname ,
            partyAddress =partaddress ,
            order=tObj,
            row_type='delivery',
            vehicle_number=vehicle,
            date_of_delivery=deliveryDate,
            no_of_bags=allBags,
            quantity=quantity,
            jute_bags = jute,
            plastic_bags = plastic,
            fssi = fssi,
            loose = loose,
            freight = Freight ,
            data = Dala,
            kanta = Kata ,
            cashDiscount = cd,
            tdsTcs = tds,
            bardana = Bardana,
            brokerage = Brokerage,
            commission = Commission,
            deductedAmt = total,
            finalAmt = final,
            dueDate=due_date,
            invoice_no = inv,
            invoice_date = invdate,
            status='delivered'
        )
        order.save()
        if tObj.supplier_type=='agent':
            final=Brokerage
        sock=ProductStock()
       
        sock.product = tObj.product
        
        sock.type='purchase'
        sock.quantity =quantity
        sock.cost_of_single =tObj.price_per_quantal
        sock.save()
        ledger_entry=LedgerEntry(
            delivery = order,
            order = tObj,
            account = Ledger.objects.get(ledger_name='SUPPLIER PURCHASES'),
            # Other fields for ledger entry details
            description = f"For Purchase OrderId:-{order} DeliveryID:-{delivery} Invoice No:{inv} Invoice Date :{invdate} " ,
            debit_amount = Decimal(final),
            credit_amount = 0,
        ).save()
        ledger_entry=LedgerEntry(
            delivery = order,
            order = tObj,
            account = Ledger.objects.get(ledgerUser=delivery.order.user),
            # Other fields for ledger entry details
            description = f"For Purchase OrderId:-{order} DeliveryID:-{delivery}" ,
            debit_amount = 0,
            credit_amount = Decimal(final),
        ).save()
        # Notification.objects.create(user=order.user, message=f'Delivery Accepted: Order #{order.id}')
        return redirect('adminapproved')
        
        
        
    return render(request, 'adminOrder/updatedelivery.html', {'delivery':delivery,'formatted_date':formatted_date,'brk':brk})  




@login_required(login_url='login')
def downloadDelivery(request,order_id):
    
    delivery=DeliveryDetails.objects.get(id=order_id)
    formatted_date = delivery.date_of_delivery.strftime('%Y-%m-%d')

        
        
    return render(request, 'adminOrder/downloadDelivery.html', {'delivery':delivery,'formatted_date':formatted_date})  


@login_required(login_url='login')
def salesdownloadDelivery(request,order_id):
    
    delivery=SalesDeliveryDetails.objects.get(id=order_id)
    formatted_date = delivery.date_of_delivery.strftime('%Y-%m-%d')
    if delivery.row_type == 'dispatch':
        row='Dispatch'
    else:
        row='Delivery'
        
    

        
        
    return render(request, 'customerOrder/adminOrder/saledownload.html', {'row':row,'orders':delivery,'formatted_date':formatted_date})  










@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def adminapproved(request):
    Orders=Order.objects.filter(is_approved='approved')
    return render(request, 'adminOrder/approved.html', {'Orders': Orders})  
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def admindisapproved(request):
    Orders=Order.objects.filter(is_approved='disapproved')
    return render(request, 'adminOrder/disapproved.html', {'Orders': Orders})  
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def salesacceptDelivery(request,order_id):
    
    Orders=Order.objects.filter(id=order_id,is_approved='approved')
    delivery=DeliveryDetails.objects.filter(order=Orders[0].id)
    try:
        latest_delivery = DeliveryDetails.objects.filter(order__id=order_id, user=request.user, row_type='delivery')[0].created_at
    except:
        latest_delivery=''
    
     
        
        
    return render(request, 'adminOrder/acceptdelivery.html', {'Orders': Orders[0],'delivery':delivery,'last':latest_delivery})  




#############Supplier Delivery Finished ############

































####################a

def SalesQuotationDetailView(request,pk):
    delivery=SalesDeliveryDetails.objects.filter(OrderFk=pk)
    
    try:
        latest_delivery = SalesDeliveryDetails.objects.filter(order__quotation_number=order_id, row_type='delivery')[0].created_at
    except:
        latest_delivery=''
    sales_quotation_with_items = SalesQuotation.objects.select_related('customer').prefetch_related('items').filter(quotation_number=pk).first()
    if request.method=='POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        delivery = request.POST.get('delivery_date')
        if action=='approved':
            ord=SalesQuotation.objects.get(quotation_number=order_id)
            ord.approval="approved"
            ord.delivery_date=delivery
            
            ord.save()
            return redirect('salesapproved')
        elif action=='disapproved':
            ord=SalesQuotation.objects.get(quotation_number=order_id)
            ord.approval="Disapproved"
            ord.save()
            return redirect('salesdisapproved')
        else:
            pass

    if str(request.user.account_type) =='Customer':
        
        return render(request, 'customerOrderside/orderdetail.html', {'sales_quotation': sales_quotation_with_items,'delivery':delivery})  
    else:    
        return render(request, 'customerOrder/orderdetail.html', {'sales_quotation': sales_quotation_with_items})  


def salesapprove(request):
    approved_quotations = SalesQuotation.objects.select_related('customer').prefetch_related('items').filter(approval__in=['Pending','pending'])

    if request.method=='POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        delivery = request.POST.get('delivery_date')
        print(order_id,action,delivery)

      
    return render(request,'customerOrder/order_approval.html',{'orders':approved_quotations})
def salescompleted(request):
    
    Orders= SalesQuotation.objects.select_related('customer').prefetch_related('items').exclude(approval__in =['pending','Pending','Disapproved','disapproved'])
    return render(request, 'customerOrder/adminOrder/approved.html', {'orders': Orders})  
def salesapproved(request):
    
    Orders= SalesQuotation.objects.select_related('customer').prefetch_related('items').exclude(approval__in =['pending','Pending','Disapproved','Completed','disapproved','completed'])
    return render(request, 'customerOrder/adminOrder/approved.html', {'orders': Orders})  
def salespending(request):
    
    Orders = SalesQuotation.objects.filter(approval__in=['pending','Pending']).select_related('customer').prefetch_related('items')
    print(Orders)
    return render(request, 'customerOrder/adminOrder/sales_pending.html', {'orders': Orders}) 
def salesdisapproved(request):
    Orders=SalesQuotation.objects.select_related('customer').prefetch_related('items').filter(approval='disapproved')
    return render(request, 'customerOrder/adminOrder/disapproved.html', {'orders': Orders})  

def salesstartdelivery(request,order_id):
    Orders = SalesQuotation.objects.select_related('customer').prefetch_related('items').filter(quotation_number=order_id).first()#,approval='Approved' ,customer=CustomUser.objects.get(username=request.user)
    counter=Orders.items.all()
    delivery=SalesDeliveryDetails.objects.filter(OrderFk=order_id)
    
    
    try:
        latest_delivery = SalesDeliveryDetails.objects.filter(order__quotation_number=order_id, row_type='delivery')[0].created_at
    except:
        latest_delivery=''
       
    if request.method=='POST':
        for i in counter:
            order = request.POST.get(f'order{i.id}')
            product = request.POST.get(f'product{i.id}')
            
            vehicle = request.POST.get(f'vehicle{i.id}')
            allBags = int(request.POST.get(f'allBags{i.id}'))
            deliveryDate = request.POST.get(f'deliveryDate{i.id}')
            
            quantity = int(request.POST.get(f'quantity{i.id}'))
            jute = int(request.POST.get(f'jute{i.id}'))
            plastic = int(request.POST.get(f'plastic{i.id}'))
            fssi = int(request.POST.get(f'fssi{i.id}'))
            loose = int(request.POST.get(f'loose{i.id}'))
            tObj = SalesItemRow.objects.get(id=i.id)
            order = SalesDeliveryDetails(
                OrderFk=SalesQuotation.objects.get(quotation_number=order),
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
                final_quantity_price=float(tObj.unit_price) * float(quantity)
            )
            order.save()
        # Notification.objects.create(user=order.user, message=f'You have a new Deliver: Order #{order.id}')
        return redirect('salesapproved')
        
        
    return render(request, 'customerOrder/adminOrder/startdelivery.html', {'orders': Orders,'delivery':delivery,'last':latest_delivery})  



 
@login_required(login_url='login')
def payables(request):
    all_pay=DeliveryDetails.objects.filter(row_type='delivery')
    print(all_pay)
    return render(request,'account/payables.html',{'all_pay':all_pay})
@login_required(login_url='login')
def recievables(request):
    
    return render(request,'account/recievables.html')

@login_required(login_url='login')
def viewdelivery(request,pk):
    purchase = get_object_or_404(DeliveryDetails, order=pk)
    company = get_object_or_404(Company, name=request.user.company)
    quote = PurchaseItemRow.objects.filter(quotation=purchase)
    
    


    return render(request,'bills/PurchaseOrder1.html',{'purchase':purchase,'company':company,'quotes':quote})













@login_required(login_url='login')
def PurchaseQuotationDetailView(request,pk):
    print(request.user.company)
    purchase = get_object_or_404(PurchaseQuotation, quotation_number=pk)
    company = get_object_or_404(Company, name=request.user.company)
    quote = PurchaseItemRow.objects.filter(quotation=purchase)
    
    


    return render(request,'bills/PurchaseOrder1.html',{'purchase':purchase,'company':company,'quotes':quote})




# def updateDelivery(request,order_id):

#     delivery=DeliveryDetails.objects.get(id=order_id)
#     formatted_date = delivery.date_of_delivery.strftime('%Y-%m-%d')

#     if request.method=='POST':
#         order = request.POST.get('order')
        
#         vehicle = request.POST.get('vehicle')
#         allBags = int(request.POST.get('allBags', 0))
#         deliveryDate = request.POST.get('deliveryDate')
        
#         quantity = int(request.POST.get('quantity'))
#         jute = int(request.POST.get('jute'))
#         plastic = int(request.POST.get('plastic'))
#         fssi = int(request.POST.get('fssi'))
#         loose = int(request.POST.get('loose'))
#         tObj=Order.objects.get(id=order)
#         tObj.quantity_left-=quantity
#         tObj.save()
#         delivery.status='delivered'
#         delivery.save()
#         order = DeliveryDetails(
#             user=CustomUser.objects.get(username=request.user),
#             order=tObj,
#             row_type='delivery',
#             vehicle_number=vehicle,
#             date_of_delivery=deliveryDate,
#             no_of_bags=allBags,
#             quantity=quantity,
#             jute_bags = jute,
#             plastic_bags = plastic,
#             fssi = fssi,
#             loose = loose,
#             status='delivered'
#         )
#         order.save()
#         prod=ProductStock()  
#         prod.delivery=delivery  
#         prod.product=tObj.product  
#         prod.type='purchase'
#         prod.quantity=quantity  
#         prod.cost_of_single=tObj.price_per_quantal
#         prod.save()
#         # Notification.objects.create(user=order.user, message=f'Your Delivery is Accepted: Order #{order.id}')
#         return redirect('adminapproved')
        
        
        
#     return render(request, 'adminOrder/updatedelivery.html', {'delivery':delivery,'formatted_date':formatted_date})  



















##################Purchase################
  
  
def purchaseEntry(request):
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    debit = Ledger.objects.filter(group__group_name__in=["Purchase"])
    cash= Ledger.objects.filter(group__group_name__in=["Cash"])
    accounts = Ledger.objects.exclude(group__group_name__in=["Purchase"])
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    return render(request, 'purchase/PurchaseInvoice_Voucher/purchaseVoucher.html', context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':accounts,'currency':currency,'debit':debit,
        'cashs':cash
    })  
    
def purchaseList(request):
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    banks = Ledger.objects.filter(group__group_name__in=["Bank Account"])
    cash= Ledger.objects.filter(group__group_name__in=["Cash"])
    accounts = Ledger.objects.exclude(group__group_name__in=["Cash", "Bank Account"])
    supplier=Supplier.objects.all()
    products=Product.objects.all()
    latest_quotation = PurchaseQuotation.objects.order_by().last()
    next_quotation_number = latest_quotation.quotation_number + 1 if latest_quotation else 10000
    company = get_object_or_404(Company, name=request.user.company)
    print(next_quotation_number)
    terms = TermsAndCondition.objects.get(company=company,name='SHIPPING')
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    return render(request, 'purchase/PurchaseInvoice_Voucher/purchaseVouchers.html', context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':accounts,'currency':currency,'banks':banks,
        'cashs':cash,'PurchaseQuotation': next_quotation_number,'suppliers':supplier,'products':products,'terms':terms
    })
  
  
  
def submitpurchase(request):
    # Category_list=Primary_Group.objects.all()
    # Subcategory_list = Group.objects.all()
    # debit = Ledger.objects.filter(group__group_name__in=["Sales"])
    # accounts = Ledger.objects.exclude(group__group_name__in=["Sales"])
    # currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    
    
    # try:
    data = request.POST # Replace with your actual QueryDict data
    bankDr = data.get(f'bankDr')
    
    voucher_no = data.get(f'invoice_no')
    invoicedate = data.get(f'invoice_date')
    debit_led = data.get(f'debit_led')
    total = data.get(f'd_total')
    
    deb_category = Primary_Group.objects.get(primary_group_name='EXPENSES')
    deb_subcategory = Group.objects.get(group_name='Purchase')
    deb_account = Ledger.objects.get(ledger_name=debit_led.split('-')[-1])  # Replace with the appropriate field
            
    
    
    try:
    # Loop through the data to create and save JournalEntries instances
        for i in range(1, 10):  # Assuming you have four sets of data (1 to 4)
            # Replace 'voucher' with the actual key in your QueryDict
            # narration = data.get(f'nar{i}')  # Replace 'nar' with the actual key in your QueryDict
            category_name = data.get(f'cat{i}')
            subcategory_name = data.get(f'sub{i}')
            desc = data.get(f'ref{i}', 0)
            amt = data.get(f'amt{i}', 0)
            bill_no = data.get(f'bill{i}', 0)
            
            
            

            account_num=data.get(f'dropdown{i}', 0)  # Default to 0 if not present or invalid
            print(account_num)
            
            try:
                    # Fetch the corresponding Category, Subcategory, and IndividualAccount instances
                
                cre_account = Ledger.objects.get(ledger_number=account_num)  # Replace with the appropriate field
                cre_subcategory = cre_account.group
                cre_category = cre_account.group.primary_group
                print(voucher_no)
                
                # Create and save the JournalEntries instance
                entry = PurchaseReceipt(
                    date=invoicedate,
                    voucherNo=voucher_no.split('-')[-1],
                    voucherCode=voucher_no,
                    deb_primary_group=deb_category,
                    deb_group=deb_subcategory,
                    deb_ledger=deb_account,
                    cred_primary_group=cre_category,
                    cred_group=cre_subcategory,
                    cred_ledger=cre_account,
                    description=desc,
                    amount=float(amt),
                    total=float(total),
                    bill_no=bill_no
                    
                        # You can set comments as needed
                )
                entry.save()
            except Primary_Group.DoesNotExist:
                pass
            except Group.DoesNotExist:
                pass
            except Ledger.DoesNotExist:
                pass
        entry_response = {
                    "voucherNo": entry.voucherNo,
                    "voucherCode": entry.voucherCode,  # Assuming you have a 'voucherCode' field in your model
                    "account": entry.deb_ledger.ledger_name,  # Assuming 'account_name' is the relevant field in 'IndividualAccount'
                }

        return JsonResponse({'success': True, 'message': 'Sucess'})            
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': 'Invalid request'})
        
    
    


from .consumers import PurchaseQuotationConsumer

def purchase_quote(request):
    supplier=Supplier.objects.all()
    products=Product.objects.all()
    if request.method=='POST':
        # Extract keys that match the pattern 'cat{number}', 'sub{number}', 'ref{number}', etc.
        rows=find_max_rows(request.POST)
        
        entry='PurchaseQuotation'
        
        # Handle POST request and process the form data
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
                index = int(key.replace('dropdown'))
                PurchaseItemRow.objects.create(
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
    return render(request, 'purchase/PurchaseOrder/purchaseOrder.html',context)

@login_required(login_url='login')
def quotepurchaseList(request):
    quotes=PurchaseQuotation.objects.all()
    return render(request,'purchase/PurchaseOrder/PurchaseOrders.html',{'quotes':quotes})


@login_required(login_url='login')
def PurchaseQuotationDeleteView(request,pk):
        
    product = get_object_or_404(PurchaseQuotation, quotation_number=pk)
    if request.method == 'POST':
        product.delete()
        # Add any additional processing or redirect as needed
        return redirect('purchase-orders')  # Redirect to the product list view

    return render(request,'purchase/PurchaseOrder/purchaseOrdersConfirmDelet.html',{'object':product})

    
######################################################## 
    
    
    
    
    
    
    
    
###########product Material Section############    
def productMaterials(request):
    quotes=ProductMaterial.objects.all()
    for quote in quotes:
        # Extract all materials related to the ProductMaterial instance
        materials = quote.material.all()
   
        # Iterate through the materials queryset
        for material in materials:
            print(material.name) 
    return render(request,'productandservices/productmaterial/productmaterial_list.html',{'quotes':quotes})   
    
    
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
from django.shortcuts import render, redirect
from commonApp.models import ProductMaterial
from commonApp.forms import ProductMaterialForm,ProductMaterialEditForm

def product_materials_detail(request, product_id):
    # Fetch the specific product
    product = get_object_or_404(Product, pk=product_id)

    # Fetch all ProductMaterial instances for the product
    product_materials = ProductMaterial.objects.filter(product=product)

    # Define your template name (adjust as needed)
    template_name = 'productandservices/productmaterial/material.html'

    # Pass the product and product_materials to the template
    return render(request, template_name, {'product': product, 'product_materials': product_materials})
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


def brand_category(request):
    cat = ProductCategory.objects.all()
    brand = ProductBrand.objects.all()
    
    return render(request, 'productandservices/brandandcategory/productAndcategory.html',{'cat':cat,'brand':brand})

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

def list_services(request):
    services = Service.objects.all()
    return render(request, 'productandservices/services/services.html',{'services':services})

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
def accountingDashboard(request):
    return render(request,'accountingDashboard.html')


















@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def Journal_entry(request):
                
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    account = VoucherLedgerVisibility.objects.get(voucher_type='JV')

    # Get all ledgers under the selected groups
    selected_group_numbers = account.selected_groups.values_list('group_number', flat=True)
    ledgers_under_selected_groups = Ledger.objects.filter(
        Q(group__group_number__in=selected_group_numbers) |
        Q(group__primary_group__primary_group_number__in=selected_group_numbers)
    )


    if request.method=='POST':
        # Extract keys that match the pattern 'cat{number}', 'sub{number}', 'ref{number}', etc.
        
        # Handle POST request and process the form data
        journal_date = request.POST.get('journal_date')
        voucher_no = request.POST.get('voucher_no')
        
        invoice_no = request.POST.get('invoice_no')
        notes = request.POST.get('notes')
        
        invoice_date = request.POST.get('invoice_date')
        
        
        d_total = float(request.POST.get('d_total'))
        c_total = float(request.POST.get('c_total'))

        count=int(request.POST.get('count'))
        quote=JournalEntry(
            date = journal_date,
            voucherNo=voucher_no,
            invoice_no=invoice_no,
            invoice_date=invoice_date,
            
            narration = notes,
            debit_total = d_total,  
            credit_total = c_total, 
        )
        quote.save()
        # Add a discount field if you intend to use it

 
        for index in range(1,count+1):
                led = request.POST.get(f'dropdown{index}')
                comment=request.POST.get(f'nar{index}')
                print(comment)
                try:
                    cred=float(request.POST.get(f'deb{index}'))
                except:
                    cred=0.00
                try:
                    deb=float(request.POST.get(f'cre{index}'))
                except:
                    deb=0.00
                
                # Extract the index from the key (e.g., dropdown1, dropdown2, etc.)
                JournalEntryRow.objects.create(
                    # quotation=quotation,
                    entryFk=quote,
                    ledger=Ledger.objects.get(ledger_number=led),
                    comment=comment,
                    debit=cred,
                    credit=deb,

                    # Add other fields as needed
                )
                LedgerEntry.objects.create(
                    account = Ledger.objects.get(ledger_number=led),
                    description = notes,
                    debit_amount = cred,
                    credit_amount = deb,
                )



        # Redirect to the detail view for the created quotation
        return redirect('journal-entries')
        
        
                  
    latest_quotation = JournalEntry.objects.order_by().last()
    next_quotation_number = latest_quotation.voucherNo + 1 if latest_quotation else 100
    return render(request, 'vouchers/Journal/journalEntry.html',  context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':ledgers_under_selected_groups,
    'next_quotation_number':next_quotation_number})
    
    
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def payments(request):
    paymentsV=PaymentEntry.objects.all()
    return render (request, 'vouchers/Payment/paymentList.html',  context={'paymentsV':paymentsV})
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def reciepts(request):
    RecieptEntryV=RecieptEntry.objects.all()
    return render (request, 'vouchers/Reciept/receiptList.html',  context={'RecieptEntryV':RecieptEntryV})





@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def payment(request):
                

    purchase=DeliveryDetails.objects.filter(payment__in=['due','pending'],row_type='delivery')
   
    pay = Ledger.objects.filter(group__group_name__in=['BANK ACCOUNTS', 'CASH-IN-HAND'])
    to_ledger_accounts = Ledger.objects.exclude(group__group_name__in=['BANK ACCOUNTS', 'CASH-IN-HAND'])

   

    if request.method=='POST':
        # Extract keys that match the pattern 'cat{number}', 'sub{number}', 'ref{number}', etc.
        
        # Handle POST request and process the form data
        journal_date = request.POST.get('journal_date')
        voucher_no = request.POST.get('voucher_no')
        
        invoice_no = request.POST.get('invoice_no')
        notes = request.POST.get('notes')
        
        invoice_date = request.POST.get('invoice_date')
        
        from_ledger = request.POST.get(f'dropdown1')
        to_ledger=request.POST.get(f'dropdown2')
  
        
        from_led=Ledger.objects.get(ledger_number=from_ledger)
        to_led=Ledger.objects.get(ledger_number=to_ledger)
        delivery=DeliveryDetails.objects.get(id=invoice_no)
        
        amt=float(request.POST.get(f'd_total'))
        comment=request.POST.get(f'comment')
   
        quote=PaymentEntry(
            date = journal_date,
            voucherNo=voucher_no,
            invoice_no = invoice_no,
            invoice_date = invoice_date,
            narration = notes,
            comment=comment,
            from_ledger = from_led,
            to_ledger = to_led,
            debit_total = amt,
            credit_total=amt,
        )
        quote.save()
        
        delivery.pendingAmt-=Decimal(amt)
        
        # delivery.save()
        if delivery.pendingAmt==0:
            delivery.payment='paid'
        delivery.save()
       
        ledger_entry=LedgerEntry(
            delivery = delivery,
            order = delivery.order,
            account =to_led,
            # Other fields for ledger entry details
            description = f"Payment For Purchase OrderId:-{delivery.order.id} DeliveryID:-{delivery.id}" ,
            debit_amount = Decimal(request.POST.get(f'd_total')),
            credit_amount = 0,
        ).save()
       
        ledger_entry=LedgerEntry(
                    delivery = delivery,
                    order = delivery.order,
                    account =from_led,
                    # Other fields for ledger entry details
                    description = f"Payment For OrderId:-{delivery.order.id} DeliveryID:-{delivery.id} comment:-{comment}" ,
                    debit_amount = 0,
                    credit_amount = Decimal(request.POST.get(f'd_total')),
                ).save()
        
    
   
        

        # Redirect to the detail view for the created quotation
        return redirect('payments')
        
        
                  
    latest_quotation = PaymentEntry.objects.order_by().last()
    next_quotation_number = latest_quotation.voucherNo + 1 if latest_quotation else 100
    return render(request, 'vouchers/Payment/payment.html',  context={
        'username':request.user,'account_list':to_ledger_accounts,
    'next_quotation_number':next_quotation_number,'purchases':purchase,'pay':pay})


def reciept(request):
                
                    

    purchase=SalesDeliveryDetails.objects.filter(payment__in=['due','pending'],row_type='delivery')
    pay = Ledger.objects.filter(group__group_name__in=['BANK ACCOUNTS', 'CASH-IN-HAND'])
    to_ledger_accounts = Ledger.objects.exclude(group__group_name__in=['BANK ACCOUNTS', 'CASH-IN-HAND'])

   

    if request.method=='POST':
        # Extract keys that match the pattern 'cat{number}', 'sub{number}', 'ref{number}', etc.
        
        # Handle POST request and process the form data
        journal_date = request.POST.get('journal_date')
        voucher_no = request.POST.get('voucher_no')
        
        invoice_no = request.POST.get('invoice_no')
        notes = request.POST.get('notes')
       
        
        invoice_date = request.POST.get('invoice_date')
        
        from_ledger = request.POST.get(f'dropdown1')
        to_ledger=request.POST.get(f'dropdown2')
  
        
        from_led=Ledger.objects.get(ledger_number=from_ledger)
        to_led=Ledger.objects.get(ledger_number=to_ledger)
        delivery=SalesDeliveryDetails.objects.get(id=invoice_no)
        
        amt=float(request.POST.get(f'd_total'))
        comment=request.POST.get(f'comment')
   
        quote=RecieptEntry(
            date = journal_date,
            voucherNo=voucher_no,
            invoice_no = invoice_no,
            invoice_date = invoice_date,
            narration = notes,
            comment=comment,
            from_ledger = from_led,
            to_ledger = to_led,
            debit_total = amt,
            credit_total=amt,
        )
        quote.save()

        delivery.payment='recieved'
        delivery.save()
        sq=SalesQuotation.objects.get(quotation_number=delivery.OrderFk.quotation_number)
        ledger_entry=LedgerEntry(
            salesdelivery = delivery,
            saleorder = sq,
            account =to_led,
            # Other fields for ledger entry details
            description = f"Payment Recieved For Purchase OrderId:-{delivery.order.id} DeliveryID:-{delivery.id}" ,
            debit_amount = Decimal(request.POST.get(f'd_total')),
            credit_amount = 0,
        ).save()
       
        ledger_entry=LedgerEntry(
                    salesdelivery = delivery,
                    saleorder = sq,
                    account =from_led,
                    # Other fields for ledger entry details
                    description = f"Payment Recieved For OrderId:-{delivery.order.id} DeliveryID:-{delivery.id} comment:-{comment}" ,
                    debit_amount = 0,
                    credit_amount = Decimal(request.POST.get(f'd_total')),
                ).save()
        
    
   
        

        # Redirect to the detail view for the created quotation
        return redirect('reciepts')
        
        
                  
    latest_quotation = RecieptEntry.objects.order_by().last()
    next_quotation_number = latest_quotation.voucherNo + 1 if latest_quotation else 100
    return render(request, 'vouchers/Reciept/receiptEntry.html',  context={
        'username':request.user,'account_list':to_ledger_accounts,
    'next_quotation_number':next_quotation_number,'purchases':purchase,'pay':pay})



def contra(request):
                
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    account = VoucherLedgerVisibility.objects.get(voucher_type='CV')

    # Get all ledgers under the selected groups
    selected_group_numbers = account.selected_groups.values_list('group_number', flat=True)
    ledgers_under_selected_groups = Ledger.objects.filter(
        Q(group__group_number__in=selected_group_numbers) |
        Q(group__primary_group__primary_group_number__in=selected_group_numbers)
    )

    # Now `ledgers_under_selected_groups` contains all ledgers under the selected groups
    for ledger in ledgers_under_selected_groups:
   
        if request.method=='POST':
            # Extract keys that match the pattern 'cat{number}', 'sub{number}', 'ref{number}', etc.
            
            # Handle POST request and process the form data
            journal_date = request.POST.get('journal_date')
            voucher_no = request.POST.get('voucher_no')
            
            invoice_no = request.POST.get('invoice_no')
            notes = request.POST.get('notes')
            
            invoice_date = request.POST.get('invoice_date')
            
            
            d_total = float(request.POST.get('d_total'))
            c_total = float(request.POST.get('c_total'))

            count=int(request.POST.get('count'))
            quote=ContraEntry(
                date = journal_date,
                voucherNo=voucher_no,
                invoice_no=invoice_no,
                invoice_date=invoice_date,
                narration = notes,
                debit_total = d_total,  
                credit_total = c_total, 
            )
            quote.save()
            # Add a discount field if you intend to use it

    
            for index in range(1,count+1):
                    print(index)
                    led = request.POST.get(f'dropdown{index}')
                    try:
                        cred=float(request.POST.get(f'deb{index}'))
                    except:
                        cred=0.00
                    try:
                        deb=float(request.POST.get(f'cre{index}'))
                    except:
                        deb=0.00
                    comment=request.POST.get(f'nar{index}')
                    
                    # Extract the index from the key (e.g., dropdown1, dropdown2, etc.)
                    ContraEntryRow.objects.create(
                        # quotation=quotation,
                        entryFk=quote,
                        ledger=Ledger.objects.get(ledger_number=led),
                        comment=comment,
                        
                        debit=cred,
                        credit=deb,

                        # Add other fields as needed
                    )



            # Redirect to the detail view for the created quotation
            return redirect('contra')
            
            
                  
    latest_quotation = ContraEntry.objects.order_by().last()
    next_quotation_number = latest_quotation.voucherNo + 1 if latest_quotation else 100
    return render(request, 'vouchers/Contra/contra.html',  context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':ledgers_under_selected_groups,
    'next_quotation_number':next_quotation_number})





def credit_note(request):
                
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    account = VoucherLedgerVisibility.objects.get(voucher_type='CNV')

    # Get all ledgers under the selected groups
    selected_group_numbers = account.selected_groups.values_list('group_number', flat=True)
    ledgers_under_selected_groups = Ledger.objects.filter(
        Q(group__group_number__in=selected_group_numbers) |
        Q(group__primary_group__primary_group_number__in=selected_group_numbers)
    )

    if request.method=='POST':
        # Extract keys that match the pattern 'cat{number}', 'sub{number}', 'ref{number}', etc.
        
        # Handle POST request and process the form data
        journal_date = request.POST.get('journal_date')
        voucher_no = request.POST.get('voucher_no')
        
        invoice_no = request.POST.get('invoice_no')
        notes = request.POST.get('notes')
        
        invoice_date = request.POST.get('invoice_date')
        
        
        d_total = float(request.POST.get('d_total'))
        c_total = float(request.POST.get('c_total'))

        count=int(request.POST.get('count'))
        quote=CreditNoteEntry(
            date = journal_date,
            voucherNo=voucher_no,
            invoice_no=invoice_no,
            invoice_date=invoice_date,
            
            narration = notes,
            debit_total = d_total,  
            credit_total = c_total, 
        )
        quote.save()
        # Add a discount field if you intend to use it

 
        for index in range(1,count+1):
                led = request.POST.get(f'dropdown{index}')
                try:
                    cred=float(request.POST.get(f'deb{index}'))
                except:
                    cred=0.00
                try:
                    deb=float(request.POST.get(f'cre{index}'))
                except:
                    deb=0.00
                comment=request.POST.get(f'nar{index}')
                
                # Extract the index from the key (e.g., dropdown1, dropdown2, etc.)
                creditNoteEntryRow.objects.create(
                    # quotation=quotation,
                    entryFk=quote,
                    ledger=Ledger.objects.get(ledger_number=led),
                    comment=comment,
                    
                    debit=cred,
                    credit=deb,

                    # Add other fields as needed
                )



        # Redirect to the detail view for the created quotation
        return redirect('credit-note-entries')
        
        
                  
    latest_quotation = CreditNoteEntry.objects.order_by().last()
    next_quotation_number = latest_quotation.voucherNo + 1 if latest_quotation else 100
    return render(request, 'vouchers/Credit/credit_note.html',  context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':ledgers_under_selected_groups,
    'next_quotation_number':next_quotation_number})


def debit_note(request):
                
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    account = VoucherLedgerVisibility.objects.get(voucher_type='DNV')

    # Get all ledgers under the selected groups
    selected_group_numbers = account.selected_groups.values_list('group_number', flat=True)
    ledgers_under_selected_groups = Ledger.objects.filter(
        Q(group__group_number__in=selected_group_numbers) |
        Q(group__primary_group__primary_group_number__in=selected_group_numbers)
    )

    if request.method=='POST':
        # Extract keys that match the pattern 'cat{number}', 'sub{number}', 'ref{number}', etc.
        
        # Handle POST request and process the form data
        journal_date = request.POST.get('journal_date')
        voucher_no = request.POST.get('voucher_no')
        
        invoice_no = request.POST.get('invoice_no')
        notes = request.POST.get('notes')
        
        invoice_date = request.POST.get('invoice_date')
        
        
        d_total = float(request.POST.get('d_total'))
        c_total = float(request.POST.get('c_total'))

        count=int(request.POST.get('count'))
        quote=DebitNoteEntry(
            date = journal_date,
            voucherNo=voucher_no,
            invoice_no=invoice_no,
            invoice_date=invoice_date,
            
            narration = notes,
            debit_total = d_total,  
            credit_total = c_total, 
        )
        quote.save()
        # Add a discount field if you intend to use it

 
        for index in range(1,count+1):
                led = request.POST.get(f'dropdown{index}')
                try:
                    cred=float(request.POST.get(f'deb{index}'))
                except:
                    cred=0.00
                try:
                    deb=float(request.POST.get(f'cre{index}'))
                except:
                    deb=0.00
                comment=request.POST.get(f'nar{index}')
                
                # Extract the index from the key (e.g., dropdown1, dropdown2, etc.)
                DebitNoteEntryRow.objects.create(
                    # quotation=quotation,
                    entryFk=quote,
                    ledger=Ledger.objects.get(ledger_number=led),
                    comment=comment,
                    
                    debit=cred,
                    credit=deb,

                    # Add other fields as needed
                )


        # Redirect to the detail view for the created quotation
        return redirect('debit-note-entries')
        
        
                  
    latest_quotation = DebitNoteEntry.objects.order_by().last()
    next_quotation_number = latest_quotation.voucherNo + 1 if latest_quotation else 100
    return render(request, 'vouchers/Debit/debit_note.html',  context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':ledgers_under_selected_groups,
    'next_quotation_number':next_quotation_number})























    
































































def autocomplete(request):
    term = request.GET.get('term')
    # Implement your logic to fetch suggestions based on the input term
    suggestions = Ledger.objects.filter(ledger_name__icontains=term).values_list('ledger_name', flat=True)
    return JsonResponse(list(suggestions), safe=False)


#######################Ledgers Create and Chart Of account###################
def Account_chart(request):
    Category_list=Group.objects.all()
    # category_data = serializers.serialize('json', Category_list)
    accounts = Ledger.objects.all()

    return render(request, 'accountsCharts.html', context={
        'username':request.user,'IndividualAccount_list':accounts,'account_subcategory':Category_list
    })



def primaryGroup(request):
    IndividualAccount_list=Primary_Group.objects.all()

    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    
    if request.method=="POST":
        if 'save' in request.POST:
            data = request.POST # Replace with your actual QueryDict data
            primaryType = data.get(f'primaryType')
            GroupName = data.get(f'GroupName')
            prime=Primary_Group(primary_group_name=GroupName,
                        primary_group_type=primaryType)
            prime.save()
    if request.method=="POST":
        if 'delete' in request.POST:
            account_numberc = request.POST.get('accountNumberc')
            # Assuming Primary_Group is your model
            prime_del = get_object_or_404(Primary_Group, primary_group_number=account_numberc)
            prime_del.delete()
    
    
    return render(request, 'accountingPrimaryGroup.html', context={
        'username':request.user,'IndividualAccount_list':IndividualAccount_list,'currency':currency,
    })
 
def groupPage(request):
    IndividualAccount_list=Group.objects.all()
    account_subcategory=Primary_Group.objects.all()
    

    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    
    if request.method=="POST":
        if 'save' in request.POST:
            data = request.POST # Replace with your actual QueryDict data
            primaryGroupName = data.get(f'primaryGroupName')
            GroupName = data.get(f'GroupName')
            dr=Primary_Group.objects.get(primary_group_name=primaryGroupName)
            print(dr)
            prime=Group(group_name=GroupName,
                        primary_group=dr)
            prime.save()
    if request.method=="POST":
        if 'delete' in request.POST:
            account_numberc = request.POST.get('accountNumberc')
            print(account_numberc,'hhhhhhhhhhh')
            # Assuming Primary_Group is your model
            prime_del = get_object_or_404(Group, group_number=account_numberc)
            prime_del.delete()
    
    
    return render(request, 'accountingroup.html', context={
        
        'account_subcategory':account_subcategory,'username':request.user,'IndividualAccount_list':IndividualAccount_list,'currency':currency,
    })
 


def journalEntries(request):
    normalized_data = []
    journal_page_obj=JournalEntryRow.objects.all()

    for journal_entry in journal_page_obj:
        entry_data = {
            
            'voucherNo': journal_entry.entryFk.voucherNo,
            'voucherCode': journal_entry.entryFk.voucherCode,
            'date': journal_entry.entryFk.date,
            'invoice_no': journal_entry.entryFk.invoice_no,
            'invoice_date': journal_entry.entryFk.invoice_date,
            'narration': journal_entry.entryFk.narration,
            'debit_total': journal_entry.entryFk.debit_total,
            'credit_total': journal_entry.entryFk.credit_total,
            
            'ledger_name': journal_entry.ledger.ledger_name,
            'comment': journal_entry.comment,
            'debit': journal_entry.debit,
            'credit': journal_entry.credit,
        }

  

        normalized_data.append(entry_data)
    return render(request, 'vouchers/Journal/journalEntries.html', context={'journal_page_obj':normalized_data})
def Gernal_Ledger(request):
    if request.user.account_type.name == "Customer" or request.user.account_type.name == "Supplier":
        accounts = Ledger.objects.filter(ledgerUser=request.user)
    else:
        accounts = Ledger.objects.all()
    q = request.GET.get('q')
    types = ''
    led = ''
    lis = []
    result = {}
    cat = ''
    subcat = ''
    total_debit = 0
    total_credit = 0
    total_balance = 0

    if q:
        # Assuming you have a ForeignKey relationship between LedgerEntry and DeliveryDetails
        # and LedgerEntry has fields like debit_amount, credit_amount, and date
        ledgers = LedgerEntry.objects.filter(account=Ledger.objects.get(ledger_number=q))

        # Calculate running balances and totals
        running_balance = 0
        for entry in ledgers:
            entry.balance = running_balance + entry.debit_amount - entry.credit_amount
            running_balance = entry.balance

            # Update total debit and credit
            total_debit += entry.debit_amount
            total_credit += entry.credit_amount

            if entry.balance < 0:
                entry.balance = entry.balance * -1
                types = 'Cr'
            else:
                types = 'Dr'

        # Calculate total balance
        total_balance = total_debit - total_credit
        if total_balance<0:
            total_balance=total_balance*-1
        # Pass the ledger entries and totals to the template
        lis = ledgers
        
        led = Ledger.objects.get(ledger_number=q)
        

    return render(request, 'ledgers/ledger.html', context={'heading': led, 'cat': cat, 'subcat': subcat,
                                                             'username': request.user, 'account_list': accounts,
                                                             'led': lis, 'result': result,
                                                             'types': types,
                                                             'total_debit': total_debit,
                                                             'total_credit': total_credit,
                                                             'total_balance': total_balance})


# views.py
from django.shortcuts import render
from .models import LedgerEntry
from .filters import LedgerEntryFilter
from django.db.models import Q

# Filter based on the first condition

def LedgerEntries(request):
    if request.user.account_type.name == "Customer" :
        ledger_entries = LedgerEntry.objects.filter(saleorder__customer=request.user)
        
    elif request.user.account_type.name == "Supplier":
        entries_condition1 = LedgerEntry.objects.filter(order__user=request.user)

        # Filter based on the second condition
        entries_condition2 = LedgerEntry.objects.filter(account=Ledger.objects.get(ledgerUser=request.user))

        # Combine the sets using union (|) or intersection (&) based on your requirement
        ledger_entries = entries_condition1 | entries_condition2
        # ledger_entries = LedgerEntry.objects.filter(order__user=request.user,account=Ledger.objects.get(ledgerUser=request.user))
    else:
        ledger_entries = LedgerEntry.objects.all()
    print(ledger_entries)

    # Apply the date range filter
    ledger_filter = LedgerEntryFilter(request.GET, queryset=ledger_entries)

    return render(request, 'ledgers/ledgerEntries.html', context={'ledger_filter': ledger_filter})



def check_delivery_details(request,delivery_id):
    ledg=LedgerEntry.objects.get(id=delivery_id)
    
    if ledg.saleorder :
        delivery=ledg.salesdelivery
        return render(request, 'ledgers/sale_delivery_details.html', context={'delivery': delivery})
    else:
        delivery=ledg.delivery
    
        return render(request, 'ledgers/delivery_details.html', context={'delivery': delivery})








def action_ledger(request):
    if request.method == "POST":
        data = request.POST  # Get the POST data
        action = data.get("action")
    

        if action == "delete":
            # Handle delete action
            account_number = data.get("ledger_number")

            # Delete the account using the account number
            try:
                account_to_delete = Ledger.objects.get(ledger_number=account_number)
                account_to_delete.delete()
                return JsonResponse({'success': True, 'message': 'Account deleted successfully'})
            except Ledger.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Account not found'})
        elif action == "save":
            # Handle edit action
            account_num = data.get("account_number")
            new_account_name = data.get("accountname").replace(' ','_')
            category = Group.objects.get(group_number=account_num)
            new_account = Ledger(group=category, ledger_name=new_account_name)

        # Save the new Account object to the database
            new_account.save()
            
            return JsonResponse({'success': True, 'message': 'Account Added successfully'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})

def action(request):
    if request.method == "POST":
        data = request.POST  # Get the POST data
        action = data.get("action")
    

        if action == "delete":
            # Handle delete action
            account_number = data.get("account_number")

            # Delete the account using the account number
            try:
                account_to_delete = Ledger.objects.get(ledger_number=account_number)
                account_to_delete.delete()
                return JsonResponse({'success': True, 'message': 'Account deleted successfully'})
            except Ledger.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Account not found'})
        elif action == "save":
            # Handle edit action
            account_num = data.get("account_number")
            new_account_name = data.get("accountname").replace(' ','_')
            category = Group.objects.get(group_number=account_num)
            new_account = Ledger(group=category, ledger_name=new_account_name)

        # Save the new Account object to the database
            new_account.save()
            
            return JsonResponse({'success': True, 'message': 'Account Added successfully'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})







def paymentEntry(request):
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    banks = Ledger.objects.filter(group__group_name__in=["BANK ACCOUNTS"])
    cash= Ledger.objects.filter(group__group_name__in=["Cash"])
    accounts = Ledger.objects.exclude(group__group_name__in=["Cash", "BANK ACCOUNTS"])
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    return render(request, 'paymentVoucher.html', context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':accounts,'currency':currency,'banks':banks,
        'cashs':cash
    })
def paymentList(request):
    print(request.user.username)    
               

    return render(request, 'paymentList.html', context={
        'username':request.user
    })

def submit_payment(request):
    invoicedate=voucher_no=invoicedate=transactionType=bankAmt_inWords=Banknotes=total=None
    cashtransactionType=transactionType=bank_currency=chequeNumber=chequeDate=clearanceDate=None
    bankDr=bank_currency=transaction_type=cheque_no=chequeDate=clearanceDate=None
    
    try:
        data = request.POST # Replace with your actual QueryDict data
        voucher_no = data.get(f'bankvoucher_no')
        invoicedate = data.get(f'bankjournal_date')
        ttype = data.get(f'ttype')
        bankAmt_inWords = data.get(f'bankAmt_inWords')
        bankAmt_in_No =data.get(f'bankAmt_in_No')
        Banknotes = data.get(f'Banknotes')
        RecievedFrom = data.get(f'RecievedFrom')
        total = data.get(f'total')
        remark = data.get(f'cashTransaction_Id')
        
        if ttype=='cash':
            cashtransactionType = data.get(f'cashtransactionType')
            
            deb_account = Ledger.objects.get(ledger_name=cashtransactionType.split('-')[-1])  # Replace with the appropriate field
            deb_subcategory = deb_account.group
            deb_category = deb_account.group.primary_group
            method='cash'  
        
        else:
            transactionType =data.get(f'transactionType')
            if transactionType=='Cheque':
                chequeNumber =data.get(f'chequeNumber')
                chequeDate = data.get(f'chequeDate')
                clearanceDate = data.get(f'clearanceDate', 'YYYY-MM-DD')
            bank_currency = data.get(f'bank_currency')
            
            bankDr = data.get(f'bankDr')
            deb_account = Ledger.objects.get(ledger_name=bankDr)  # Replace with the appropriate field
            deb_subcategory = deb_account.group
            deb_category = deb_account.group.primary_group  
            method='bank'  
            
        try:
            # Loop through the data to create and save JournalEntries instances
            for i in range(1, 10):  # Assuming you have four sets of data (1 to 4)
                # Replace 'voucher' with the actual key in your QueryDict
                # narration = data.get(f'nar{i}')  # Replace 'nar' with the actual key in your QueryDict
                category_name = data.get(f'cat{i}')
                subcategory_name = data.get(f'sub{i}')
                ref = data.get(f'ref{i}', 0)
                bill = data.get(f'bill{i}', 0)
                amt = data.get(f'amt{i}', 0)
                cred = data.get(f'cred{i}', 0)
                account_num=data.get(f'dropdown{i}', 0)  # Default to 0 if not present or invalid
                print(account_num)
                # try:
                        # Fetch the corresponding Category, Subcategory, and IndividualAccount instances
                cre_account = Ledger.objects.get(ledger_number=int(account_num))  # Replace with the appropriate field
                cre_subcategory = cre_account.group
                cre_category = cre_account.group.primary_group
                # Create and save the JournalEntries instance
                entry = Payment(
                    date=invoicedate,
                    voucherNo=voucher_no.split('-')[-1],
                    voucherCode=voucher_no,
                    receipt_method=method,
                    amount_in_words=bankAmt_inWords,
                    amount_in_numbers=bankAmt_in_No,
                    received_from=RecievedFrom,
                    remarks=remark,
                    narration=Banknotes,
                    d_ledger=deb_account,
                    d_primary_group=deb_category,
                    d_group=deb_subcategory,
                    c_ledger=cre_account,
                    c_primary_group=cre_subcategory,
                    c_group=cre_category,
                    reference=ref,
                    reference_bill_number=bill,
                    reference_bill_amount = amt,
                    debit = cred,
                    transaction_currency = bank_currency,
                    clearance_date =clearanceDate,
                    transaction_type = transactionType,
                    cheque_no = chequeNumber,
                    bank_date = chequeDate,

                )
                entry.save()
        except Primary_Group.DoesNotExist:
            pass
        except Group.DoesNotExist:
            pass
        except Ledger.DoesNotExist:
            pass
        entry_response = {
                "voucherNo": entry.voucherNo,
                "voucherCode": entry.voucherCode,  # Assuming you have a 'voucherCode' field in your model
                "account": entry.d_ledger.ledger_name,  # Assuming 'account_name' is the relevant field in 'IndividualAccount'
            }
        print(entry_response)
        return JsonResponse({'success': True, 'message': 'Sucess'})            
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': 'Invalid request'})
    




def recieptEntry(request):
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    banks = Ledger.objects.filter(group__group_name__in=["BANK ACCOUNTS"])
    cash= Ledger.objects.filter(group__group_name__in=["Cash"])
    accounts = Ledger.objects.exclude(group__group_name__in=["Cash", "BANK ACCOUNTS"])
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    return render(request, 'recieptVoucher.html', context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':accounts,'currency':currency,'banks':banks,
        'cashs':cash
    })
  
def submit_reciept(request):
    invoicedate=voucher_no=invoicedate=transactionType=bankAmt_inWords=Banknotes=total=None
    cashtransactionType=transactionType=bank_currency=chequeNumber=chequeDate=clearanceDate=None
    bankDr=bank_currency=transaction_type=cheque_no=chequeDate=clearanceDate=None
    
    try:
        data = request.POST # Replace with your actual QueryDict data
        voucher_no = data.get(f'bankvoucher_no')
        invoicedate = data.get(f'bankjournal_date')
        ttype = data.get(f'ttype')
        bankAmt_inWords = data.get(f'bankAmt_inWords')
        bankAmt_in_No =data.get(f'bankAmt_in_No')
        Banknotes = data.get(f'Banknotes')
        RecievedFrom = data.get(f'RecievedFrom')
        total = data.get(f'total')
        remark = data.get(f'cashTransaction_Id')
        
        if ttype=='cash':
            cashtransactionType = data.get(f'cashtransactionType')
            
            deb_account = Ledger.objects.get(ledger_name=cashtransactionType.split('-')[-1])  # Replace with the appropriate field
            deb_subcategory = deb_account.group
            deb_category = deb_account.group.primary_group
            method='cash'  
        
        else:
            transactionType =data.get(f'transactionType')
            if transactionType=='Cheque':
                chequeNumber =data.get(f'chequeNumber')
                chequeDate = data.get(f'chequeDate')
                clearanceDate = data.get(f'clearanceDate', 'YYYY-MM-DD')
            bank_currency = data.get(f'bank_currency')
            
            bankDr = data.get(f'bankDr')
            deb_account = Ledger.objects.get(ledger_name=bankDr)  # Replace with the appropriate field
            deb_subcategory = deb_account.group
            deb_category = deb_account.group.primary_group  
            method='bank'  
            
        try:
            # Loop through the data to create and save JournalEntries instances
            for i in range(1, 10):  # Assuming you have four sets of data (1 to 4)
                # Replace 'voucher' with the actual key in your QueryDict
                # narration = data.get(f'nar{i}')  # Replace 'nar' with the actual key in your QueryDict
                category_name = data.get(f'cat{i}')
                subcategory_name = data.get(f'sub{i}')
                ref = data.get(f'ref{i}', 0)
                bill = data.get(f'bill{i}', 0)
                amt = data.get(f'amt{i}', 0)
                cred = data.get(f'cred{i}', 0)
                account_num=data.get(f'dropdown{i}', 0)  # Default to 0 if not present or invalid
                print(account_num)
                # try:
                        # Fetch the corresponding Category, Subcategory, and IndividualAccount instances
                cre_account = Ledger.objects.get(ledger_number=int(account_num))  # Replace with the appropriate field
                cre_subcategory = cre_account.group
                cre_category = cre_account.group.primary_group
                # Create and save the JournalEntries instance
                entry = Receipt(
                    date=invoicedate,
                    voucherNo=voucher_no.split('-')[-1],
                    voucherCode=voucher_no,
                    receipt_method=method,
                    amount_in_words=bankAmt_inWords,
                    amount_in_numbers=bankAmt_in_No,
                    received_from=RecievedFrom,
                    remarks=remark,
                    narration=Banknotes,
                    d_ledger=deb_account,
                    d_primary_group=deb_category,
                    d_group=deb_subcategory,
                    c_ledger=cre_account,
                    c_primary_group=cre_subcategory,
                    c_group=cre_category,
                    reference=ref,
                    reference_bill_number=bill,
                    reference_bill_amount = amt,
                    debit = cred,
                    transaction_currency = bank_currency,
                    clearance_date =clearanceDate,
                    transaction_type = transactionType,
                    cheque_no = chequeNumber,
                    bank_date = chequeDate,

                )
                entry.save()
        except Primary_Group.DoesNotExist:
            pass
        except Group.DoesNotExist:
            pass
        except Ledger.DoesNotExist:
            pass
        entry_response = {
                "voucherNo": entry.voucherNo,
                "voucherCode": entry.voucherCode,  # Assuming you have a 'voucherCode' field in your model
                "account": entry.d_ledger.ledger_name,  # Assuming 'account_name' is the relevant field in 'IndividualAccount'
            }
        print(entry_response)
        return JsonResponse({'success': True, 'message': 'Sucess'})            
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': 'Invalid request'})
    
def recieptList(request):
    print(request.user.username)    
               

    return render(request, 'recieptList.html', context={
        'username':request.user
    })
    
    
    
    
def salesEntry(request):
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    debit = Ledger.objects.filter(group__group_name__in=["Sales"])
    accounts = Ledger.objects.exclude(group__group_name__in=["Sales"])
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    return render(request, 'sales_voucher.html', context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':accounts,'currency':currency,'debit':debit,
    })  
def submitSales(request):
    tax_per=10
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    debit = Ledger.objects.filter(group__group_name__in=["Sales"])
    accounts = Ledger.objects.exclude(group__group_name__in=["Sales"])
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    
    
    # try:
    data = request.POST # Replace with your actual QueryDict data
    voucher_no = data.get(f'voucher')
    invoicedate = data.get(f'invoice_date')
    debit_led = data.get(f'debit_led')
    total = data.get(f'd_total')
    taxed=(10/100)*float(total)
    final=float(total)+taxed
    deb_category = Primary_Group.objects.get(primary_group_name='INCOME')
    deb_subcategory = Group.objects.get(group_name='Sales')
    deb_account = Ledger.objects.get(ledger_name=debit_led.split('-')[-1])  # Replace with the appropriate field
            
    
    
    try:
    # Loop through the data to create and save JournalEntries instances
        for i in range(1, 10):  # Assuming you have four sets of data (1 to 4)
            # Replace 'voucher' with the actual key in your QueryDict
            # narration = data.get(f'nar{i}')  # Replace 'nar' with the actual key in your QueryDict
            category_name = data.get(f'cat{i}')
            subcategory_name = data.get(f'sub{i}')
            desc = data.get(f'ref{i}', 0)
            qty = data.get(f'qty{i}', 0)
            
            unt = data.get(f'unt{i}', 0)
            
            amt = data.get(f'amt{i}', 0)
            
            

            account_num=data.get(f'dropdown{i}', 0)  # Default to 0 if not present or invalid
            
            try:
                    # Fetch the corresponding Category, Subcategory, and IndividualAccount instances
                
                cre_account = Ledger.objects.get(ledger_number=account_num)  # Replace with the appropriate field
                cre_subcategory = cre_account.group
                cre_category = cre_account.group.primary_group
                
                # Create and save the JournalEntries instance
                entry = SalesReceipt(
                    date=invoicedate,
                    voucherNo=voucher_no.split('-')[-1],
                    voucherCode=voucher_no,
                    deb_primary_group=deb_category,
                    deb_group=deb_subcategory,
                    deb_ledger=deb_account,
                    cred_primary_group=cre_category,
                    cred_group=cre_subcategory,
                    cred_ledger=cre_account,
                    decsription=desc,
                    qty=int(qty),
                    untPrice=int(unt),
                    amount=float(amt),
                    total=float(total),
                    taxed=float(taxed),
                    final=float(final),
                    
                    
                        # You can set comments as needed
                )
                entry.save()
            except Primary_Group.DoesNotExist:
                pass
            except Group.DoesNotExist:
                pass
            except Ledger.DoesNotExist:
                pass
        entry_response = {
                    "voucherNo": entry.voucherNo,
                    "voucherCode": entry.voucherCode,  # Assuming you have a 'voucherCode' field in your model
                    "account": entry.deb_ledger.ledger_name,  # Assuming 'account_name' is the relevant field in 'IndividualAccount'
                }

        return JsonResponse({'success': True, 'message': 'Sucess'})            
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': 'Invalid request'}) 
from django.db.models import F

from django.db.models import Subquery, OuterRef
def salesList(request):
    unique_receipts = SalesReceipt.objects.filter(
    s_no=Subquery(
        SalesReceipt.objects.filter(voucherCode=OuterRef('voucherCode')).order_by('s_no').values('s_no')[:1]
    )
)
    # Sale_Receipt=SalesReceipt.objects.all()
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    banks = Ledger.objects.filter(group__group_name__in=["Bank Account"])
    cash= Ledger.objects.filter(group__group_name__in=["Cash"])
    accounts = Ledger.objects.exclude(group__group_name__in=["Cash", "Bank Account"])
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    print(unique_receipts)
    return render(request, 'sales_list.html', context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':accounts,'currency':currency,'banks':banks,
        'cashs':cash,'SalesReceipt':unique_receipts
    })  
  
  
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import FileResponse
  
  
def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "inline; filename=your_file.pdf"

    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, "Hello, world.")
    # Add more content here using the ReportLab API.

    p.showPage()
    p.save()

    return response
  


def item_detail(request, voucher_id):
    print(voucher_id)
    Sale_Receipt=SalesReceipt.objects.filter(voucherCode=voucher_id)
    print(Sale_Receipt)
    # item = get_object_or_404(Item, id=item_id)  # Retrieve the item based on its ID
    return render(request, 'salesvoucher_pdf.html', {'item': Sale_Receipt[0],'items': Sale_Receipt,})
  
  
  
  
  
  
  
  
  
  
  
  
  
  
    
        
        
        
        
        
        

  
  
    
def Trial_Balance(request):
                
    accounts = Ledger.objects.values('ledger_name',)  
    led=[]
    res={}
    resdeb=0
    rescred=0
    resbal=0
    
    for account in accounts:        
        ledgers=JournalEntries.objects.filter(ledger__ledger_name=account['ledger_name'])
        print()
        cred=0
        deb=0
        bal=0
        for row in ledgers:
            
      
 
    
            cred=cred+row.credit
            deb=deb+row.debit
            bal=deb-cred
            
        le={'type':account['ledger_name'],
            'deb':deb,'cred':cred,'bal':bal
        }
        led.append(le)
        resdeb=resdeb+deb
        rescred=rescred+cred
        resbal=resbal+bal
    result={
        'deb_result':resdeb,
        'cred_result':rescred,
        'bal_result':resbal
    }        
    return render(request, 'trial_balance.html', context={
        'username':request.user,'account_list':accounts,
        'data':led,'result':result
    }) 
    
def Profit_Loss(request):
    print(request.user.username)    
               

    return render(request, 'home.html', context={
        'username':request.user
    })
def Balance_sheet(request):
                
    print(request.user.username)    
               

    return render(request, 'home.html', context={
        'username':request.user
    })
    
    
    
def maintain(request):
                
    print(request.user.username)    
               

    return render(request, 'maintain.html', context={
        'username':request.user
    })




@login_required(login_url='login')
def accountingroup(request):
    return render(request,'accountingroup.html')

@login_required(login_url='login')
def accountingvoucher(request):
    return render(request,'accountingvoucher.html')
@login_required(login_url='login')
def accountingcurrency(request):
    return render(request,'accountingcurrency.html')


