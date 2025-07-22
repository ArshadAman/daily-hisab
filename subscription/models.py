from django.db import models


from users.models import User

class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_months = models.IntegerField()
    is_active = models.BooleanField(default=True)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    auto_renew = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.IntegerField()
    valid_from = models.DateField()
    valid_to = models.DateField()
    is_active = models.BooleanField(default=True)
