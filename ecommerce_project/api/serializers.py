from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock']

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity']

class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemSerializer(many=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("Order must contain at least one item")
        return items

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'items', 'total_price', 'status', 'created_at'] 