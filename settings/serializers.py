from rest_framework import serializers
from .models import ProfileSettings

class ProfileSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileSettings
        fields = '__all__'
