from rest_framework import serializers
from django.contrib.auth import authenticate
import bleach

from .models import MyUser

class MyUserLightSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['email', 'username', 'lastLogin']


class MyUserFullSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['email', 'username', 'lastLogin', 'creationDate', 'lastLogin', 'isProjectManager']


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('username', 'email')


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True,'min_length': 8},
                        'username': {'min_length': 6}
                    }

    def create(self, validated_data):
        user = MyUser.objects.create_user(bleach.clean(validated_data['email']), bleach.clean(validated_data['username']), validated_data['password'])
        return user


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials Passed.')