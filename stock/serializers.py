from rest_framework import serializers
from .models import StockItem, StockTransaction

class StockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItem
        fields = '__all__'

class StockTransactionSerializer(serializers.ModelSerializer):
    stock_item = StockItemSerializer(read_only=True)
    stock_item_id = serializers.PrimaryKeyRelatedField(
        queryset=StockItem.objects.all(), source='stock_item', write_only=True, required=False
    )
    class Meta:
        model = StockTransaction
        fields = [
            'id', 'stock_item', 'stock_item_id', 'transaction_type', 'quantity', 'date', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
