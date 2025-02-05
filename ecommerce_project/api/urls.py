from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from api.views import ProductDetailView, ProductListCreateView, OrderDetailView, OrderListCreateView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
] 

