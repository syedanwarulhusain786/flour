from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login,logout
from .models import *
# Create your views here.

def index(request):
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
                    
                        print('hi')
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



def logout(request):
    logout(request)
    return redirect('index')