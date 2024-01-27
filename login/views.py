from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login,logout
from .models import *
# Create your views here.
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.list import ListView
from .models import Billing_Company
from .forms import BillingCompanyForm
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Billing_Company
from .forms import BillingCompanyForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
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
# Your existing code...

@department_required(allowed_departments=['ACCOUNT', 'INVENTORY'])
@login_required(login_url='login')
def billing_company_update_view(request, pk):
    billing_company = get_object_or_404(Billing_Company, pk=pk)

    if request.method == 'POST':
        form = BillingCompanyForm(request.POST, request.FILES, instance=billing_company)
        if form.is_valid():
            form.save()
            # You can add additional logic here if needed
            return redirect('billing_company_list')
    else:
        form = BillingCompanyForm(instance=billing_company)

    return render(request, 'billing_company_form.html', {'form': form})

@department_required(allowed_departments=['ACCOUNT', 'INVENTORY'])
@login_required(login_url='login')
def billing_company_delete_view(request, pk):
    billing_company = get_object_or_404(Billing_Company, pk=pk)

    if request.method == 'POST':
        billing_company.delete()
        return redirect('billing_company_list')

    return render(request, 'billing_company_confirm_delete.html', {'billing_company': billing_company})
@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login')
def create_billing_company(request):
    template_name = 'billing_company_form.html'

    if request.method == 'POST':
        form = BillingCompanyForm(request.POST, request.FILES)
        if form.is_valid():
            billing_company = form.save()
            # You can add additional logic here if needed
            return redirect('billing_company_list')
    else:
        form = BillingCompanyForm()

    return render(request, template_name, {'form': form})
@department_required(allowed_departments=['ACCOUNT',"INVENTORY"])
@login_required(login_url='login')
def billing_company_list_view(request):
    billing_companies = Billing_Company.objects.all()
    return render(request, 'billing_company_list.html', {'billing_companies': billing_companies})
def index(request):
    user=request.user
    if user.is_authenticated:
        if user.company_id:
            if user.department_id:
                print(user.account_type.name)
                if user.department.name=='SALES':
                    login(request, user)
                    return redirect('sales')
                elif user.department.name=='ACCOUNT':
                    login(request, user)
                    return redirect('account')
                elif user.department.name=='NONE':
                    if user.account_type.name=='Supplier':
                        login(request, user)
                        return redirect('supplier-home')
                    elif user.account_type.name=='Customer':
                        login(request, user)
                        return redirect('customer_home')
                    elif user.account_type.name=='Agent':
                        login(request, user)
                        return redirect('customer_home')
             
                # login(request, user)
                # return redirect('home')  # Replace 'home' with your home page URL.
            else:
                message="No Department Alotted to You Please ask admin To allot department"
                return render(request, 'login.html', {'message': message}) 
        else:
            message="No Company is Alotted to You Please ask admin To allot Company"
            return render(request, 'login.html', {'message': message})
    if request.method=="POST":
        
        username=request.POST['Username']
        password=request.POST['Password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if Company.objects.exists():
                if user.company_id:
                    if user.department_id:
                        if user.department.name=='SALES':
                            login(request, user)
                            return redirect('sales')
                        elif user.department.name=='ACCOUNT':
                            login(request, user)
                            return redirect('account')
                        elif user.department.name=='NONE':
                            if user.account_type.name=='Supplier':
                                login(request, user)
                                return redirect('supplier-home')
                            elif user.account_type.name=='Customer':
                                login(request, user)
                                return redirect('customer_home')
                            elif user.account_type.name=='Agent':
                                login(request, user)
                                return redirect('customer_home')
                        # login(request, user)
                        # return redirect('home')  # Replace 'home' with your home page URL.
                    else:
                        message="No Department Alotted to You Please ask admin To allot department"
                        return render(request, 'login.html', {'message': message}) 
                else:
                    message="No Company is Alotted to You Please ask admin To allot Company"
                    return render(request, 'login.html', {'message': message}) 
            else:
                message="No Company Started Please Ask Admin To start one Company"
                return render(request, 'login.html', {'message': message}) 
        else:
            message="Invalid login credentials"
            return render(request, 'login.html', {'message': message})
    return render(request,'login.html')



def logou(request):
    logout(request)
    return redirect('login')