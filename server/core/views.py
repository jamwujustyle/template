from rest_framework import status, generics, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView


from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

from utils.exception_handler import ErrorHandlingMixin

from .serializers import (
    UserSerializer,
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
)
from logging_config import logger

from drf_spectacular.utils import extend_schema


@extend_schema(tags=["auth"])
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


@extend_schema(tags=["auth"])
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


@extend_schema(tags=["auth"])
class UserProfile(ErrorHandlingMixin, generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(tags=["auth"])
class UserRecover(ErrorHandlingMixin, APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        email = request.data.get("email")
        user = get_user_model().objects.filter(email=email).first()
        logger.critical(f"email passed: {email}, user found: {user}")
        if not user:
            return Response(
                {"email": "User not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        reset_link = f"http://localhost:3000/reset-password?token={token}"
        # TODO: DEFINE DEFAULT_FROM_EMAIL
        send_mail(
            "Reset your password",
            f"Click the link to reset your password: {reset_link}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return Response({"msg": "Password reset email sent"})


@extend_schema(tags=["auth"])
class UserRecoverConfirm(ErrorHandlingMixin, APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        # TODO: EXTRACT TOKEN FROM HEADERS
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "password reset successful"})


# TODO: DISTINGUISH BETWEEN RECOVERING AND LOGIN JWTS
