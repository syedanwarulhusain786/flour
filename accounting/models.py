from django.db import models

from commonApp.models import *
    

class Primary_Group(models.Model): #### Primary Group
    PRIMARY_GROUP_CHOICES = [
        ('Debit', 'Debit'),
        ('Credit', 'Credit'),
    ]
    primary_group_number = models.PositiveIntegerField(primary_key=True)  # Start from 100, 200, 300, ...
    primary_group_name = models.CharField(max_length=255)
    primary_group_type = models.CharField(
        max_length=10,
        choices=PRIMARY_GROUP_CHOICES,
    )
    def __str__(self):
        return f"{self.primary_group_name}"

    def save(self, *args, **kwargs):
        if not self.primary_group_number:
            latest_category = Primary_Group.objects.order_by('-primary_group_number').first()
            if latest_category:
                self.primary_group_number = latest_category.primary_group_number + 100
            else:
                self.primary_group_number = 100
        super(Primary_Group, self).save(*args, **kwargs)

class Group(models.Model): #### Group
    primary_group = models.ForeignKey(Primary_Group, on_delete=models.CASCADE)
    group_number = models.PositiveIntegerField()  # Start from 1 within each category
    group_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.group_name}"

    def save(self, *args, **kwargs):
        if not self.group_number:
            # Ensure subcategory_number is unique within each category
            latest_subcategory_in_category = Group.objects.filter(primary_group=self.primary_group).order_by('-group_number').first()
            if latest_subcategory_in_category:
                self.group_number = latest_subcategory_in_category.group_number + 1
            else:
                self.group_number = self.primary_group.primary_group_number+1
        super(Group, self).save(*args, **kwargs)

class Ledger(models.Model): #### Ledger
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    ledger_number = models.PositiveIntegerField()  # Start from 1 within each subcategory
    ledger_name = models.CharField(max_length=255)
    ledger_type = models.CharField(max_length=50)  # You might want to use choices for predefined types
    opening_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    ledger_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    ledger_limitLeft = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.ledger_name}"

    def save(self, *args, **kwargs):
        if not self.ledger_number:
            # Ensure account_number is unique within each subcategory
            latest_account_in_subcategory = Ledger.objects.filter(group=self.group).order_by('-ledger_number').first()
            if latest_account_in_subcategory:
                self.ledger_number = latest_account_in_subcategory.ledger_number + 1
            else:
                self.ledger_number = self.group.group_number*10+1
        super(Ledger, self).save(*args, **kwargs)





class Customer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    
    legder = models.ForeignKey(Ledger, on_delete=models.CASCADE)
    customer_id = models.IntegerField(unique=True)
    customer_name = models.CharField(max_length=255)
    customer_code = models.CharField(max_length=50)
    credit_period = models.IntegerField()
    credit_limit = models.IntegerField()
    mailing_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    
    email = models.EmailField()
    bank_account = models.CharField(max_length=50)
    tin = models.CharField(max_length=20)
    narration = models.CharField(max_length=255)
    gst_no = models.CharField(max_length=20)
    pan = models.CharField(max_length=20)
    opening_balance = models.IntegerField()
    route_id = models.CharField(max_length=20)
    area_id = models.CharField(max_length=20)
    branch_name = models.CharField(max_length=20)
    
    address = models.TextField()

    def save(self, *args, **kwargs):
        # Generate the customer ID if it doesn't exist
        if not self.customer_id:
            last_customer = Customer.objects.order_by('-id').first()
            if last_customer:
                last_id = int(last_customer.customer_id)
                new_id = f'{str(last_id + 1).zfill(2)}'
                new_code = f'cust-{str(last_id + 1).zfill(2)}'
                
            else:
                new_id = 1001
                new_code= 'cus-01'
            self.customer_id = new_id
            self.customer_code = new_code

        super().save(*args, **kwargs)

    def __str__(self):
        return self.customer_name
    
    
    
class Supplier(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    
    ledger = models.ForeignKey(Ledger, on_delete=models.SET_NULL,null=True, blank=True)
    supplier_id = models.IntegerField(unique=True)
    supplier_name = models.CharField(max_length=255)
    supplier_code = models.CharField(max_length=50)
    credit_period = models.IntegerField()
    credit_limit = models.IntegerField()
    mailing_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    branch_name =  models.CharField(max_length=50)
    mobile = models.CharField(max_length=255)
    email = models.EmailField()
    bank_account = models.CharField(max_length=50)
    tin = models.CharField(max_length=20)
    narration = models.CharField(max_length=255)
    gst_no = models.CharField(max_length=20)
    pan = models.CharField(max_length=20)
    opening_balance = models.IntegerField()
    route_id = models.CharField(max_length=20)
    area_id = models.CharField(max_length=20)
    address = models.TextField()

    def save(self, *args, **kwargs):
        # Generate the supplier ID if it doesn't exist
        if not self.supplier_id:
            last_supplier = Supplier.objects.order_by('-id').first()
            if last_supplier:
                last_id = int(last_supplier.supplier_id)
                new_id = f'{str(last_id + 1).zfill(2)}'
                new_code = f'sup-{str(last_id + 1).zfill(2)}'
                
            else:
                new_id = 1001
                new_code= 'sup-01'
            self.supplier_id = new_id
            self.supplier_code = new_code
            

        super().save(*args, **kwargs)

    def __str__(self):
        return self.supplier_name
    




class PurchaseInvoice(models.Model):
    quotation_number = models.AutoField(primary_key=True)  
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL,null=True, blank=True)

    billing_address = models.TextField()
    shipping_address = models.TextField(blank=True)
    quotation_date = models.DateField(auto_now_add=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    terms_and_conditions = models.TextField(blank=True)
    notes_comments = models.TextField(null=True,blank=True)
    
    # Add a discount field if you intend to use it
    sub_total = models.CharField(max_length=255)
    csgst_total = models.CharField(max_length=255)
    sgst_total = models.CharField(max_length=255)
    
    final_amt = models.CharField(max_length=255)
    Others = models.CharField(max_length=255,blank=True,null=True)
    
    

    # def save(self, *args, **kwargs):
    #     # Calculate grand total before saving
    #     total_price = sum(item.sub_total for item in self.items.all())
    #     print(f"Total Price: {total_price}")
        
    #     self.final_amt = total_price + (total_price * (self.tax_rate or 0) / 100)
    #     print(f"Final Amount: {self.final_amt}")

    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"PurchaseQuotation #{self.quotation_number}"
    
class PurchaseInvoiceItemRow(models.Model):
    ENTRY_TYPE_CHOICES = [
        ('PurchaseQuotation', 'PurchaseQuotation'),
    ]

    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPE_CHOICES)
    quotation = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE, related_name='items',null=True,blank=True)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    quantity = models.PositiveIntegerField()
    unit_price = models.CharField(max_length=255)
    total_price = models.CharField(max_length=255)
      


    def __str__(self):
        return f"{self.product_description} - {self.quantity} units"




class SalesQuotation(models.Model):
   
    salesstatus_TYPE_CHOICES=[
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('disapproved', 'disapproved'),
        ('inProduction', 'in Production'),
        ('produced', 'produced'),
        
        
        ('deliverPending', 'deliverPending'),
        ('completed', 'completed'),
        
        
    ]
   
    quotation_number = models.AutoField(primary_key=True)  
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True, blank=True)

    billing_address = models.TextField()
    shipping_address = models.TextField(blank=True)
    quotation_date = models.DateField(auto_now_add=True,null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    
    terms_and_conditions = models.TextField(blank=True)
    notes_comments = models.TextField(null=True,blank=True)
    commision = models.PositiveIntegerField(null=True,blank=True,default=0)
    
    # Add a discount field if you intend to use it
    sub_total = models.CharField(max_length=255,null=True, blank=True)

    
    approval = models.CharField(max_length=20, choices=salesstatus_TYPE_CHOICES,default='pending')

    def __str__(self):
        return f"SalesQuotation #{self.quotation_number}"
    
class SalesItemRow(models.Model):
    ENTRY_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('agent', 'Agent'),
        
    ]
 
    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPE_CHOICES)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='product',null=True,blank=True)
    quotation = models.ForeignKey(SalesQuotation, on_delete=models.CASCADE, related_name='items',null=True,blank=True)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    quantity = models.PositiveIntegerField()
    quantity_left = models.PositiveIntegerField()
    unit_price = models.CharField(max_length=255)
    total_price = models.CharField(max_length=255)
  
      
    def save(self, *args, **kwargs):
        # Set quantity_left to the initial quantity value when a new row is created
        if not self.id and self.quantity:
            self.quantity_left = self.quantity

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_description} - {self.quantity} units"

    def __str__(self):
        return f"{self.product_description} - {self.quantity} units"


  
class SalesDeliveryDetails(models.Model):
    ROW_TYPE_CHOICES = [
    ('dispatch', 'Dispatch'),
    ('delivery', 'Delivery'),
    ]
    status_row = [
    ('pending', 'Pending'),
    ('delivered', 'Delivered'),
    ]
    status_payment= [
    ('due', 'due'),
    ('recieved', 'recieved'),
    ]
    created_at=models.DateField(auto_now_add=True,null=True, blank=True)
    OrderFk = models.ForeignKey(SalesQuotation, on_delete=models.SET_NULL,null=True, blank=True)

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True, blank=True)
    order = models.ForeignKey(SalesItemRow, on_delete=models.SET_NULL,null=True, blank=True)
    row_type = models.CharField(max_length=20, choices=ROW_TYPE_CHOICES)
    vehicle_number = models.CharField(max_length=20)
    date_of_delivery = models.DateField()
    no_of_bags = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    jute_bags = models.PositiveIntegerField()
    plastic_bags = models.PositiveIntegerField()
    fssi = models.PositiveIntegerField()
    loose = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=status_row,default='pending')
    dueDate = models.DateField(null=True, blank=True)
    
    
    
    payment= models.CharField(max_length=20, choices=status_payment,default='due')
    final_quantity_price= models.CharField(max_length=20,null=True, blank=True)
    

    def __str__(self):
        return f"SalesDeliveryDetails for Order {self.order}"    
    
    
    
    
    




    
    
class PurchaseQuotation(models.Model):
    status_TYPE_CHOICES = [
        ('ACTIVE', True),
        ('INACTIVE', False),
        
    ]
    quotation_number = models.AutoField(primary_key=True)  
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)

    billing_address = models.TextField()
    shipping_address = models.TextField(blank=True)
    quotation_date = models.DateField(auto_now_add=True,null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    
    terms_and_conditions = models.TextField(blank=True)
    notes_comments = models.TextField(null=True,blank=True)
    
    # Add a discount field if you intend to use it
    sub_total = models.CharField(max_length=255,null=True, blank=True)
    csgst_total = models.CharField(max_length=255,null=True, blank=True)
    sgst_total = models.CharField(max_length=255,null=True, blank=True)
    
    final_amt = models.CharField(max_length=255,null=True, blank=True)
    Others = models.CharField(max_length=255,blank=True,null=True)
    status = models.BooleanField(max_length=20, choices=status_TYPE_CHOICES)
    
    

    # def save(self, *args, **kwargs):
    #     # Calculate grand total before saving
    #     total_price = sum(item.sub_total for item in self.items.all())
    #     print(f"Total Price: {total_price}")
        
    #     self.final_amt = total_price + (total_price * (self.tax_rate or 0) / 100)
    #     print(f"Final Amount: {self.final_amt}")

    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"PurchaseQuotation #{self.quotation_number}"
    
class PurchaseItemRow(models.Model):
    ENTRY_TYPE_CHOICES = [
        ('PurchaseQuotation', 'PurchaseQuotation'),
    ]
 
    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPE_CHOICES)
    quotation = models.ForeignKey(PurchaseQuotation, on_delete=models.CASCADE, related_name='items',null=True,blank=True)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    quantity = models.PositiveIntegerField()
    unit_price = models.CharField(max_length=255)
    total_price = models.CharField(max_length=255)
  
      


    def __str__(self):
        return f"{self.product_description} - {self.quantity} units"




class Bids(models.Model):
    ENTRY_TYPE_CHOICES = [
        ('AGENT', 'AGENT'),
        ('SUPPLIER', 'SUPPLIER'),
        
    ]
    quotation = models.ForeignKey(PurchaseQuotation, on_delete=models.CASCADE, related_name='Quotationitems',null=True,blank=True)
    prductRow = models.ForeignKey(PurchaseItemRow, on_delete=models.CASCADE, related_name='Product',null=True,blank=True)
    supplier_type = models.CharField(max_length=20, choices=ENTRY_TYPE_CHOICES)
    
    supplierBid = models.CharField(max_length=255)
    agentcommision = models.CharField(max_length=255,default=0)
    delivery_date = models.DateField(null=True, blank=True)

 
      


    def __str__(self):
        return f"{self.product_description} - {self.quantity} units"



























class JournalEntry(models.Model):
    s_no=models.AutoField(primary_key=True)
    voucherNo = models.IntegerField() 
    voucherCode = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    invoice_no=models.CharField(blank=True,null=True,max_length=255)
    invoice_date=models.DateField(blank=True,null=True)
    narration = models.CharField(max_length=255,null=True, blank=True)
    
    debit_total = models.DecimalField(max_digits=10, decimal_places=2)    
    credit_total = models.DecimalField(max_digits=10, decimal_places=2)    
    

    def save(self, *args, **kwargs):
        if not self.voucherNo:
            # Get the maximum voucher number currently in the database
            max_voucher = JournalEntry.objects.aggregate(models.Max('voucherNo'))['voucherNo__max']
            # Set the voucher number to the maximum + 1 or 100 if there are no records yet
            self.voucherNo = max_voucher + 1 if max_voucher else 100
        self.voucherCode = "JV-"+str(self.voucherNo)
            
        super(JournalEntry, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.voucherNo}"
class JournalEntryRow(models.Model):
    
    entryFk = models.ForeignKey(JournalEntry, on_delete=models.CASCADE , related_name='rows')
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE)
    comment=models.CharField(blank=True,null=True,max_length=499)

    debit = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    credit = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)    
    
    



class PaymentEntry(models.Model):
    s_no = models.AutoField(primary_key=True)
    voucherNo = models.IntegerField() 
    voucherCode = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    invoice_no = models.CharField(blank=True, null=True, max_length=255)
    invoice_date = models.DateField(blank=True, null=True)
    narration = models.CharField(max_length=255, null=True, blank=True)
    from_ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE, related_name='payments_made')
    to_ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE, related_name='payments_received')
    debit_total = models.DecimalField(max_digits=10, decimal_places=2)    
    credit_total = models.DecimalField(max_digits=10, decimal_places=2)    
    comment=models.CharField(max_length=255, null=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.voucherNo:
            # Get the maximum voucher number currently in the database
            max_voucher = PaymentEntry.objects.aggregate(models.Max('voucherNo'))['voucherNo__max']
            # Set the voucher number to the maximum + 1 or 100 if there are no records yet
            self.voucherNo = max_voucher + 1 if max_voucher else 100
        self.voucherCode = f"PV-{self.voucherNo}"
        super(PaymentEntry, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.voucherNo}"


class RecieptEntry(models.Model):
    s_no = models.AutoField(primary_key=True)
    voucherNo = models.IntegerField() 
    voucherCode = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    invoice_no = models.CharField(blank=True, null=True, max_length=255)
    invoice_date = models.DateField(blank=True, null=True)
    narration = models.CharField(max_length=255, null=True, blank=True)
    from_ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE, related_name='payments_from')
    to_ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE, related_name='payments_to')
    debit_total = models.DecimalField(max_digits=10, decimal_places=2)    
    credit_total = models.DecimalField(max_digits=10, decimal_places=2)    
    comment=models.CharField(max_length=255, null=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.voucherNo:
            # Get the maximum voucher number currently in the database
            max_voucher = RecieptEntry.objects.aggregate(models.Max('voucherNo'))['voucherNo__max']
            # Set the voucher number to the maximum + 1 or 100 if there are no records yet
            self.voucherNo = max_voucher + 1 if max_voucher else 100
        self.voucherCode = f"RV-{self.voucherNo}"
        super(RecieptEntry, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.voucherNo}"





class ContraEntry(models.Model):
    s_no=models.AutoField(primary_key=True)
    voucherNo = models.IntegerField() 
    voucherCode = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    invoice_no=models.CharField(blank=True,null=True,max_length=255)
    invoice_date=models.DateField(blank=True,null=True)
    narration = models.CharField(max_length=255,null=True, blank=True)
    
    debit_total = models.DecimalField(max_digits=10, decimal_places=2)    
    credit_total = models.DecimalField(max_digits=10, decimal_places=2)    
    

    def save(self, *args, **kwargs):
        if not self.voucherNo:
            # Get the maximum voucher number currently in the database
            max_voucher = ContraEntry.objects.aggregate(models.Max('voucherNo'))['voucherNo__max']
            # Set the voucher number to the maximum + 1 or 100 if there are no records yet
            self.voucherNo = max_voucher + 1 if max_voucher else 100
        self.voucherCode = "CV-"+str(self.voucherNo)
            
        super(ContraEntry, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.voucherNo}"
class ContraEntryRow(models.Model):
    
    entryFk = models.ForeignKey(ContraEntry, on_delete=models.CASCADE , related_name='rows')
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE)
    comment=models.CharField(blank=True,null=True,max_length=499)

    debit = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    credit = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)  






class SalesEntry(models.Model):
    s_no=models.AutoField(primary_key=True)
    voucherNo = models.IntegerField() 
    voucherCode = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    invoice_no=models.CharField(blank=True,null=True,max_length=255)
    invoice_date=models.DateField(blank=True,null=True)
    narration = models.CharField(max_length=255,null=True, blank=True)
    comment=models.CharField(blank=True,null=True,max_length=499)
    
    debit_total = models.DecimalField(max_digits=10, decimal_places=2)    
    credit_total = models.DecimalField(max_digits=10, decimal_places=2)    
    

    def save(self, *args, **kwargs):
        if not self.voucherNo:
            # Get the maximum voucher number currently in the database
            max_voucher = SalesEntry.objects.aggregate(models.Max('voucherNo'))['voucherNo__max']
            # Set the voucher number to the maximum + 1 or 100 if there are no records yet
            self.voucherNo = max_voucher + 1 if max_voucher else 100
        self.voucherCode = "SV-"+str(self.voucherNo)
            
        super(SalesEntry, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.voucherNo}"
class SalesEntryRow(models.Model):
    
    entryFk = models.ForeignKey(SalesEntry, on_delete=models.CASCADE , related_name='rows')
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE)
    comment=models.CharField(blank=True,null=True,max_length=499)

    debit = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    credit = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)  







class PurchaseEntry(models.Model):
    s_no=models.AutoField(primary_key=True)
    voucherNo = models.IntegerField() 
    voucherCode = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    invoice_no=models.CharField(blank=True,null=True,max_length=255)
    invoice_date=models.DateField(blank=True,null=True)
    narration = models.CharField(max_length=255,null=True, blank=True)
    
    debit_total = models.DecimalField(max_digits=10, decimal_places=2)    
    credit_total = models.DecimalField(max_digits=10, decimal_places=2)    
    

    def save(self, *args, **kwargs):
        if not self.voucherNo:
            # Get the maximum voucher number currently in the database
            max_voucher = PurchaseEntry.objects.aggregate(models.Max('voucherNo'))['voucherNo__max']
            # Set the voucher number to the maximum + 1 or 100 if there are no records yet
            self.voucherNo = max_voucher + 1 if max_voucher else 100
        self.voucherCode = "PRV-"+str(self.voucherNo)
            
        super(PurchaseEntry, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.voucherNo}"
class PurchaseEntryRow(models.Model):
    
    entryFk = models.ForeignKey(PurchaseEntry, on_delete=models.CASCADE , related_name='rows')
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE)
    comment=models.CharField(blank=True,null=True,max_length=499)

    debit = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    credit = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)  










class CreditNoteEntry(models.Model):
    s_no=models.AutoField(primary_key=True)
    voucherNo = models.IntegerField() 
    voucherCode = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    invoice_no=models.CharField(blank=True,null=True,max_length=255)
    invoice_date=models.DateField(blank=True,null=True)
    narration = models.CharField(max_length=255,null=True, blank=True)
    
    debit_total = models.DecimalField(max_digits=10, decimal_places=2)    
    credit_total = models.DecimalField(max_digits=10, decimal_places=2)    
    

    def save(self, *args, **kwargs):
        if not self.voucherNo:
            # Get the maximum voucher number currently in the database
            max_voucher = CreditNoteEntry.objects.aggregate(models.Max('voucherNo'))['voucherNo__max']
            # Set the voucher number to the maximum + 1 or 100 if there are no records yet
            self.voucherNo = max_voucher + 1 if max_voucher else 100
        self.voucherCode = "CNV-"+str(self.voucherNo)
            
        super(CreditNoteEntry, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.voucherNo}"
class creditNoteEntryRow(models.Model):
    
    entryFk = models.ForeignKey(CreditNoteEntry, on_delete=models.CASCADE , related_name='rows')
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE)
    comment=models.CharField(blank=True,null=True,max_length=499)

    debit = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    credit = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)  










class DebitNoteEntry(models.Model):
    s_no=models.AutoField(primary_key=True)
    voucherNo = models.IntegerField() 
    voucherCode = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    invoice_no=models.CharField(blank=True,null=True,max_length=255)
    invoice_date=models.DateField(blank=True,null=True)
    narration = models.CharField(max_length=255,null=True, blank=True)
    
    debit_total = models.DecimalField(max_digits=10, decimal_places=2)    
    credit_total = models.DecimalField(max_digits=10, decimal_places=2)    
    

    def save(self, *args, **kwargs):
        if not self.voucherNo:
            # Get the maximum voucher number currently in the database
            max_voucher = DebitNoteEntry.objects.aggregate(models.Max('voucherNo'))['voucherNo__max']
            # Set the voucher number to the maximum + 1 or 100 if there are no records yet
            self.voucherNo = max_voucher + 1 if max_voucher else 100
        self.voucherCode = "DNV-"+str(self.voucherNo)
            
        super(DebitNoteEntry, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.voucherNo}"
    
class DebitNoteEntryRow(models.Model):
    
    entryFk = models.ForeignKey(DebitNoteEntry, on_delete=models.CASCADE , related_name='rows')
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE)
    comment=models.CharField(blank=True,null=True,max_length=499)

    debit = models.DecimalField(max_digits=10, decimal_places=3,blank=True,null=True)
    credit = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)  





    
    
    




class VoucherLedgerVisibility(models.Model):
    VOUCHER_CHOICES = [
        ('CV', 'Contra Voucher'),
        ('SV', 'Sales Voucher'),
        ('PV', 'Purchase Voucher'),
        ('JV', 'Journal Voucher'),
        ('CNV', 'Credit Note Voucher'),
        ('DNV', 'Debit Note Voucher'),
        ('SJV', 'Stock Journal Voucher'),
        ('PAV', 'Payment Advice Voucher'),
        ('RAV', 'Receipt Advice Voucher'),
        ('PAY', 'Payment Voucher'),
        ('RCT', 'Receipt Voucher'),
        
        
        # Add more voucher types as needed
    ]

    voucher_type = models.CharField(max_length=3, choices=VOUCHER_CHOICES)
    selected_groups = models.ManyToManyField(Group)

    def __str__(self):
        return f"{self.get_voucher_type_display()} Ledger Visibility"

    class Meta:
        verbose_name_plural = "Voucher Ledger Visibility"


class Tax(models.Model):
    type = models.CharField(max_length=50)  # Allow for longer user-defined tax types
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.type} - {self.percentage}%"
    
    
class LedgerEntry(models.Model):
    # Reference to Delivery and Order
    salesdelivery = models.ForeignKey(SalesDeliveryDetails, on_delete=models.CASCADE, related_name='ledger_sales',null=True,blank=-True)
    
    delivery = models.ForeignKey(DeliveryDetails, on_delete=models.CASCADE, related_name='ledger_purchase' ,null=True,blank=-True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ledger_entries' ,null=True,blank=-True)
    saleorder = models.ForeignKey(SalesQuotation, on_delete=models.CASCADE, related_name='ledgerSalesQuotation_entries' ,null=True,blank=-True)
    
    account = models.ForeignKey(Ledger, on_delete=models.CASCADE, related_name='ledger_accounts')
    # Other fields for ledger entry details
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    debit_amount = models.DecimalField(max_digits=100, decimal_places=2)
    credit_amount = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return f"Ledger Entry #{self.id} - {self.date}"