from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Project, ProjectMember, ProjectRole, ProjectRolePermission
from .serializers import ProjectSerializer
from features.utils import has_permission
from features.models import Feature, FeaturePermission
class ProjectCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not has_permission(request.user, "project", "create"):
            return Response({"detail": "Permission denied"}, status=403)

        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project = serializer.save(owner=request.user)

        ProjectMember.objects.get_or_create(
            project=project,
            user=request.user
        )

        return Response(serializer.data, status=201)
class ProjectListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not has_permission(request.user, "project", "read"):
            return Response({"detail": "Permission denied"}, status=403)

        owned = Project.objects.filter(owner=request.user)
        member = Project.objects.filter(projectmember__user=request.user)

        projects = (owned | member).distinct()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
class ProjectUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        if not has_permission(request.user, "project", "update"):
            return Response({"detail": "Permission denied"}, status=403)

        project = Project.objects.get(pk=pk)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
class ProjectDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        if not has_permission(request.user, "project", "delete"):
            return Response({"detail": "Permission denied"}, status=403)

        Project.objects.filter(pk=pk).delete()
        return Response(status=204)
class AddProjectMemberAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        project_id = request.data.get("project_id")
        user_id = request.data.get("user_id")

        project = Project.objects.get(id=project_id)

        if project.owner != request.user:
            return Response(
                {"detail": "Only project owner can add members"},
                status=403
            )

        ProjectMember.objects.get_or_create(
            project_id=project_id,
            user_id=user_id
        )

        return Response({"message": "Member added"})
class ProjectPermissionListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        user = request.user

        project = Project.objects.get(id=project_id)

        member = ProjectMember.objects.filter(
            project=project,
            user=user
        ).first()

        if not member:
            return Response(
                {"detail": "Not a project member"},
                status=403
            )

        data = []

        features = Feature.objects.all()

        admin_role = ProjectRole.objects.get(
            project=project,
            name="admin"
        )

        for feature in features:
            tier_perm = FeaturePermission.objects.filter(
                tier=user.tier,
                feature=feature
            ).first()

            admin_perm = ProjectRolePermission.objects.filter(
                project=project,
                role=admin_role,
                feature=feature
            ).first()

            role_perms = ProjectRolePermission.objects.filter(
                project=project,
                role__in=member.roles.all(),
                feature=feature
            )

            def allowed(action):
                return (
                    tier_perm
                    and getattr(tier_perm, f"can_{action}")
                    and admin_perm
                    and getattr(admin_perm, f"can_{action}")
                    and any(getattr(p, f"can_{action}") for p in role_perms)
                )

            if not role_perms.exists():
                continue

            data.append({
                "feature": feature.code,
                "can_create": allowed("create"),
                "can_read": allowed("read"),
                "can_update": allowed("update"),
                "can_delete": allowed("delete"),
                "roles": list(member.roles.values_list("name", flat=True)),
                "is_owner": project.owner_id == user.id
            })

        return Response(data)
