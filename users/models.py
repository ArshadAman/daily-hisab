from django.db import models


from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    language = models.CharField(max_length=5, choices=[('en', 'English'), ('hi', 'Hindi'), ('mr', 'Marathi')], default='en')
    business = models.ForeignKey('Business', on_delete=models.SET_NULL, null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=20, blank=True, null=True)
    referred_by = models.CharField(max_length=20, blank=True, null=True)
    app_locked = models.BooleanField(default=False)
    health_score = models.IntegerField(default=100)
    notes = models.TextField(blank=True, null=True)

class Business(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='owned_businesses')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
