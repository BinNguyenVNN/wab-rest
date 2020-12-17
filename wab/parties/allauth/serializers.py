from abc import ABC

from django.contrib.auth.models import update_last_login
from django.db.models import Q
from rest_framework import serializers
from wab.core.users.models import User
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class RegisterUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def get_password2(self, obj):
        return obj.password2

    def get_password1(self, obj):
        return obj.password1

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginUserSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        password = data.get("password", None)
        email = data.get("email", None)

        user = User.objects.filter((Q(email=email) | Q(username=email))).first()
        if user:
            if not user.is_active:
                raise serializers.ValidationError('A user is not verify.')
            user = authenticate(username=user.username, password=password)
            if user is None:
                raise serializers.ValidationError('A user with this username and password is not found.')
            try:
                payload = JWT_PAYLOAD_HANDLER(user)
                jwt_token = JWT_ENCODE_HANDLER(payload)
                update_last_login(None, user)
            except User.DoesNotExist:
                raise serializers.ValidationError('User with given email and password does not exists')
            return {
                'username': user.username,
                'phone': user.email,
                'token': jwt_token
            }
        else:
            raise serializers.ValidationError('A user with this username and password is not found.')


class ResetPasswordRequestSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    email = serializers.CharField(max_length=255)
