from rest_framework import permissions, generics
from rest_framework.response import Response

from knox.models import AuthToken

from .serializers import RegisterSerializer, MyUserSerializer, LoginSerializer
from ArticleManager.throttlers import LoginRateThrottle


class RegisterView(generics.CreateAPIView):
    # Create user API view
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    throttle_classes = (LoginRateThrottle,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        return Response({
            "token": AuthToken.objects.create(user)[1]
        })