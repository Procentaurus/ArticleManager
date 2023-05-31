from django.urls import path

from .views import *

urlpatterns = [
    path('publications/', PublicationList.as_view(), name="publication_list"),
    path('publications/<str:title>/', PublicationDetail.as_view(), name="publication_detail"),
]