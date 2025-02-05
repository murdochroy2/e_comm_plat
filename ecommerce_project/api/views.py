from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Product, Order, OrderItem
from .serializers import (
    ProductSerializer, 
    OrderCreateSerializer,
    OrderSerializer
)
from .exceptions import InsufficientStockError

class ProductListCreateView(APIView):
    def get(self, request):
        """List all products"""
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new product"""
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)

    def get(self, request, pk):
        """Retrieve a product"""
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        """Update a product"""
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a product"""
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderListCreateView(APIView):
    def get(self, request):
        """List all orders"""
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        """Create a new order"""
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate total and validate stock
        total_price = 0
        order_items = []
        
        for item in serializer.validated_data['items']:
            product = Product.objects.select_for_update().get(
                id=item['product_id']
            )
            
            if product.stock < item['quantity']:
                raise InsufficientStockError(
                    f"Insufficient stock for product {product.name}"
                )
            
            item_price = product.price * item['quantity']
            total_price += item_price
            
            order_items.append({
                'product': product,
                'quantity': item['quantity'],
                'price': item_price
            })

        # Create order and order items
        order = Order.objects.create(
            total_price=total_price,
            status='pending'
        )

        for item in order_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price']
            )
            # Update stock
            item['product'].stock -= item['quantity']
            item['product'].save()

        order.status = 'completed'
        order.save()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )

class OrderDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Order, pk=pk)

    def get(self, request, pk):
        """Retrieve an order"""
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data) 