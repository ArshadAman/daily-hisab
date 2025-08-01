from django.contrib import admin
from .models import AdminActivityLog, AdminRole

admin.site.register(AdminActivityLog)
admin.site.register(AdminRole)
