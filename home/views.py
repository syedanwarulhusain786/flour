from django.shortcuts import render, redirect 
# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    return render(request,'home.html')
