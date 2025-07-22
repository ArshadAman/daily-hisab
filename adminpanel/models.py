from django.db import models


from users.models import User, Business

class AdminActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

class AdminRole(models.Model):
    name = models.CharField(max_length=50)
    permissions = models.TextField()
    users = models.ManyToManyField(User, related_name='admin_roles')
