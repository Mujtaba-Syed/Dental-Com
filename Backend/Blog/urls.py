from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Blog Post URLs
    path('posts/', views.BlogPostListCreateView.as_view(), name='post-list-create'),
    path('posts/search/', views.BlogPostSearchView.as_view(), name='post-search'),
    path('posts/featured/', views.FeaturedBlogPostsView.as_view(), name='post-featured'),
    path('posts/<int:id>/', views.BlogPostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
    path('posts/<int:id>/increment-view/', views.increment_view_count, name='post-increment-view'),
    path('posts/<int:id>/increment-like/', views.increment_like_count, name='post-increment-like'),
    path('posts/<int:id>/decrement-like/', views.decrement_like_count, name='post-decrement-like'),
]
