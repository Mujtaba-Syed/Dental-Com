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
        # Get active services for the home page
        from Service.models import Service
        from Review.models import Review
        
        services = Service.objects.filter(is_active=True).prefetch_related('images').order_by('-created_at')[:3]
        # Convert to list of dictionaries to match API format
        context['services'] = [
            {
                'id': service.id,
                'name': service.name,
                'slug': service.slug,
                'description': service.description,
                'meta_description': service.meta_description,
                'image': {
                    'image': service.images.first().image.url if service.images.exists() else None,
                    'alt_text': service.images.first().alt_text if service.images.exists() else service.name
                },
                'images': [
                    {
                        'id': img.id,
                        'image': img.image.url,
                        'alt_text': img.alt_text or service.name,
                        'order': img.order
                    }
                    for img in service.images.all().order_by('order')
                ],
                'category': 'dental_services',
                'is_active': service.is_active,
                'is_featured': service.is_featured,
                'is_new': service.is_new,
                'created_at': service.created_at.isoformat()
            }
            for service in services
        ]
        
        # Get reviews for testimonials (only active/non-archived reviews)
        reviews = Review.objects.select_related('user').filter(is_archived=False).order_by('-created_at')
        context['reviews'] = reviews
        
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

class ServiceView(TemplateView):
    """Service page view"""
    template_name = 'services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all active services for the services page
        from Service.models import Service
        services = Service.objects.filter(is_active=True).prefetch_related('images').order_by('-created_at')
        # Convert to list of dictionaries to match API format
        context['services'] = [
            {
                'id': service.id,
                'name': service.name,
                'slug': service.slug,
                'description': service.description,
                'meta_description': service.meta_description,
                'image': {
                    'image': service.images.first().image.url if service.images.exists() else None,
                    'alt_text': service.images.first().alt_text if service.images.exists() else service.name
                },
                'images': [
                    {
                        'id': img.id,
                        'image': img.image.url,
                        'alt_text': img.alt_text or service.name,
                        'order': img.order
                    }
                    for img in service.images.all().order_by('order')
                ],
                'category': 'dental_services',
                'is_active': service.is_active,
                'is_featured': service.is_featured,
                'is_new': service.is_new,
                'created_at': service.created_at.isoformat()
            }
            for service in services
        ]
        return context

class SingleServiceView(TemplateView):
    """Single service page view"""
    template_name = 'service-details.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the service by ID with prefetched images
        from Service.models import Service
        service = Service.objects.prefetch_related('images').get(id=kwargs['service_id'])
        context['service'] = service
        return context


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