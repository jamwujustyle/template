from django.urls import path
from .views import Mock

urlpatterns = [
    path("data", Mock.as_view(), name="mock"),
]
