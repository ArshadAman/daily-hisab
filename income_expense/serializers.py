from rest_framework import serializers
from .models import Category, IncomeExpense

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class IncomeExpenseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )
    class Meta:
        model = IncomeExpense
        fields = [
            'id', 'user', 'business', 'amount', 'type', 'category', 'category_id',
            'date', 'time', 'payment_mode', 'notes', 'created_at', 'voice_entry'
        ]
        read_only_fields = ['id', 'created_at']
