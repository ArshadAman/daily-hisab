from rest_framework import serializers
from .models import AdminActivityLog, AdminRole

class AdminActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminActivityLog
        fields = '__all__'

class AdminRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminRole
        fields = '__all__'
