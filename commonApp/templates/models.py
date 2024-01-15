import uuid
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum  


from login.models import *

from decimal import Decimal
def get_image_filename(instance, filename):
    """Generate a unique filename for each uploaded image."""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"product_images/{filename}"



class Material(models.Model):
    PIECE = 'Piece'
    LITER = 'Liter'
    METER = 'Meter'
    CMS = 'Centimeter'

    UNIT_CHOICES = [
        (PIECE, 'Piece'),
        (LITER, 'Liter'),
        (METER, 'Meter'),
        (CMS, 'Centimeter'),
    ]
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    unit_of_measurement = models.CharField(max_length=10, choices=UNIT_CHOICES, default=PIECE)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    

    def __str__(self):
        return self.name
    
class ProductBrand(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    

    def __str__(self):
        return self.name   

    

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    productCost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    productSelling = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    brand = models.ForeignKey(ProductBrand, on_delete=models.PROTECT)
    
    image0 = models.ImageField(upload_to=get_image_filename, blank=True, null=True)
    image1 = models.ImageField(upload_to=get_image_filename, blank=True, null=True)
    image2 = models.ImageField(upload_to=get_image_filename, blank=True, null=True)
    image3 = models.ImageField(upload_to=get_image_filename, blank=True, null=True)
    image4 = models.ImageField(upload_to=get_image_filename, blank=True, null=True)
    image5 = models.ImageField(upload_to=get_image_filename, blank=True, null=True)
    image6 = models.ImageField(upload_to=get_image_filename, blank=True, null=True)
    image7 = models.ImageField(upload_to=get_image_filename, blank=True, null=True)
    image8 = models.ImageField(upload_to=get_image_filename, blank=True, null=True)
    image9 = models.ImageField(upload_to=get_image_filename, blank=True, null=True)
    
    packaging_products = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='sales_products')    
    def __str__(self):
        return self.name

    
class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_per_piece = models.DecimalField(max_digits=10, decimal_places=2)
    material =models.ManyToManyField(Material)
    




class Order(models.Model):
    APPROVED = 'approved'
    DISAPPROVED = 'disapproved'
    PENDING = 'pending'
    STATUS_CHOICES = [
        (APPROVED, 'Approved'),
        (DISAPPROVED, 'Disapproved'),
        (PENDING, 'Pending'),
    ]
    user = models.ForeignKey('login.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
    
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=255)  # New field to store product name
    quantity = models.PositiveIntegerField()
    price_per_quantal = models.DecimalField(max_digits=20, decimal_places=2)
    end_delivery_date = models.DateField(null=True, blank=True)
    supplier_type= models.CharField(max_length=255) 
    agent_commission_per_quantal = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    final_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    is_approved = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    order_date=models.DateField(auto_now_add=True,null=True, blank=True)
    quantity_left=models.FloatField(default=0)
    
    def __str__(self):
            return f"Order Id {self.id} User "

    
class DeliveryDetails(models.Model):
    ROW_TYPE_CHOICES = [
    ('dispatch', 'Dispatch'),
    ('delivery', 'Delivery'),
    ]
    status_row = [
    ('pending', 'Pending'),
    ('delivered', 'Delivered'),
    ]
    payment_row = [
    ('pending', 'Pending'),
    
    ('due', 'Due'),
    ('paid', 'Paid'),
    ]
    created_at=models.DateField(auto_now_add=True,null=True, blank=True)

    user = models.ForeignKey('login.CustomUser', on_delete=models.CASCADE)
    billing_company = models.ForeignKey('login.Billing_Company', on_delete=models.CASCADE)
    partyName = models.CharField(max_length=20, choices=ROW_TYPE_CHOICES)
    partyAddress = models.CharField(max_length=20, choices=ROW_TYPE_CHOICES)
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    row_type = models.CharField(max_length=50, choices=ROW_TYPE_CHOICES)
    vehicle_number = models.CharField(max_length=20)
    invoice_no = models.CharField(max_length=50, null=True, blank=True)
    invoice_date = models.DateField(null=True, blank=True)

    date_of_delivery = models.DateField()
    no_of_bags = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    
    jute_bags = models.PositiveIntegerField()
    plastic_bags = models.PositiveIntegerField()
    fssi = models.PositiveIntegerField()
    loose = models.PositiveIntegerField()
    freight = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    data = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    kanta = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    cashDiscount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    tdsTcs = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    bardana = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    brokerage = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    commission = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    deductedAmt = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    finalAmt = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    
    dueDate = models.DateField(null=True, blank=True)
    
    
    
    status = models.CharField(max_length=20, choices=status_row,default='pending')
    payment= models.CharField(max_length=20, choices=payment_row,default='due')

    

    # Calculate final quantity price based on the order's price per quantal
    def calculate_final_quantity_price(self):
        order_price_per_quantal = self.order.price_per_quantal
        self.final_quantity_price = Decimal(self.quantity) * Decimal(order_price_per_quantal)

    final_quantity_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.calculate_final_quantity_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order.id} Delivery {self.id}"
    
    
    
  
   
    
class ServiceCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Qty = models.PositiveIntegerField()
    costing = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name   




# models.py
from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey('login.CustomUser', on_delete=models.CASCADE)
    order_id = models.IntegerField(null=True, blank=True)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)





 
class MaterialStock(models.Model):
    purchase = 'purchase'
    sales = 'sales'
    


    UNIT_CHOICES = [
        (purchase, 'Purchase'),
        (sales, 'Sales'),
        
        
    ]
    type = models.CharField(max_length=10, choices=UNIT_CHOICES, default=purchase)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL ,blank=True,null=True)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    cost_of_single = models.DecimalField(max_digits=40, decimal_places=2)
    cost_of_all = models.DecimalField(max_digits=50, decimal_places=2)
    total_value = models.DecimalField(max_digits=50, decimal_places=2)
    entry_date = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        # Calculate cost_of_all and total_value before saving
        self.cost_of_all = self.cost_of_single * self.quantity
       

        # Calculate total_value as the sum of cost_of_all for the same material
        total_cost_of_all = MaterialStock.objects.filter(material=self.material).aggregate(
            total_cost=Sum('cost_of_all')
        )['total_cost'] or self.cost_of_all
        self.total_value = total_cost_of_all+self.cost_of_all
        super().save(*args, **kwargs)

class ProductStock(models.Model):
    purchase = 'purchase'
    sales = 'return'
    prod = 'prod'
    
    


    UNIT_CHOICES = [
        (purchase, 'Purchase'),
        (sales, 'Return'),
        (prod, 'Prod'),
        
        
        
    ]
    delivery = models.ForeignKey(DeliveryDetails, on_delete=models.SET_NULL,blank=True,null=True)

    type = models.CharField(max_length=10, choices=UNIT_CHOICES, default=purchase)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    cost_of_single = models.DecimalField(max_digits=50, decimal_places=2)
    cost_of_all = models.DecimalField(max_digits=50, decimal_places=2)
    total_value = models.DecimalField(max_digits=50, decimal_places=2)
    entry_date = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        # Calculate cost_of_all and total_value before saving
        self.cost_of_all = self.cost_of_single * self.quantity
        

        # Calculate total_value as the sum of cost_of_all for the same product
        total_cost_of_all = ProductStock.objects.filter(product=self.product).aggregate(
            total_cost=Sum('cost_of_all')
        )['total_cost'] or self.cost_of_all
        self.total_value = total_cost_of_all+self.cost_of_all
        super().save(*args, **kwargs)
        
        

class AllocateMaterial(models.Model):
    sales= models.CharField(max_length=50)
    
    material = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    quantity_per_piece = models.IntegerField()
    order_quantity = models.IntegerField()
    required = models.IntegerField()
    available = models.IntegerField()
    allocated = models.IntegerField(default=0)

    def __str__(self):
        return self.sales
    