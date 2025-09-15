from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Q

from .models import Product, ProductImage
from .serializers import (
    ProductSerializer, 
    ProductListSerializer, 
    ProductCreateUpdateSerializer,
    ProductImageSerializer
)

class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductListCreateView(generics.ListCreateAPIView):
    """
    List all products or create a new product
    """
    queryset = Product.objects.filter(is_active=True)
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductListSerializer
        return ProductCreateUpdateSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a product
    """
    queryset = Product.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        return ProductCreateUpdateSerializer

class ProductByCategoryView(generics.ListAPIView):
    """
    List products by category
    """
    serializer_class = ProductListSerializer
    pagination_class = ProductPagination
    
    def get_queryset(self):
        category = self.kwargs['category']
        return Product.objects.filter(category=category, is_active=True)

class ProductSearchView(generics.ListAPIView):
    """
    Search products by name or description
    """
    serializer_class = ProductListSerializer
    pagination_class = ProductPagination
    
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return Product.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query),
                is_active=True
            )
        return Product.objects.filter(is_active=True)

class ProductImageListCreateView(generics.ListCreateAPIView):
    """
    List all images for a product or create a new image
    """
    serializer_class = ProductImageSerializer
    
    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductImage.objects.filter(product_id=product_id)

class ProductImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a product image
    """
    serializer_class = ProductImageSerializer
    
    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductImage.objects.filter(product_id=product_id)

@api_view(['GET'])
def product_stats(request):
    """
    Get product statistics
    """
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    categories = Product.objects.values_list('category', flat=True).distinct()
    
    stats = {
        'total_products': total_products,
        'active_products': active_products,
        'inactive_products': total_products - active_products,
        'categories': list(categories),
        'categories_count': len(categories)
    }
    
    return Response(stats)
