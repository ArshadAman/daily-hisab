from rest_framework import serializers
from .models import Plan, Subscription, Coupon

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
