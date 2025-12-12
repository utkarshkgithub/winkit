from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model"""
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'subtotal', 'created_at']
        read_only_fields = ['id', 'product_name', 'price', 'subtotal', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model"""
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_name', 'order_status', 'total_amount',
            'shipping_address', 'phone_number', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'total_amount', 'created_at', 'updated_at']


class CreateOrderSerializer(serializers.Serializer):
    """Serializer for creating an order"""
    shipping_address = serializers.CharField()
    phone_number = serializers.CharField(max_length=15)

    def validate_shipping_address(self, value):
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError("Please provide a valid shipping address")
        return value

    def validate_phone_number(self, value):
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError("Please provide a valid phone number")
        return value


class UpdateOrderStatusSerializer(serializers.Serializer):
    """Serializer for updating order status (admin only)"""
    order_status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)
