from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "name", "avatar"]

        # extra_kwargs = {
        #     "url": {"view_name": "user-detail", "lookup_field": "username"}
        # }


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "description", "avatar"]
