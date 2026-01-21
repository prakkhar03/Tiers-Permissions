from features.models import Feature, FeaturePermission
from .models import ProjectMember, ProjectRole, ProjectRolePermission

def has_project_permission(user, project, feature_code, action):
    if action not in ["create", "read", "update", "delete"]:
        return False

    try:
        feature = Feature.objects.get(code=feature_code)
    except Feature.DoesNotExist:
        return False

    member = ProjectMember.objects.filter(
        project=project,
        user=user
    ).first()

    if not member:
        return False

    tier_perm = FeaturePermission.objects.filter(
        tier=user.tier,
        feature=feature
    ).first()

    if not tier_perm or not getattr(tier_perm, f"can_{action}"):
        return False

    admin_role = ProjectRole.objects.get(project=project, name="admin")

    admin_perm = ProjectRolePermission.objects.filter(
        project=project,
        role=admin_role,
        feature=feature
    ).first()

    if not admin_perm or not getattr(admin_perm, f"can_{action}"):
        return False

    role_perms = ProjectRolePermission.objects.filter(
        project=project,
        role__in=member.roles.all(),
        feature=feature
    )

    return any(getattr(p, f"can_{action}") for p in role_perms)
