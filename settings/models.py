from django.db import models


from users.models import User, Business

class ProfileSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=5, choices=[('en', 'English'), ('hi', 'Hindi'), ('mr', 'Marathi')], default='en')
    app_lock = models.BooleanField(default=False)
    ai_alerts = models.BooleanField(default=True)
    finance_tips = models.BooleanField(default=True)
    multi_business = models.BooleanField(default=False)
    calendar_view = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
