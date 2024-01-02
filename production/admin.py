from django.contrib import admin
from .models import *
# Register your models here.
from sales.models import *
from accounting.models import *
from .models import *

admin.site.register(ProductionRow)
admin.site.register(ProducedRow)