"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.authtoken.views import obtain_auth_token
from accounts import views  # Make sure to import views from the accounts app
from rest_framework_simplejwt.tokens import RefreshToken

# Import necessary Django functions
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Register view for creating a new user
@api_view(['POST'])
def register(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already in use"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(email=email, password=password)
    token = RefreshToken.for_user(user)

    # Send confirmation email
    send_mail(
        'Confirm your registration',
        'Please confirm your email address.',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

    return Response({"message": "User created successfully, confirmation email sent", "token": str(token)}, status=status.HTTP_201_CREATED)


# Login view for authenticating users
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, username=email, password=password)
    
    if user is None:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    
    token = RefreshToken.for_user(user)
    return Response({"token": str(token)}, status=status.HTTP_200_OK)


# URL configurations
urlpatterns = [
    path('register/', views.register),  # Pointing to the correct views
    path('login/', views.login),        # Pointing to the correct views
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),  # Include URLs from the accounts app
    path('api/token/login/', obtain_auth_token, name='api_token_auth'),  # Token-based login for DRF
]

# Serve static files during development
urlpatterns += staticfiles_urlpatterns()
