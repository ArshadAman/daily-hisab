from rest_framework import serializers
from .models import User, Business

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    business = BusinessSerializer(read_only=True)
    business_id = serializers.PrimaryKeyRelatedField(
        queryset=Business.objects.all(), source='business', write_only=True, required=False
    )
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone', 'language', 'business', 'business_id',
            'is_premium', 'referral_code', 'referred_by', 'app_locked', 'health_score', 'notes',
            'first_name', 'last_name', 'is_active', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
