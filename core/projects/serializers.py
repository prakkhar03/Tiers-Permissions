from rest_framework import serializers
from .models import Project, ProjectMember

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = Project
        fields = ["id", "name", "owner"]


class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ["id", "project", "user"]
