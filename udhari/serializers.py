from rest_framework import serializers
from .models import Customer, Udhari

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class UdhariSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True, required=False
    )
    class Meta:
        model = Udhari
        fields = [
            'id', 'customer', 'customer_id', 'amount', 'given', 'date', 'due_date', 'status', 'notes', 'reminder', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
