from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated
import datetime
from rest_framework.exceptions import ValidationError

from knox.auth import TokenAuthentication
import bleach

from .serializers import *
from .models import *
from ArticleManager.permissions import *
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
        serializer.is_valid(raise_exception=True)

        instance = serializer.create({**serializer.validated_data, 'author': self.request.user, 'creationDate': datetime.datetime.now()})
        instance.save()    

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

        serializer_cleaned_data = serializer.validated_data

        try:
            instance = self.get_object()
        except:
            raise ValidationError("Text instance not found.")

        try:
            newProject = Project.objects.get(name=serializer_cleaned_data["project"])
        except:
            raise ValidationError("No such project.")
        
        if self.request.user not in newProject.writers.all():
             raise ValidationError("You cant add text to chosen Project.")

        # Update instance with cleaned data
        instance.body = serializer_cleaned_data["body"]
        if instance.project != newProject:
            instance.project = newProject

        instance.save()
            
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

#  -----------    classes for Comment model    ---------------

class CommentList(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):

    permission_classes = (
        IsAuthenticated & ((~ChoseSafeMethod & WantToAddCommentToTextInOneOfHisProjects) | ChoseSafeMethod | IsEditor),
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

        serializer.is_valid(raise_exception=True)
        instance = serializer.create({**serializer.validated_data, 'author': self.request.user, 'creationDate': datetime.datetime.now()})
        instance.save()  

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

        serializer_cleaned = serializer.validated_data
        try:
            instance = self.get_object()
        except:
            raise ValidationError("Comment instance not found.")

        if self.request.user not in instance.text.project.writers.all():
            raise ValidationError("You cant add comment to chosen Text.")

        instance.body = serializer_cleaned["body"]
        if instance.text != serializer_cleaned["text"]:
            instance.project = serializer_cleaned["text"]

        instance.save()
            
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
        
        try:
            newManager = MyUser.objects.get(username=serializer.validated_data["manager"])
        except:
            raise ValidationError("There is no such user as {}".format(serializer.validated_data["manager"]))
        
        if newManager.isProjectManager:
            raise ValidationError("The chosen user can't become manager. He already is.")
        else:
            name = bleach.clean(serializer.validated_data.get('name'))
            serializer.validated_data['name'] = name

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

        try:
            project = Project.objects.get(name=bleach.clean(self.kwargs['name']))
        except:
            raise ValidationError("There is no project of name {}".format(bleach.clean(self.kwargs['name'])))

        if project.manager != serializer.validated_data["manager"] and not serializer.validated_data["manager"].isProjectManager:
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