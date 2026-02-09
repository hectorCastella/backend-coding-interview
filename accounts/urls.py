from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
]