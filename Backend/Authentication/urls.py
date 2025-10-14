from django.urls import path
from .views import (
    GuestLoginView,
    GoogleAuthView,
    VerifyTokenView,
    RefreshTokenView
)

app_name = 'authentication'

urlpatterns = [
    path('guest-login/', GuestLoginView.as_view(), name='guest_login'),
    path('google-auth/', GoogleAuthView.as_view(), name='google_auth'),
    path('verify-token/', VerifyTokenView.as_view(), name='verify_token'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh_token'),
]
