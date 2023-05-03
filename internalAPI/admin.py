from django.contrib import admin

from .models import *

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'isFinished', 'startDate')
    list_filter = ('manager', 'isFinished')

class TextAdmin(admin.ModelAdmin):
    list_display = ('author', 'creationDate', 'project', 'lastModified')
    list_filter = ('author', 'creationDate', 'project')
    search_fields = ('author', 'creationDate', 'body', 'project')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'creationDate')
    list_filter = ('author', 'creationDate')
    search_fields = ('author', 'creationDate', 'body')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(Comment, CommentAdmin)
