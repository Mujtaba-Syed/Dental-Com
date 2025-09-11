from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

# Create your views here.

class HomeView(TemplateView):
    """Home page view"""
    template_name = 'index.html'

class Home2View(TemplateView):
    """Alternative home page view"""
    template_name = 'index_2.html'

class AboutView(TemplateView):
    """About page view"""
    template_name = 'about.html'

class ShopView(TemplateView):
    """Shop page view"""
    template_name = 'shop.html'

class SingleProductView(TemplateView):
    """Single product page view"""
    template_name = 'single-product.html'

class CartView(TemplateView):
    """Shopping cart page view"""
    template_name = 'cart.html'

class CheckoutView(TemplateView):
    """Checkout page view"""
    template_name = 'checkout.html'

class ContactView(TemplateView):
    """Contact page view"""
    template_name = 'contact.html'

class NewsView(TemplateView):
    """News page view"""
    template_name = 'news.html'

class SingleNewsView(TemplateView):
    """Single news article page view"""
    template_name = 'single-news.html'

class Error404View(TemplateView):
    """404 error page view"""
    template_name = '404.html'
    status_code = 404

def mail_handler(request):
    """Handle contact form submissions"""
    if request.method == 'POST':
        # Handle form submission here
        # You can add form processing logic
        return HttpResponse('Message sent successfully!')
    return HttpResponse('Method not allowed', status=405)
