from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
import datetime
from rest_framework.exceptions import ValidationError

from knox.auth import TokenAuthentication

from .serializers import *
from .models import *
from .permissions import *
from ArticleManager.throttlers import TextRateThrottle, CommentRateThrottle, ProjectRateThrottle


#  -----------    classes for Text model    ---------------

class TextList(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
  
    permission_classes = (
        IsAuthenticated & ((~ChoseSafeMethod & WantToAddTextToOneOfHisProjects) | ChoseSafeMethod),
    )
    throttle_classes = (TextRateThrottle,)

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

    permission_classes = (
        IsAuthenticated &
        (    IsAuthor |
            (ChoseSafeMethod & WantToSeeTextOfHisProject) |
            (ChoseDeleteMethod & IsManagerOfProjectTextBelongTo)
        ),
    )

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
    
    def perform_update(self, serializer):
        newProject = Project.objects.get(name=serializer.validated_data["project"])
        if self.request.user not in newProject.writers.all():
             raise ValidationError("You cant add text to chosen Project.")

        serializer.save()
            
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

#  -----------    classes for Comment model    ---------------

class CommentList(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):

    permission_classes = (
        IsAuthenticated & ((~ChoseSafeMethod & WantToAddCommentToTextInOneOfHisProjects) | ChoseSafeMethod),
    )
    throttle_classes = (CommentRateThrottle,)
  
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

    permission_classes = (
        IsAuthenticated &
        (    IsAuthor |
            (ChoseSafeMethod & WantToSeeCommentOfHisProject) |
            (ChoseDeleteMethod & IsManagerOfProjectCommentBelongTo)
        ),
    )

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
    
    def perform_update(self, serializer):
        text = serializer.validated_data["text"]
        if self.request.user not in text.project.writers.all():
             raise ValidationError("You cant add comment to chosen Text.")

        serializer.save()
            
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


#  -----------    classes for Project model    ---------------

class ProjectList(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
    
    permission_classes = (IsAuthenticated & (IsEditor | ChoseSafeMethod),)
    throttle_classes = (ProjectRateThrottle,)

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
        
        newManager = MyUser.objects.get(username=serializer.validated_data["manager"])
        if newManager.isProjectManager:
            raise ValidationError("The chosen user can't become manager. He already is.")
        else:
            instance = serializer.save()
            instance.writers.add(newManager)
            newManager.isProjectManager = True
            newManager.save()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    
class ProjectDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    lookup_field = 'name'
    permission_classes = (
        IsAuthenticated &
            (IsEditor | (IsProjectManager | ~ChoseDeleteMethod) | (ChoseSafeMethod & WantToSeeHisProject)),
    ) 
    
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

    def perform_update(self, serializer):

        project = Project.objects.get(name=self.kwargs['name'])

        if project.manager != serializer.validated_data["manager"]:
            project.manager.isProjectManager = False
            project.manager.save()
            
        instance = serializer.save()
        instance.manager.isProjectManager = True
        instance.manager.save()
        if instance.manager not in instance.writers.all():
            instance.writers.add(instance.manager)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)