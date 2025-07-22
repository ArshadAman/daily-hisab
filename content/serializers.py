from rest_framework import serializers
from .models import Banner, Tutorial

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class TutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields = '__all__'
