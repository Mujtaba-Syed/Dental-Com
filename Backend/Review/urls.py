from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    # All reviews endpoint
    path('reviews-list/', 
         views.AllReviewsListView.as_view(), 
         name='all-reviews-list'),
    
    # Product-specific review endpoints
    path('products/<int:product_id>/reviews/', 
         views.ReviewListCreateView.as_view(), 
         name='product-reviews-list-create'),
    
    path('products/<int:product_id>/reviews/<int:review_id>/', 
         views.ReviewDetailView.as_view(), 
         name='product-review-detail'),
    
    # Review statistics
    path('products/<int:product_id>/reviews/stats/', 
         views.product_review_stats, 
         name='product-review-stats'),
    
    # Mark review as helpful
    path('products/<int:product_id>/reviews/<int:review_id>/helpful/', 
         views.mark_review_helpful, 
         name='mark-review-helpful'),
    
    # User's own reviews
    path('my-reviews/', 
         views.UserReviewListView.as_view(), 
         name='user-reviews-list'),
]
