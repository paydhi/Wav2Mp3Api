from rest_framework import serializers
from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ResponseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['access_token', 'user_uuid']
