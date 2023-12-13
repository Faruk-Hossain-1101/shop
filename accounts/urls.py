from django.urls import path

from .views import RegisterView, LoginView, UserVerification

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("verify/", UserVerification.as_view(), name="verify"),
]