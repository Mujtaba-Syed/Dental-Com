from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import (
    GuestUserSerializer, 
    GoogleAuthSerializer, 
    UserSerializer,
    get_tokens_for_user
)


class GuestLoginView(APIView):
    """
    API View for guest user authentication
    POST: Create a guest user and return JWT tokens
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = GuestUserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            
            return Response({
                'success': True,
                'message': 'Guest user created successfully',
                'data': tokens
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': 'Failed to create guest user',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class GoogleAuthView(APIView):
    """
    API View for Google OAuth authentication
    POST: Authenticate user with Google ID token and return JWT tokens
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            
            return Response({
                'success': True,
                'message': 'Google authentication successful',
                'data': tokens
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'message': 'Google authentication failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class VerifyTokenView(APIView):
    """
    API View to verify if a token is valid
    POST: Verify access token
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        token = request.data.get('token')
        
        if not token:
            return Response({
                'success': False,
                'message': 'Token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from rest_framework_simplejwt.tokens import AccessToken
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            
            try:
                user = User.objects.get(id=user_id)
                return Response({
                    'success': True,
                    'message': 'Token is valid',
                    'data': {
                        'user': UserSerializer(user).data
                    }
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Invalid token',
                'error': str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)


class RefreshTokenView(APIView):
    """
    API View to refresh access token
    POST: Provide refresh token to get new access token
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response({
                'success': False,
                'message': 'Refresh token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            
            return Response({
                'success': True,
                'message': 'Token refreshed successfully',
                'data': {
                    'access': access_token
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Invalid refresh token',
                'error': str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)
