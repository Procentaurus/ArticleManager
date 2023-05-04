from django.urls import path

from .views import *

urlpatterns = [
    path('texts/', TextList.as_view()),
    path('texts/<str:pk>/', TextDetail.as_view()),
    path('comments/', CommentList.as_view()),
    path('comments/<str:pk>/', CommentDetail.as_view()),
    path('projects/', ProjectList.as_view()),
    path('projects/<str:name>/', ProjectDetail.as_view()),
]