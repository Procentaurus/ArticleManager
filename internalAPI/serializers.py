from rest_framework import serializers
import bleach

from .models import *
from customUser.serializers import *
from customUser.serializers import MyUserLightSerializer



# ------------- Project Serializers ------------

class ProjectFormSerializer(serializers.ModelSerializer):
        
    manager = serializers.SlugRelatedField(slug_field='username', queryset=MyUser.objects.all())
    writers = serializers.SlugRelatedField(slug_field='username', queryset=MyUser.objects.all(), many=True)

    def validate(self, attrs):

        sanitized_attrs = {"manager": attrs["manager"], "writers": attrs["writers"], "startDate": attrs["startDate"]}
        proper_lengths = {"name":100}
        errors = {}
        error_counter = 0

        for key, value in proper_lengths.items(): # attrs
            try:
                if len(attrs[key]) > value:
                    errors[error_counter] = f"Input for field {key} is too long."
                    error_counter += 1
            except:
                raise serializers.ValidationError("No all required fields or wrong names.")

            sanitized_attrs[key] = bleach.clean(attrs[key])
            
        if error_counter > 0:
            raise serializers.ValidationError(errors)
        else:
            return sanitized_attrs
    
    class Meta:
        model = Project
        fields = ['name', 'manager', 'writers', 'startDate']

class ProjectLightSerializer(serializers.ModelSerializer):

    manager = MyUserLightSerializer()
    writers = MyUserLightSerializer(many=True)

    class Meta:
        model = Project
        fields = ['name', 'manager', 'writers', 'startDate', 'isFinished']
        lookup_field = 'name'


class ProjectFullSerializer(serializers.ModelSerializer):

    manager = MyUserFullSerializer()
    writers = MyUserFullSerializer(many=True)

    class Meta:
        model = Project
        fields = ['name', 'manager', 'writers', 'startDate', 'isFinished']
        lookup_field = 'name'


# ------------- Text Serializers ------------

class TextFormSerializer(serializers.ModelSerializer):

    project = serializers.SlugRelatedField(slug_field='name', queryset=Project.objects.all())

    def validate(self, attrs):

        sanitized_attrs = {"project": attrs["project"]}
        proper_lengths = {"body": 1000}
        errors = {}
        error_counter = 0

        for key, value in proper_lengths.items(): # attrs
            try:
                if len(attrs[key]) > value:
                    errors[error_counter] = f"Input for field {key} is too long."
                    error_counter += 1
            except:
                raise serializers.ValidationError("No all required fields.")

            sanitized_attrs[key] = bleach.clean(attrs[key])

        if error_counter > 0:
            raise serializers.ValidationError(errors)
        else:
            return sanitized_attrs
           
    class Meta:
        model = Text
        fields = ['project', 'body']

class TextLightSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(slug_field='username', queryset=MyUser.objects.all())
    project = serializers.SlugRelatedField(slug_field='name', queryset=Project.objects.all())

    class Meta:
        model = Text
        fields = ['id','author', 'project', 'body', 'creationDate']


class TextFullSerializer(serializers.ModelSerializer):

    author = MyUserLightSerializer()
    project = ProjectLightSerializer()

    class Meta:
        model = Text
        fields = ['id','author', 'project', 'body', 'creationDate']



# ------------- Comment Serializers ------------

class CommentFormSerializer(serializers.ModelSerializer):

    text = serializers.PrimaryKeyRelatedField(queryset=Text.objects.all())


    def validate(self, attrs):
        sanitized_attrs = {"text":attrs["text"]}
        proper_lengths = {"body":1000}

        for key, value in proper_lengths.items():
            if value > len(attrs[key]):
                sanitized_value = bleach.clean(attrs[key])
                sanitized_attrs[key] = sanitized_value
            else: raise ValueError(f"Too long input for field {key}")

        return sanitized_attrs
    
    class Meta:
        model = Comment
        fields = ['text', 'body']


class CommentLightSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField()
    text = serializers.PrimaryKeyRelatedField(queryset=Text.objects.all())

    class Meta:
        model = Comment
        fields = ["id",'author','body','creationDate', 'text']



class CommentFullSerializer(serializers.ModelSerializer):

    author = MyUserLightSerializer()
    text = TextLightSerializer()

    class Meta:
        model = Comment
        fields = ["id",'author', 'text', 'body', 'creationDate']
