from rest_framework import serializers
from .models import ReportExport

class ReportExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportExport
        fields = '__all__'
