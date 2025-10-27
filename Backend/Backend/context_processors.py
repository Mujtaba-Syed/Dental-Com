from django.conf import settings

def api_config(request):
    """
    Context processor to make API configuration available in all templates
    """
    return {
        'API_BASE_URL': settings.API_BASE_URL,
        'BASE_URL': settings.BASE_URL,
        'GOOGLE_CLIENT_ID': settings.GOOGLE_OAUTH_CLIENT_ID,
    }
