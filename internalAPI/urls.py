from django.urls import path

from .views import *

urlpatterns = [
    path('texts/', TextList.as_view()),
    path('texts/<int:pk>/', TextDetail.as_view()),
    path('comments/', CommentList.as_view()),
    path('comments/<int:pk>/', CommentDetail.as_view()),
    path('projects/', ProjectList.as_view()),
    path('projects/<str:name>/', ProjectDetail.as_view()),
]