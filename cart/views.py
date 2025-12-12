from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from products.models import Product
from .serializers import (
    CartSerializer, 
    AddToCartSerializer, 
    UpdateCartItemSerializer
)


class AddToCartView(APIView):
    """Add items to cart"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        product = get_object_or_404(Product, id=product_id)

        # Check stock availability
        if product.stock < quantity:
            return Response(
                {'error': 'Insufficient stock available'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get or create cart for user
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Get or create cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            # Update quantity if item already exists
            new_quantity = cart_item.quantity + quantity
            if product.stock < new_quantity:
                return Response(
                    {'error': 'Insufficient stock available'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity = new_quantity
            cart_item.save()

        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_201_CREATED)


class UpdateCartView(APIView):
    """Update cart item quantity"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UpdateCartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Cart not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Product not found in cart'},
                status=status.HTTP_404_NOT_FOUND
            )

        if quantity == 0:
            # Remove item if quantity is 0
            cart_item.delete()
        else:
            # Check stock availability
            if cart_item.product.stock < quantity:
                return Response(
                    {'error': 'Insufficient stock available'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity = quantity
            cart_item.save()

        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_200_OK)


class GetCartView(APIView):
    """Get user's cart"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClearCartView(APIView):
    """Clear all items from cart"""
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
            return Response(
                {'message': 'Cart cleared successfully'},
                status=status.HTTP_200_OK
            )
        except Cart.DoesNotExist:
            return Response(
                {'message': 'Cart is already empty'},
                status=status.HTTP_200_OK
            )
