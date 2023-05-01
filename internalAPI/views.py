from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
import datetime

from .serializers import *
from .models import *


#  -----------    classes for Text model    ---------------

class TextList(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
  
    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.request.user.isEditor:
                return TextFullSerializer
            else:
                return TextLightSerializer
        else:
            return TextFormSerializer

    def get_queryset(self):
        
        user = self.request.user

        if user.isEditor:
            return Text.objects.all()
        else:
            projects = Project.objects.filter(writers__in=[user])
            texts = Text.objects.filter(project__in=projects)
            return texts
      
    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, creationDate=datetime.datetime.now())    

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class TextDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    def get_serializer_class(self):
        if self.request.method in ['GET', 'DELETE']:
            if self.request.user.isEditor:
                return TextFullSerializer
            else: 
                return TextLightSerializer
        else:
            return TextFormSerializer
        
    def get_queryset(self):
        return Text.objects.all()
            
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

#  -----------    classes for Comment model    ---------------

class CommentList(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
  
    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.request.user.isEditor:
                return CommentFullSerializer
            else:
                return CommentLightSerializer
        else:
            return CommentFormSerializer

    def get_queryset(self):
        
        user = self.request.user

        if user.isEditor:
            return Comment.objects.all()
        else:
            projects = Project.objects.filter(writers__in=[user])
            texts = Text.objects.filter(project__in=projects)
            comments = Comment.objects.filter(text__in=texts)
            return comments
      
    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, creationDate=datetime.datetime.now())    

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    
class CommentDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    def get_serializer_class(self):
        if self.request.method in ['GET', 'DELETE']:
            if self.request.user.isEditor:
                return CommentFullSerializer
            else: 
                return CommentLightSerializer
        else:
            return CommentFormSerializer
        
    def get_queryset(self):
        return Comment.objects.all()
            
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


#  -----------    classes for Project model    ---------------

class ProjectList(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
  
    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.request.user.isEditor:
                return ProjectFullSerializer
            else:
                return ProjectLightSerializer
        else:
            return ProjectFormSerializer

    def get_queryset(self):
        
        user = self.request.user

        if user.isEditor:
            return Project.objects.all()
        else:
            return Project.objects.filter(writers__in=[user])

      
    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)
    
    def perform_create(self, serializer):
        instance = serializer.save()

        newManager = instance.manager
        instance.writers.add(newManager)
        newManager.isProjectManager = True
        newManager.save()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    
class ProjectDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    lookup_field = 'name'
    
    def get_serializer_class(self):
        if self.request.method in ['GET', 'DELETE']:
            if self.request.user.isEditor:
                return ProjectFullSerializer
            else: 
                return ProjectLightSerializer
        else:
            return ProjectFormSerializer
        
    def get_queryset(self):
        return Project.objects.all()
    
    def perform_destroy(self, instance):
        manager = instance.manager
        manager.isProjectManager = False
        manager.save()
        
        instance.delete()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)