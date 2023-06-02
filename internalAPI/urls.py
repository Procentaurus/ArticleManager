from django.urls import path

from .views import *

urlpatterns = [
    path('texts/', TextList.as_view(), name='text_list'),
    path('texts/<str:pk>/', TextDetail.as_view(), name='text_detail'),
    path('comments/', CommentList.as_view(), name='comment_list'),
    path('comments/<str:pk>/', CommentDetail.as_view(), name="comment_detail"),
    path('projects/', ProjectList.as_view(), name='project_list'),
    path('projects/<str:name>/', ProjectDetail.as_view(), name='project_detail'),
]