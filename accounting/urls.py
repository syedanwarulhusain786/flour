"""
URL configuration for erp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from .views import ProductListView, product_form, product_delete
from .views import GeneratePDF
urlpatterns = [
    path('payables/', views.payables, name='payables'),
    path('viewdelivery/<int:pk>/', views.viewdelivery, name='viewdelivery'),
    
    path('recievables/', views.recievables, name='recievables'),
    
    
    path('salesapprove/', views.salesapprove, name='salesapprove'),
    path('sales_quotations/<int:pk>/', views.SalesQuotationDetailView, name='sales_quotation_detail'),
    # path('approve_order/<int:order_id>/',  views.approve_order, name='approve_order'),
    # path('disapprove_order/<int:order_id>/',  views.disapprove_order, name='disapprove_order'),
    path('salesapproved/', views.salesapproved, name='salesapproved'),
    path('salesdisapproved/', views.salesdisapproved, name='salesdisapproved'),
    path('salesacceptDelivery/<int:order_id>/', views.salesacceptDelivery, name='salesacceptDelivery'),
    
    path('updateDelivery/<int:order_id>/', views.updateDelivery, name='updateDelivery'),
    path('salesstartdelivery/<int:order_id>/', views.salesstartdelivery, name='salesstartdelivery'),
    
    
    
    path('payments/', views.payments, name='payments'),
    path('reciepts/', views.reciepts, name='reciepts'),
    
    
    
    
    
    
    
    
    
    
    path('approve/', views.approve, name='approve'),

    # path('approve_order/<int:order_id>/',  views.approve_order, name='approve_order'),
    # path('disapprove_order/<int:order_id>/',  views.disapprove_order, name='disapprove_order'),
    path('adminapproved/', views.adminapproved, name='adminapproved'),
    path('admindisapproved/', views.admindisapproved, name='admindisapproved'),
    path('acceptDelivery/<int:order_id>/', views.acceptDelivery, name='acceptDelivery'),
    path('updateDelivery/<int:order_id>/', views.updateDelivery, name='updateDelivery'),
    
    
    
    path('accountsChart/', views.Account_chart, name="accountsChart"),



    path('primaryGroup/', views.primaryGroup, name="primaryGroup"),
    path('groupage/', views.groupPage, name="groupage"),


    
    
    
    ##############Journal Ledgers###########
    path('generalLedger/', views.Gernal_Ledger, name="generalLedger"),
    path('LedgerEntries/', views.LedgerEntries, name="LedgerEntries"),
    path('delivery-details/<int:delivery_id>/', views.check_delivery_details, name='check_delivery_details'),

    
    ###########################################################################################################################
    
    
    
    
    
    
    #################################################Purchase Return ##########################

    

    path('purchaseReturn/add/', views.add_service, name='add_service'),
    path('purchaseReturn/', views.list_services, name='list_services'),
    path('purchaseReturn/add/', views.add_service, name='add_service'),
    
    
    #################################################Journal Entry ##########################

          
    path('journal/', views.Journal_entry, name="journal"),
    path('journal-entries/', views.journalEntries, name="journal-entries"),
    path('edit-journal/', views.journalEntries, name="edit-journal"),
    
    
    
    ###############Payment Entries#############
             
    path('payment/', views.payment, name="payment"),
    path('payment-entries/', views.journalEntries, name="payment-entries"),
    
    ############Reciept Entry#############
             
    path('reciept/', views.reciept, name="reciept"),
    path('edit-reciept/', views.Journal_entry, name="edit-reciept"),
    path('reciept-entries/', views.journalEntries, name="reciept-entries"),
    
    #############contra Entry############
             
    path('contra/', views.contra, name="contra"),
    path('edit-contra/', views.Journal_entry, name="edit-contra"),
    path('contra-entries/', views.journalEntries, name="contra-entries"),
    
    ################################################################
    
    #############credit Entry############
    
    path('credit-note/', views.credit_note, name="credit-note"),
    path('edit-credit-note/', views.Journal_entry, name="edit-credit-note"),
    path('credit-note-entries/', views.journalEntries, name="credit-note-entries"),
    
    #############debit Entry############
    
    path('debit-note/', views.debit_note, name="debit-note"),
    path('edit-debit-note/', views.Journal_entry, name="edit-debit-note"),
    path('debit-note-entries/', views.journalEntries, name="debit-note-entries"),
    
    
    
    
    
    
    
    
    
    
    
    
    
    path('account/', views.accountingDashboard, name='account'),
    
    
    path('customer/', views.accountingcustomer, name='customer'),
    path('addcustomer/', views.addaccountingcustomer, name='addcustomer'),
    
    
    path('addsupplier/', views.addaccountingsupplier, name='addsupplier'),
    path('supplier/', views.accountingsupplier, name='supplier'),
    
    
    
    path('group/', views.accountingroup, name='group'),
    path('accountingledger/', views.accountingledger, name='accountingledger'),
    path('voucher/', views.accountingvoucher, name='voucher'),
    path('currency/', views.accountingcurrency, name='currency'),
    

    
    path('trialBalance/', views.Trial_Balance, name="trialBalance"),
    
    path('profitAndLoss/', views.Profit_Loss, name="profitAndLoss"),
    
    path('balanceSheet/', views.Balance_sheet, name="balanceSheet"),
    
  
    
    path('autocomplete/', views.autocomplete, name="autocomplete"),
    
    path('action/', views.action, name="action"),
    path('action_ledger/', views.action_ledger, name="action"),
    
    
    
    
    path('maintain/', views.maintain, name="maintain"),
    
    
    path('paymentEntry/', views.paymentEntry, name="paymentEntry"),
    path('paymentList/', views.paymentList, name="paymentList"),
    path('submit_payment/', views.submit_payment, name="submit_payment"),
    
    path('recieptList/', views.recieptList, name="recieptList"),
    path('recieptEntry/', views.recieptEntry, name="recieptEntry"),
    path('submit_reciept/', views.submit_reciept, name="submit_reciept"),
    
    
    path('salesList/', views.salesList, name="salesList"),
    path('salesEntry/', views.salesEntry, name="salesEntry"),
    path('submitSales/', views.submitSales, name="submitSales"),
    
    path('purchaseList/', views.purchaseList, name="purchaseList"),
    path('purchaseEntry/', views.purchaseEntry, name="purchaseEntry"),
    path('submitpurchase/', views.submitpurchase, name="submitpurchase"),
    
    
    
    
    
    path('view_salesvoucher/<str:voucher_id>/', views.item_detail, name='item_detail'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    
    
    
    
    #################################################Products Urls ##########################
    
    
    path('products/', ProductListView.as_view(), name='product_list'),
    # path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', product_form, name='product_create'),
    path('products/<int:pk>/update/', views.product_update_form , name='product_update'),
    path('products/<int:pk>/delete/', product_delete, name='product_delete'),
    
    ######################product material###########
    path('product-materials/', views.productMaterials, name='product-materials'),
    path('product-materials/create/', views.productMaterials_form, name='product_materials_create'),
    path('product-materials/<int:pk>/update/', views.productMaterials_update_form , name='product_materials_update'),
    path('product-materials/<int:pk>/delete/', views.productMaterials_delete, name='product_materials_delete'),
    
# path('product-materials-detail/<int:product_id>/', views.product_materials_detail, name='product-materials-detail'),

    
    # Add more URLs as needed
    
    
    
    #################################################Services Url ##########################
    
    
    path('services/', views.list_services, name='list_services'),
    path('services/add/', views.add_service, name='add_service'),
    path('services/edit/<int:service_id>/', views.edit_service, name='edit_service'),
    path('services/delete/<int:service_id>/', views.delete_service, name='delete_service'),
    
    
    
    
    
    
    
    
    #################################################brand and Category Urls##########################
    
    #################################################brand ##########################
    
    path('brands-category/', views.brand_category, name='brand_category'),
    path('brands/add/', views.add_brands, name='add_brands'),
    path('brands/edit/<int:service_id>/', views.edit_brands, name='edit_brands'),
    path('brands/delete/<int:service_id>/', views.delete_brands, name='delete_brands'),
    
    #################################################Category Urls##########################
    
    
    path('category/add/', views.add_category, name='add_category'),
    path('category/edit/<int:service_id>/', views.edit_category, name='edit_category'),
    path('category/delete/<int:service_id>/', views.delete_category, name='delete_category'),
    ################################################################################################################################################
    #################################################Quotation Urls##########################
    path('purchase/', views.purchase_quote, name='purchase_quote'),
    path('purchase-orders/', views.quotepurchaseList, name='purchase-orders'),
    path('purchase/<int:pk>/', views.PurchaseQuotationDetailView, name='quotation-detail'),
    path('purchase/<int:pk>/delete/',views.PurchaseQuotationDeleteView, name='quotation-delete'),
    
    
    
    
    
    
    
    ###################################Purchase Urls##########################
    
    
    path('purchase-invoices/', views.purchaseList, name='purchaseOrder'),
    path('purchase/add/', views.purchaseEntry, name='add_purchase'),
    #####################################################################################################

    
    path('pdfs/', GeneratePDF.as_view(), name='pdfs'),
    
    
    
]
