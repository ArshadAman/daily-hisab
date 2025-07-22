from django.db import models


# Reports are generated, not stored, but you can log exports
from users.models import User, Business

class ReportExport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=50)
    file_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
