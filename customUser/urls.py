from django.urls import path

from knox import views as knox_views

from .views import *

urlpatterns = [
    path('create/', RegisterView.as_view(), name="create"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
]