from django.urls import path
from .views import *

urlpatterns = [
    path("check/", PermissionListAPI.as_view()),
]
