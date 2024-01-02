from django.contrib import admin

# Register your models here.
from .models import CustomUser, Department,AccountType,Company,TermsAndCondition

admin.site.register(CustomUser)
admin.site.register(Department)
admin.site.register(AccountType)
admin.site.register(Company)
admin.site.register(TermsAndCondition)



