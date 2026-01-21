from django.urls import path
from .views import RegisterAPI, LoginAPI, ProfileAPI
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterAPI.as_view()),
    path("login/", LoginAPI.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("me/", ProfileAPI.as_view()),
]
