from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Template view
    path('template/', views.CartTemplateView.as_view(), name='cart_template'),
    
    # API endpoints
    path('', views.CartAPIView.as_view(), name='cart'),
    path('add/', views.AddToCartAPIView.as_view(), name='add_to_cart'),
    path('increase/<int:cart_item_id>/', views.IncreaseCartItemAPIView.as_view(), name='increase_cart_item'),
    path('decrease/<int:cart_item_id>/', views.DecreaseCartItemAPIView.as_view(), name='decrease_cart_item'),
    path('update/<int:cart_item_id>/', views.UpdateCartItemAPIView.as_view(), name='update_cart_item'),
    path('remove/<int:cart_item_id>/', views.RemoveFromCartAPIView.as_view(), name='remove_from_cart'),
    path('clear/', views.ClearCartAPIView.as_view(), name='clear_cart'),
    path('item-count/', views.GetItemCountAPIView.as_view(), name='get_item_count'),
]