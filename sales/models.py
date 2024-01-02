# models.py
from django.db import models
from accounting.models import Ledger  # Import your Ledger model here

class Quotation(models.Model):
    quotation_number = models.AutoField(primary_key=True)  
    customer_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True)
    contact_person = models.CharField(max_length=255)
    contact_email = models.EmailField()
    billing_address = models.TextField()
    shipping_address = models.TextField(blank=True)
    quotation_date = models.DateField()
    expiry_date = models.DateField()
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    terms_and_conditions = models.TextField(blank=True)
    notes_comments = models.TextField(blank=True)
    
    # Add a discount field if you intend to use it
    sub_total = models.CharField(max_length=255)
    tax_total = models.CharField(max_length=255)
    final_amt = models.CharField(max_length=255)
    

    # def save(self, *args, **kwargs):
    #     # Calculate grand total before saving
    #     total_price = sum(item.sub_total for item in self.items.all())
    #     print(f"Total Price: {total_price}")
        
    #     self.final_amt = total_price + (total_price * (self.tax_rate or 0) / 100)
    #     print(f"Final Amount: {self.final_amt}")

    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"Quotation #{self.quotation_number}"

class Sales(models.Model):
    trasactionType_CHOICES = [
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('neft/rtgs/upi', 'NEFT/RTGS/UPI'),
        
    ]

    trasactionType = models.CharField(max_length=20, choices=trasactionType_CHOICES,null=True,blank=True)
    trasactionDetails = models.CharField(max_length=20,null=True,blank=True)
    
    sale_number = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True)
    contact_person = models.CharField(max_length=255)
    contact_email = models.EmailField()
    billing_address = models.TextField()
    shipping_address = models.TextField(blank=True)
    sale_date = models.DateField()
    delivery_datesale = models.DateField()
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    terms_and_conditions = models.TextField(blank=True)
    notes_comments = models.TextField(blank=True)
    advance= models.CharField(max_length=255, blank=True, null=True)
    sub_total = models.CharField(max_length=255, blank=True, null=True)
    tax_total = models.CharField(max_length=255, blank=True, null=True)
    final_amt = models.CharField(max_length=255, blank=True, null=True)

    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE)  # Foreign key for Ledger

    def __str__(self):
        return f"Sale #{self.sale_number}"
    
    
class ItemRow(models.Model):
    ENTRY_TYPE_CHOICES = [
        ('sales', 'Sales'),
        ('quotations', 'Quotations'),
    ]

    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPE_CHOICES)
    sale = models.ForeignKey(Sales, on_delete=models.CASCADE, related_name='items',null=True,blank=True)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='items',null=True,blank=True)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    quantity = models.PositiveIntegerField()
    unit_price = models.CharField(max_length=255)
    total_price = models.CharField(max_length=255)
      


    def __str__(self):
        return f"{self.product_description} - {self.quantity} units"
