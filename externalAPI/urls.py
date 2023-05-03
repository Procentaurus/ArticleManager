from django.urls import path

from .views import *

urlpatterns = [
    path('publications/', PublicationList.as_view()),
    path('publications/<str:title>/', PublicationDetail.as_view()),
]