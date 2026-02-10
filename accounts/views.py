from accounts.serializers import LoginSerializer, UserSignupSerializer
from django.shortcuts import render
from rest_framework import generics, views
from rest_framework.permissions import AllowAny

# Create your views here.
class UserSignupView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer

class LoginView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer