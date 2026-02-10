import datetime

import logging
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)

class UserSignupSerializer(serializers.ModelSerializer):
    """Serializer for creating a new user
        depedning of the data send it will create an customer or a driver
    ."""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    """Handles user login and token generation."""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Incorrect username or password.")
        data["user"] = user
        return data

    def create(self, validated_data):
        user = validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        validated_data["token"] = token.key
        return validated_data
