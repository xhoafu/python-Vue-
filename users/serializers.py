from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user','phone','profile_picture','date_of_birth','gender']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),  # 使用 .get() 以防字段缺失
            password=validated_data['password']
        )
        return user