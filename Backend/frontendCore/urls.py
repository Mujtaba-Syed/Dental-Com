from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    # Home pages
    path('', views.HomeView.as_view(), name='home'),
    path('home2/', views.Home2View.as_view(), name='home2'),
    
    # Main pages
    path('about/', views.AboutView.as_view(), name='about'),
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('news/', views.NewsView.as_view(), name='news'),
    
    # Product pages
    path('product/<int:product_id>/', views.SingleProductView.as_view(), name='single_product'),
    
    # Shopping cart and checkout
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    
    # News pages
    path('news/<int:news_id>/', views.SingleNewsView.as_view(), name='single_news'),
    
    # Contact form handler
    path('mail/', views.mail_handler, name='mail_handler'),
    
    # Error pages
    path('404/', views.Error404View.as_view(), name='error_404'),
]
