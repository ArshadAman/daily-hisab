from django.db import models


from users.models import User, Business

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Udhari(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    given = models.BooleanField()  # True = Given, False = Received
    date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')], default='unpaid')
    notes = models.TextField(blank=True, null=True)
    reminder = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
