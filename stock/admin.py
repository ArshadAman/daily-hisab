from django.contrib import admin
from .models import StockItem, StockTransaction
# Register your models here.
admin.site.register(StockItem)
admin.site.register(StockTransaction)