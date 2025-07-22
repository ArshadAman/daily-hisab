from django.db import models


from users.models import User, Business

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    opened = models.BooleanField(default=False)
