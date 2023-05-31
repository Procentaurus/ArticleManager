from rest_framework import serializers
import bleach

from .models import *
from customUser.serializers import MyUserLightSerializer, MyUserFullSerializer



# ------------- Publication Serializers ------------

class PublicationFormSerializer(serializers.ModelSerializer):

    manager = serializers.SlugRelatedField(slug_field='username', queryset=MyUser.objects.all())

    def validate(self, attrs):

        sanitized_attrs = {"manager": attrs["manager"]}
        proper_lengths = {"title":80, "body":5000, "isAvailable":10}
        errors = {}
        error_counter = 0

        for key, value in proper_lengths.items():
            if len(str(attrs[key])) > value:
                errors[error_counter] = f"Input for field {key} is too long."
                error_counter += 1

            sanitized_value = bleach.clean(str(attrs[key]))
            sanitized_attrs[key] = sanitized_value

        if error_counter > 0:
            return serializers.ValidationError(errors)
        else:
            return sanitized_attrs

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
        fields = ["manager", "title", "body", "addingDate"]


class PublicationInternalMultiSerializer(serializers.ModelSerializer):

    manager = MyUserLightSerializer()

    class Meta:
        model = Publication
        fields = ["manager", "title", "isAvailable", "addingDate", "numberOfDownloads"]


class PublicationInternalSingleSerializer(serializers.ModelSerializer):

    manager = MyUserLightSerializer()

    class Meta:
        model = Publication
        fields = ["manager", "title", "isAvailable", "addingDate", "numberOfDownloads", "body"]
