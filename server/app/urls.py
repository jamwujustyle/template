from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
from django.contrib import admin
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

url_draft = [
    path("auth/", include("core.urls")),
    path("passkeys/", include("passkeys.urls")),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
]
urlpatterns = [
    path("api/v1/", include(url_draft)),
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
