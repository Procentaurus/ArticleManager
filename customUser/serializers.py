from rest_framework import serializers

from .models import MyUser

class MyUserLightSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['email', 'username', 'lastLogin']


class MyUserFullSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['email', 'username', 'lastLogin', 'craetionDate', 'lastLogin', 'isProjectManager']