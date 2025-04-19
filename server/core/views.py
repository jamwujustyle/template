from rest_framework import status, viewsets, mixins, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model

from utils.exception_handler import ErrorHandlingMixin

from .serializers import UserSerializer, LoginSerializer
from logging_config import logger


class UserRegister(ErrorHandlingMixin, generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return get_user_model().objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        token_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response(token_data, status=status.HTTP_201_CREATED)


class UserLogin(ErrorHandlingMixin, APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        token_data = {"refresh": str(refresh), "access": str(refresh.access_token)}
        return Response(token_data, status=status.HTTP_200_OK)
