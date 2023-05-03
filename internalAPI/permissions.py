from rest_framework import permissions

from .models import *

# --------   Position permissions  --------

class IsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True

        return False
    
class IsEditor(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.isEditor:
                return True
            return False
        else:
            return False
    
class IsProjectManager(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.manager:
            return True
        return False


# --------   Methods permissions  --------

class ChoseSafeMethod(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD']:
            return True
        else:
            return False
        
class ChoseDeleteMethod(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return True
        else:
            return False

# --------   Text permissions  --------

class WantToAddTextToOneOfHisProjects(permissions.BasePermission):

    def has_permission(self, request, view):

        project_name = request.data.get('project')
        if not project_name:
            return False
        
        project = Project.objects.get(name=project_name)
        if request.user in project.writers.all():
            return True
        else:
            return False
    

class WantToSeeTextOfHisProject(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user in obj.project.writers.all():
            return True
        else:
            return False
    
class IsManagerOfProjectTextBelongTo(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user == obj.project.manager:
            return True
        else:
            return False


# --------  Comment permissions  --------

class WantToAddCommentToTextInOneOfHisProjects(permissions.BasePermission):

    def has_permission(self, request, view):

        text_id = request.data.get('text')

        if not text_id:
            return False

        text = Text.objects.get(id=text_id)
        project = text.project
        
        if request.user in project.writers.all():
            return True
        else:
            return False
    

class WantToSeeCommentOfHisProject(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user in obj.text.project.writers.all():
            return True
        else:
            return False
    
class IsManagerOfProjectCommentBelongTo(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.text.project.manager:
            return True
        else:
            return False


# --------  Project permissions  --------

class WantToSeeHisProject(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user in obj.writers.all():
            return True
        else:
            return False

