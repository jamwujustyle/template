# server/passkeys/urls.py
from django.urls import path
from .views import PassKeyViewSet

urlpatterns = [
    path(
        "generate-registration-options/",
        PassKeyViewSet.as_view({"get": "generate_registration_options"}),
        name="passkey-generate-registration-options",
    ),
    path(
        "verify-registration/",
        PassKeyViewSet.as_view({"post": "verify_registration"}),
        name="passkey-verify-registration",
    ),
    path(
        "generate-authentication-options/",
        PassKeyViewSet.as_view({"get": "generate_authentication_options"}),
        name="passkey-generate-authentication-options",
    ),
    path(
        "verify-authentication/",
        PassKeyViewSet.as_view({"post": "verify_authentication"}),
        name="passkey-verify-authentication",
    ),
    path(
        "",
        PassKeyViewSet.as_view({"get": "list_passkeys"}),
        name="passkey-list",
    ),
    path(
        "<uuid:pk>/",  # Assuming the primary key for PassKeyCredential is UUID based on models
        PassKeyViewSet.as_view({"delete": "delete_passkey"}),
        name="passkey-delete",
    ),
]
