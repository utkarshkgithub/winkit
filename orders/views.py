from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Order, OrderItem, OrderStatusHistory
from cart.models import Cart
from .serializers import (
    OrderSerializer,
    CreateOrderSerializer,
    UpdateOrderStatusSerializer,
    OrderStatusHistorySerializer
)


class CreateOrderView(APIView):
    """Create a new order from cart items"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if cart.items.count() == 0:
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create order within a transaction
        with transaction.atomic():
            # Calculate total amount
            total_amount = cart.total_price

            # Create order
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount,
                shipping_address=serializer.validated_data['shipping_address'],
                phone_number=serializer.validated_data['phone_number']
            )

            # Create order items from cart items
            for cart_item in cart.items.all():
                # Check stock availability
                if cart_item.product.stock < cart_item.quantity:
                    transaction.set_rollback(True)
                    return Response(
                        {'error': f'Insufficient stock for {cart_item.product.name}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Create order item
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    product_name=cart_item.product.name,
                    quantity=cart_item.quantity,
                    price=cart_item.product.discounted_price
                )

                # Update product stock
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()

            # Clear cart after successful order
            cart.items.all().delete()

        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    """Get order details by ID"""
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        
        # Users can only view their own orders, admins can view all
        if not request.user.is_staff and order.user != request.user:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserOrdersView(APIView):
    """Get all orders for a specific user"""
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        # Users can only view their own orders, admins can view all
        if not request.user.is_staff and request.user.id != user_id:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )

        orders = Order.objects.filter(user_id=user_id).prefetch_related('items')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateOrderStatusView(APIView):
    """Update order status (admin only)"""
    permission_classes = [IsAdminUser]

    def put(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        
        serializer = UpdateOrderStatusSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Set changed_by to track who made the change in history
        order._changed_by = request.user
        order.order_status = serializer.validated_data['order_status']
        order.save()

        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_200_OK)


class TimelineView(APIView):
    """Get order status history timeline"""
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        
        # Users can only view their own order history, admins can view all
        if not request.user.is_staff and order.user != request.user:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get history ordered chronologically (oldest first for customer-facing timeline)
        history = order.history.all().order_by('changed_at')
        serializer = OrderStatusHistorySerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

