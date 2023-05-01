from rest_framework import serializers

from .models import *
from customUser.serializers import *
from customUser.serializers import MyUserLightSerializer



# ------------- Project Serializers ------------

class ProjectFormSerializer(serializers.ModelSerializer):
        
    manager = serializers.SlugRelatedField(slug_field='username', queryset=MyUser.objects.all())
    writers = serializers.SlugRelatedField(slug_field='username', queryset=MyUser.objects.all(), many=True)

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
        model = Comment
        fields = ['name', 'manager', 'writers', 'startDate', 'isFinished']
        lookup_field = 'name'



# ------------- Text Serializers ------------

class TextFormSerializer(serializers.ModelSerializer):

    project = serializers.SlugRelatedField(slug_field='name', queryset=Project.objects.all())
    
    class Meta:
        model = Text
        fields = ['project', 'body']

class TextLightSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(slug_field='username', queryset=MyUser.objects.all())
    project = serializers.SlugRelatedField(slug_field='name', queryset=Project.objects.all())

    class Meta:
        model = Text
        fields = ['author', 'project', 'body', 'creationDate']


class TextFullSerializer(serializers.ModelSerializer):

    author = MyUserLightSerializer()
    project = ProjectLightSerializer()

    class Meta:
        model = Text
        fields = ['author', 'project', 'body', 'creationDate']



# ------------- Comment Serializers ------------

class CommentFormSerializer(serializers.ModelSerializer):

    text = serializers.PrimaryKeyRelatedField(queryset=Text.objects.all())
    
    class Meta:
        model = Text
        fields = ['text', 'body']

class CommentLightSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField()
    text = serializers.PrimaryKeyRelatedField(queryset=Text.objects.all())

    class Meta:
        model = Text
        fields = ['author', 'project', 'body', 'creationDate']


class CommentFullSerializer(serializers.ModelSerializer):

    author = MyUserLightSerializer()
    text = TextLightSerializer()

    class Meta:
        model = Text
        fields = ['author', 'text', 'body', 'creationDate']
