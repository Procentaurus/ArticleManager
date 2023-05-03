from rest_framework import serializers

from .models import *
from customUser.serializers import MyUserLightSerializer, MyUserFullSerializer


class PublicationFormSerializer(serializers.ModelSerializer):

    manager = serializers.SlugRelatedField(slug_field='username', queryset=MyUser.objects.all())

    class Meta:
        model = Publication
        fields = ["manager", "title", "body", "isAvailable"]


class PublicationExternalMultiSerializer(serializers.ModelSerializer):

    manager = serializers.SlugRelatedField(slug_field='username', queryset=MyUser.objects.all())

    class Meta:
        model = Publication
        fields = ["manager", "title", "addingDate"]


class PublicationExternalSingleSerializer(serializers.ModelSerializer):

    manager = serializers.SlugRelatedField(slug_field='username', queryset=MyUser.objects.all())

    class Meta:
        model = Publication
        fields = ["manager", "title","body", "addingDate"]


class PublicationInternalSerializer(serializers.ModelSerializer):

    manager = MyUserLightSerializer()

    class Meta:
        model = Publication
        fields = ["manager", "title", "isAvailable", "addingDate", "numberOfDownloads"]
