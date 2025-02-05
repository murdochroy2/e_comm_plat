import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from decimal import Decimal
from api.models import Product, Order
from django.test import TestCase
from rest_framework.test import APITestCase
from api.models import OrderItem
from api.views import ProductListCreateView, ProductDetailView, OrderListCreateView, OrderDetailView
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def product_data():
    return {
        'name': 'Test Product',
        'description': 'Test Description',
        'price': '10.00',
        'stock': 10
    }

@pytest.fixture
def create_product(product_data):
    return Product.objects.create(**product_data)

@pytest.mark.django_db
class TestProductAPI:
    def test_create_product(self, api_client, product_data):
        url = reverse('product-list')
        response = api_client.post(url, product_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.count() == 1
        assert Product.objects.get().name == 'Test Product'

    def test_list_products(self, api_client, create_product):
        url = reverse('product-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_retrieve_product(self, api_client, create_product):
        url = reverse('product-detail', args=[create_product.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == create_product.name

    def test_update_product(self, api_client, create_product):
        url = reverse('product-detail', args=[create_product.id])
        updated_data = {
            'name': 'Updated Product',
            'description': 'Updated Description',
            'price': '15.00',
            'stock': 20
        }
        response = api_client.put(url, updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Product'

    def test_delete_product(self, api_client, create_product):
        url = reverse('product-detail', args=[create_product.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Product.objects.count() == 0

@pytest.mark.django_db
class TestOrderAPI:
    def test_create_order(self, api_client, create_product):
        url = reverse('order-list')
        order_data = {
            'items': [
                {
                    'product_id': create_product.id,
                    'quantity': 2
                }
            ]
        }
        response = api_client.post(url, order_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Order.objects.count() == 1
        
        # Check stock was updated
        product = Product.objects.get(id=create_product.id)
        assert product.stock == 8

    def test_insufficient_stock(self, api_client, create_product):
        url = reverse('order-list')
        order_data = {
            'items': [
                {
                    'product_id': create_product.id,
                    'quantity': 20  # More than available stock
                }
            ]
        }
        response = api_client.post(url, order_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST 

    def test_create_order_with_sufficient_stock(self, api_client, create_product):
        url = reverse('order-list')
        order_data = {
            'items': [
                {
                    'product_id': create_product.id,
                    'quantity': 1  # Sufficient stock
                }
            ]
        }
        response = api_client.post(url, order_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Order.objects.count() == 1
        
        # Check stock was updated
        product = Product.objects.get(id=create_product.id)
        assert product.stock == 9  # Stock should decrease by 1

    def test_create_order_with_zero_quantity(self, api_client, create_product):
        url = reverse('order-list')
        order_data = {
            'items': [
                {
                    'product_id': create_product.id,
                    'quantity': 0  # Zero quantity
                }
            ]
        }
        response = api_client.post(url, order_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # Expecting a bad request

    def test_create_order_with_negative_quantity(self, api_client, create_product):
        url = reverse('order-list')
        order_data = {
            'items': [
                {
                    'product_id': create_product.id,
                    'quantity': -1  # Negative quantity
                }
            ]
        }
        response = api_client.post(url, order_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # Expecting a bad request

    def test_create_order_with_insufficient_stock(self, api_client, create_product):
        url = reverse('order-list')
        order_data = {
            'items': [
                {
                    'product_id': create_product.id,
                    'quantity': 20  # More than available stock
                }
            ]
        }
        response = api_client.post(url, order_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # Expecting a bad request 