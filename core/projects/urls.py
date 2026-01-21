from django.urls import path
from .views import (
    ProjectCreateAPI,
    ProjectListAPI,
    ProjectUpdateAPI,
    ProjectDeleteAPI,
    AddProjectMemberAPI,
    ProjectPermissionListAPI,
)

urlpatterns = [
    path("create/", ProjectCreateAPI.as_view()),
    path("list/", ProjectListAPI.as_view()),
    path("update/<int:pk>/", ProjectUpdateAPI.as_view()),
    path("delete/<int:pk>/", ProjectDeleteAPI.as_view()),
    path("add-member/", AddProjectMemberAPI.as_view()),
    path("<int:project_id>/permissions/", ProjectPermissionListAPI.as_view()),

]
