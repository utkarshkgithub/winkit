from rest_framework import serializers
from .models import Order, OrderItem, OrderStatusHistory
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model"""
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'subtotal', 'created_at']
        read_only_fields = ['id', 'product_name', 'price', 'subtotal', 'created_at']


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    """Serializer for OrderStatusHistory model"""
    changed_by_username = serializers.CharField(
        source='changed_by.username',
        read_only=True,
        allow_null=True
    )
    old_status_display = serializers.CharField(
        source='get_old_status_display',
        read_only=True
    )
    new_status_display = serializers.CharField(
        source='get_new_status_display',
        read_only=True
    )
    display_message = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderStatusHistory
        fields = [
            'id', 'old_status', 'old_status_display', 'new_status',
            'new_status_display', 'changed_by_username', 'changed_at',
            'notes', 'display_message'
        ]
        read_only_fields = fields
    
    def get_display_message(self, obj):
        """Generate formatted timeline message"""
        date_str = obj.changed_at.strftime("%b %d, %Y at %I:%M %p")
        
        if obj.old_status is None:
            # Order creation
            return f"Order created on {date_str}"
        
        if obj.changed_by:
            # Changed by user/admin
            return f"Order {obj.get_new_status_display().lower()} by {obj.changed_by.username} on {date_str}"
        else:
            # System change
            return f"Order status changed to {obj.get_new_status_display().lower()} on {date_str}"


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model"""
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    history = OrderStatusHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_name', 'order_status', 'total_amount',
            'shipping_address', 'phone_number', 'items', 'history',
            'created_at', 'updated_at'
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
