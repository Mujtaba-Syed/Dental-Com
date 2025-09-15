from django.urls import path
from . import views

app_name = 'service_api'

urlpatterns = [
    # Service endpoint
    path('services/', views.ServiceListView.as_view(), name='service-list'),
]
