from rest_framework import mixins, generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Publication
from .serializers import *
from ArticleManager.permissions import ChoseSafeMethod, IsEditor
from ArticleManager.throttlers import PublicationAllRateThrottle, PublicationUserRateThrottle


class PublicationList(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):

    permission_classes = (
        (AllowAny & ChoseSafeMethod) | IsEditor,
    )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.request.user.is_authenticated:
                return PublicationInternalMultiSerializer
            else:
                return PublicationExternalMultiSerializer
        else:
            return PublicationFormSerializer
        
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Publication.objects.filter(isAvailable=True)
        
        if self.request.user.isEditor:
            return Publication.objects.all()
        else:
            return Publication.objects.filter(isAvailable=True)
        
    def get_throttles(self):
        if self.request.method == 'GET':
            throttle_classes = [PublicationUserRateThrottle, PublicationAllRateThrottle]
        else:
            throttle_classes = [PublicationUserRateThrottle]
        return [throttle() for throttle in throttle_classes]
        
    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PublicationDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    lookup_field = 'title'

    permission_classes = (
        (AllowAny & ChoseSafeMethod) | IsEditor,
    )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.request.user.is_authenticated:
                return PublicationInternalSingleSerializer
            else:
                return PublicationExternalSingleSerializer
        else:
            return PublicationFormSerializer
        
    def get_queryset(self):
        return Publication.objects.all()
    
    def get_throttles(self):
        if self.request.method == 'GET':
            throttle_classes = [PublicationUserRateThrottle, PublicationAllRateThrottle]
        else:
            throttle_classes = [PublicationUserRateThrottle]
        return [throttle() for throttle in throttle_classes]
    
    def perform_retrieve(self, instance):
        instance.numberOfDownloads += 1
        instance.save()

        serializer = self.get_serializer(instance)
        return serializer.data
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.perform_retrieve(instance)
        return Response(data)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)