from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Cart, CartItem
from .serializers import (
    CartSerializer, 
    AddToCartSerializer, 
    UpdateCartItemSerializer,
    CartItemSerializer
)
from Product.models import Product


# Template view for frontend
class CartTemplateView(TemplateView):
    """Template view for cart page"""
    template_name = 'cart.html'


# API Views
class CartAPIView(APIView):
    """
    Get user's cart with all items
    GET /api/cart/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user's cart"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddToCartAPIView(APIView):
    """
    Add item to cart or update quantity if already exists
    POST /api/cart/add/
    Body: {"product_id": 1, "quantity": 2}
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Add item to cart"""
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            
            # Get or create cart
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Get product
            product = get_object_or_404(Product, id=product_id, is_active=True)
            
            # Get or create cart item
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            # If item already exists, increase quantity
            if not item_created:
                cart_item.quantity += quantity
                cart_item.save()
            
            cart_serializer = CartSerializer(cart)
            return Response({
                'message': 'Item added to cart successfully',
                'cart': cart_serializer.data
            }, status=status.HTTP_201_CREATED if item_created else status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IncreaseCartItemAPIView(APIView):
    """
    Increase cart item quantity by 1
    POST /api/cart/increase/<cart_item_id>/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, cart_item_id):
        """Increase cart item quantity"""
        cart_item = get_object_or_404(
            CartItem, 
            id=cart_item_id, 
            cart__user=request.user
        )
        
        cart_item.quantity += 1
        cart_item.save()
        
        cart_serializer = CartSerializer(cart_item.cart)
        return Response({
            'message': 'Item quantity increased',
            'cart': cart_serializer.data
        }, status=status.HTTP_200_OK)


class DecreaseCartItemAPIView(APIView):
    """
    Decrease cart item quantity by 1
    If quantity becomes 0, item is removed
    POST /api/cart/decrease/<cart_item_id>/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, cart_item_id):
        """Decrease cart item quantity"""
        cart_item = get_object_or_404(
            CartItem, 
            id=cart_item_id, 
            cart__user=request.user
        )
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            message = 'Item quantity decreased'
        else:
            cart_item.delete()
            message = 'Item removed from cart'
        
        cart_serializer = CartSerializer(cart_item.cart)
        return Response({
            'message': message,
            'cart': cart_serializer.data
        }, status=status.HTTP_200_OK)


class UpdateCartItemAPIView(APIView):
    """
    Update cart item quantity to a specific value
    PUT /api/cart/update/<cart_item_id>/
    Body: {"quantity": 5}
    """
    permission_classes = [IsAuthenticated]
    
    def put(self, request, cart_item_id):
        """Update cart item quantity"""
        cart_item = get_object_or_404(
            CartItem, 
            id=cart_item_id, 
            cart__user=request.user
        )
        
        serializer = UpdateCartItemSerializer(data=request.data)
        if serializer.is_valid():
            cart_item.quantity = serializer.validated_data['quantity']
            cart_item.save()
            
            cart_serializer = CartSerializer(cart_item.cart)
            return Response({
                'message': 'Item quantity updated',
                'cart': cart_serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveFromCartAPIView(APIView):
    """
    Remove item from cart completely
    DELETE /api/cart/remove/<cart_item_id>/
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, cart_item_id):
        """Remove item from cart"""
        cart_item = get_object_or_404(
            CartItem, 
            id=cart_item_id, 
            cart__user=request.user
        )
        
        cart = cart_item.cart
        cart_item.delete()
        
        cart_serializer = CartSerializer(cart)
        return Response({
            'message': 'Item removed from cart',
            'cart': cart_serializer.data
        }, status=status.HTTP_200_OK)


class ClearCartAPIView(APIView):
    """
    Clear all items from cart
    POST /api/cart/clear/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Clear all items from cart"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        
        cart_serializer = CartSerializer(cart)
        return Response({
            'message': 'Cart cleared successfully',
            'cart': cart_serializer.data
        }, status=status.HTTP_200_OK)


class GetItemCountAPIView(APIView):
    """
    Get the number of quantity of items in the cart
    GET /api/cart/item-count/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get the number of quantity of total items in the cart"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        return Response({'total_quantity': sum(item.quantity for item in cart.items.all())}, status=status.HTTP_200_OK)