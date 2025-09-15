from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'product_api'

urlpatterns = [
    # Product endpoints
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/category/<str:category>/', views.ProductByCategoryView.as_view(), name='product-by-category'),
    path('products/search/', views.ProductSearchView.as_view(), name='product-search'),
    path('products/stats/', views.product_stats, name='product-stats'),
    
    # Product Image endpoints
    path('products/<int:product_id>/images/', views.ProductImageListCreateView.as_view(), name='product-image-list-create'),
    path('products/<int:product_id>/images/<int:pk>/', views.ProductImageDetailView.as_view(), name='product-image-detail'),
]
