from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
import uuid
class AccountType(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('Supplier', 'Supplier'),
        ('HR_MANAGER', 'HR Manager'),
        ('ACCOUNTANT', 'Accountant'),
        ('Agent', 'Agent'),
        ('Customer', 'Customer'),
        # Add more choices as needed
    ]

    name = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES, unique=True)

    def __str__(self):
            return self.get_name_display()

    class Meta:
        verbose_name_plural = 'Account Types'



class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Company Name')
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    
    established_date = models.DateField(null=True, blank=True)
    employees = models.PositiveIntegerField(null=True, blank=True)
    revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    parent_company = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subsidiaries')
    
    facebook_url = models.URLField(null=True, blank=True)
    twitter_handle = models.CharField(max_length=50, null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    
    billing_address = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    postal_Code = models.TextField(null=True, blank=True)

    tax_id = models.CharField(max_length=50, null=True, blank=True)

    departments = models.ManyToManyField('Department', related_name='companies', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'
class TermsAndCondition(models.Model):
    termType = [
        ('PAYMENT', 'PAYMENT'),
        ('SHIPPING', 'SHIPPING'),
        ('DELIVERY', 'DELIVERY'),
        ('SERVICES', 'SERVICES'),
        # Add more choices as needed
    ]
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    
    name = models.CharField(max_length=100, verbose_name='TermsAndCondition', choices=termType)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'TermsAndConditions'        
        

class Department(models.Model):
    DEPARTMENT_CHOICES = [
        ('SALES', 'Sales'),
        ('ACCOUNT', 'Accounting'),
        ('INVENTORY', 'Inventory'),
        ('ADMIN', 'Administration'),
        ('NONE', 'None'),
        
        # Add more choices as needed
    ]
    name = models.CharField(max_length=100, verbose_name='Department Name', choices=DEPARTMENT_CHOICES)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Departments'
def get_image_filename(instance, filename):
    """Generate a unique filename for each uploaded image."""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"product_images/{filename}"
class CustomUser(AbstractUser):
    account_type = models.ForeignKey(AccountType, on_delete=models.SET_NULL, null=True, blank=True,max_length=50)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    telegram_id = models.CharField(max_length=50, null=True, blank=True)
    profilePic = models.ImageField(upload_to='product_images/', default="product_images/user-1.jpg")
    
    
    
    
