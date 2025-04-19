from django.urls import path
from .views import UserRegister, UserLogin, UserProfile, UserRecover, UserRecoverConfirm

urlpatterns = [
    path("register", UserRegister.as_view(), name="register"),
    path("login", UserLogin.as_view(), name="login"),
    path("profile", UserProfile.as_view(), name="profile"),
    path("recover", UserRecover.as_view(), name="recover"),
    path("recover-confirm", UserRecoverConfirm.as_view(), name="recover-confirm"),
]
