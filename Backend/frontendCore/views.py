from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Appointment
from Product.models import Product
import json

# Create your views here.

class HomeView(TemplateView):
    """Home page view"""
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get active products for the home page with their primary images
        from Product.serializers import ProductListSerializer
        products = Product.objects.filter(is_active=True).prefetch_related('images').order_by('-created_at')[:3]
        # Serialize the products to match API format
        serializer = ProductListSerializer(products, many=True)
        context['products'] = serializer.data
        return context

class Home2View(TemplateView):
    """Alternative home page view"""
    template_name = 'index_2.html'

class AboutView(TemplateView):
    """About page view"""
    template_name = 'about.html'

class ShopView(TemplateView):
    """Shop page view"""
    template_name = 'shop.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all active products for the shop page
        from Product.serializers import ProductListSerializer
        products = Product.objects.filter(is_active=True).prefetch_related('images').order_by('-created_at')
        # Serialize the products to match API format
        serializer = ProductListSerializer(products, many=True)
        context['products'] = serializer.data
        return context

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


class AppointmentView(TemplateView):
    """Appointment page view"""
    template_name = 'appointment.html'

def book_appointment(request):
    """Handle appointment booking form submission"""
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            appointment_date = request.POST.get('appointment_date', '')
            appointment_time = request.POST.get('appointment_time', '')
            service = request.POST.get('service', '')
            message = request.POST.get('message', '').strip()
            
            # Basic validation
            if not all([first_name, last_name, email, phone, appointment_date, appointment_time, service]):
                return JsonResponse({
                    'success': False,
                    'message': 'Please fill in all required fields.'
                })
            
            # Clean phone number (remove formatting)
            phone_clean = ''.join(filter(str.isdigit, phone))
            
            # Create appointment
            appointment = Appointment.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone_clean,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                service=service,
                message=message
            )
            
            # Send confirmation email (if email is configured)
            try:
                if hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST:
                    send_mail(
                        'Appointment Booking Confirmation',
                        f'''
Dear {first_name} {last_name},

Thank you for booking an appointment with our dental clinic.

Appointment Details:
- Date: {appointment_date}
- Time: {appointment_time}
- Service: {dict(Appointment.SERVICE_CHOICES)[service]}
- Status: Pending Confirmation

We will contact you within 24 hours to confirm your appointment.

If you need to make any changes or have questions, please call us at +1 (555) 123-4567.

Best regards,
Dental Clinic Team
                        ''',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=True,
                    )
            except Exception as e:
                # Log error but don't fail the appointment creation
                print(f"Email sending failed: {e}")
            
            return JsonResponse({
                'success': True,
                'message': 'Appointment request submitted successfully! We will contact you within 24 hours to confirm your booking.',
                'appointment_id': appointment.id
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'An error occurred while processing your request: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    })