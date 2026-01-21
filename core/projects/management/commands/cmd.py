from django.core.management.base import BaseCommand
from django.db import transaction

from projects.models import Project, ProjectMember, ProjectRole, ProjectRolePermission
from features.models import Feature


class Command(BaseCommand):
    help = "Backfill project roles and assign member role to existing members"

    def handle(self, *args, **options):
        with transaction.atomic():
            features = Feature.objects.all()

            for project in Project.objects.all():
                admin_role, _ = ProjectRole.objects.get_or_create(
                    project=project,
                    name="admin"
                )

                member_role, _ = ProjectRole.objects.get_or_create(
                    project=project,
                    name="member"
                )

                owner_member, _ = ProjectMember.objects.get_or_create(
                    project=project,
                    user=project.owner
                )
                owner_member.roles.add(admin_role)

                for member in ProjectMember.objects.filter(project=project):
                    if member.user_id != project.owner_id:
                        member.roles.add(member_role)

                for feature in features:
                    ProjectRolePermission.objects.get_or_create(
                        project=project,
                        role=admin_role,
                        feature=feature,
                        defaults={
                            "can_create": True,
                            "can_read": True,
                            "can_update": True,
                            "can_delete": True
                        }
                    )

                    ProjectRolePermission.objects.get_or_create(
                        project=project,
                        role=member_role,
                        feature=feature,
                        defaults={
                            "can_create": False,
                            "can_read": True,
                            "can_update": False,
                            "can_delete": False
                        }
                    )

        self.stdout.write(self.style.SUCCESS("Existing members assigned member role successfully"))
