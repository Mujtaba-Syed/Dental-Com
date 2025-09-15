from rest_framework import generics
from .models import Service
from .serializers import ServiceSerializer

class ServiceListView(generics.ListAPIView):
    """
    Get all active services
    """
    queryset = Service.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ServiceSerializer