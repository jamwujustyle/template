from django.contrib import admin
from django.urls import path, include

url_draft = [
    path("", include("core.urls")),
]
urlpatterns = [
    path("api/v1/", include(url_draft)),
    path("admin/", admin.site.urls),
]
