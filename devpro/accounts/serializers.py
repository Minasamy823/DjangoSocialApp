from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import *


class CreateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'username', 'created_at', 'last_name', 'first_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data.setdefault('is_staff', False)
        user = UserProfile(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        :param instance: the original instance
        :param validated_data: the new input data
        :return: instance.save() method
        """
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)


class UpdatePasswordSerializer(serializers.Serializer):
    """
    updating passwords
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    @staticmethod
    def validate_new_password(value):
        validate_password(value)
        return value
