from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth import get_user_model
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from threading import current_thread
from django.utils import timezone
from accounting.models import Ledger
class UserStampedModel(models.Model):
    user = models.ForeignKey(
        'CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_updates'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            current_user = getattr(current_thread(), '_current_user', None)
            if current_user:
                self.user = current_user
        super(UserStampedModel, self).save(*args, **kwargs)
        
        
        
class AccountType(UserStampedModel):
    ACCOUNT_TYPE_CHOICES = [
        ('Supplier', 'Supplier'),
        ('Accountant', 'Accountant'),
        ('Agent', 'Agent'),
        ('Customer', 'Customer'),
        # Add more choices as needed
    ]

    name = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES, unique=True)

    def __str__(self):
            return self.get_name_display()

    class Meta:
        verbose_name_plural = 'Account Types'



class Company(UserStampedModel):
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
class TermsAndCondition(UserStampedModel):
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
        

class Department(UserStampedModel):
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




class CustomUser(UserStampedModel,AbstractUser):
    account_type = models.ForeignKey(AccountType, on_delete=models.SET_NULL, null=True, blank=True,max_length=50)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    ledger = models.ForeignKey(Ledger, on_delete=models.SET_NULL,null=True, blank=True)
    ERPUsers_code = models.CharField(max_length=50)
    ERPUsers_name = models.CharField(max_length=255)
    credit_period = models.IntegerField(default=7)
    mobile = models.CharField(max_length=255,null=True, blank=True)
    phone = models.CharField(max_length=20,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    ifsc =  models.CharField(max_length=50,null=True, blank=True)
    bank_account = models.CharField(max_length=50,null=True, blank=True)
    gst_no = models.CharField(max_length=20,null=True, blank=True)
    pan = models.CharField(max_length=20,null=True, blank=True)
    opening_balance = models.IntegerField(null=True, blank=True)
    pinCode = models.CharField(max_length=20,null=True, blank=True )
    address = models.TextField(null=True, blank=True)
    telegram_id = models.CharField(max_length=50, null=True, blank=True)
    profilePic = models.ImageField(upload_to='product_images/', default="product_images/user-1.jpg")
    commission = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,default=0.0)
    def save(self, *args, **kwargs):
        self.ERPUsers_name = f"{self.first_name} {self.last_name}"
        super(CustomUser, self).save(*args, **kwargs)
        
        
        
        
        
        
        
class Billing_Company(UserStampedModel):
    name = models.CharField(max_length=255, verbose_name='BillingCompany')
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    
