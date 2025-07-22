from django.db import models


from users.models import Business

class StockItem(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    opening_stock = models.DecimalField(max_digits=12, decimal_places=2)
    closing_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price_per_unit = models.DecimalField(max_digits=12, decimal_places=2)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class StockTransaction(models.Model):
    stock_item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=[('in', 'In'), ('out', 'Out')])
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
