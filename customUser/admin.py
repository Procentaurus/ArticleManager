from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import *
from .forms import *

# class MyUserAdmin(UserAdmin):

#     add_form = MyUserCreationForm
#     form = MyUserChangeForm
#     model = MyUser

#     list_display  =('email', 'username', 'creationDate', 'lastLogin', 'is_admin')
#     search_fields = ('email', 'username','is_admin')
#     readonly_fields = ('id', 'creationDate', 'lastLogin','username')

#     ordering = ('email',)

class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser
    list_display = ("email", "username", "isProjectManager", "isEditor")
    list_filter = ("email", "username", "isProjectManager")
    readonly_fields = ("email", "username", "lastLogin", "creationDate")
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Permissions", {"fields": ("creationDate","lastLogin","isEditor","isProjectManager", "is_active")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "username", "password1", "password2",
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    
admin.site.register(MyUser, MyUserAdmin)
admin.site.unregister(Group)