from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'is_guest', 'google_id', 'profile_picture', 'created_at']
        read_only_fields = ['id', 'created_at']


class GuestUserSerializer(serializers.Serializer):
    """
    Serializer for guest user creation
    """
    session_id = serializers.CharField(required=False)
    
    def create(self, validated_data):
        import uuid
        session_id = validated_data.get('session_id') or str(uuid.uuid4())
        
        # Create guest user
        user = User.objects.create(
            username=f"guest_{session_id[:8]}",
            is_guest=True,
            guest_session_id=session_id,
            is_active=True
        )
        return user


class GoogleAuthSerializer(serializers.Serializer):
    """
    Serializer for Google OAuth authentication
    """
    id_token = serializers.CharField(required=True)
    
    def validate_id_token(self, value):
        """
        Validate Google ID token
        """
        from google.oauth2 import id_token
        from google.auth.transport import requests
        from django.conf import settings
        
        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                value, 
                requests.Request(), 
                settings.GOOGLE_OAUTH_CLIENT_ID
            )
            
            # Verify the issuer
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise serializers.ValidationError('Invalid token issuer')
            
            return idinfo
            
        except Exception as e:
            raise serializers.ValidationError(f'Invalid Google token: {str(e)}')
    
    def create(self, validated_data):
        idinfo = validated_data['id_token']
        
        # Extract user information
        google_id = idinfo['sub']
        email = idinfo.get('email')
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name', '')
        profile_picture = idinfo.get('picture', '')
        
        # Check if user already exists
        user, created = User.objects.get_or_create(
            google_id=google_id,
            defaults={
                'email': email,
                'username': email.split('@')[0] if email else f"google_{google_id[:8]}",
                'first_name': first_name,
                'last_name': last_name,
                'profile_picture': profile_picture,
                'is_active': True
            }
        )
        
        # Update user info if not created (in case of updates)
        if not created:
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.profile_picture = profile_picture
            user.save()
        
        return user


class TokenSerializer(serializers.Serializer):
    """
    Serializer for token response
    """
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()


def get_tokens_for_user(user):
    """
    Generate JWT tokens for a user
    """
    refresh = RefreshToken.for_user(user)
    
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user).data
    }

