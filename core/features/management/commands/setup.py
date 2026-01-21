from django.core.management.base import BaseCommand
from accounts.models import Tier
from features.models import Feature, FeaturePermission

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        enterprise, _ = Tier.objects.get_or_create(name="Enterprise")
        pro, _ = Tier.objects.get_or_create(name="Pro")
        free, _ = Tier.objects.get_or_create(name="Free")

        feature_codes = ["project", "task", "user", "billing", "analytics"]

        feature_objs = {}
        for code in feature_codes:
            feature, _ = Feature.objects.get_or_create(
                code=code,
                defaults={"name": code.title()}
            )
            feature_objs[code] = feature

        for feature in feature_objs.values():
            FeaturePermission.objects.update_or_create(
                tier=enterprise,
                feature=feature,
                defaults={
                    "can_create": True,
                    "can_read": True,
                    "can_update": True,
                    "can_delete": True,
                }
            )

        pro_matrix = {
            "project": {
                "can_create": True,
                "can_read": True,
                "can_update": True,
                "can_delete": False,
            },
            "task": {
                "can_create": True,
                "can_read": True,
                "can_update": True,
                "can_delete": False,
            },
            "user": {
                "can_create": False,
                "can_read": True,
                "can_update": False,
                "can_delete": False,
            },
            "billing": {
                "can_create": False,
                "can_read": False,
                "can_update": False,
                "can_delete": False,
            },
            "analytics": {
                "can_create": False,
                "can_read": True,
                "can_update": False,
                "can_delete": False,
            },
        }

        for code, perms in pro_matrix.items():
            FeaturePermission.objects.update_or_create(
                tier=pro,
                feature=feature_objs[code],
                defaults=perms
            )

        free_matrix = {
            "project": {
                "can_create": False,
                "can_read": True,
                "can_update": False,
                "can_delete": False,
            },
            "task": {
                "can_create": False,
                "can_read": False,
                "can_update": False,
                "can_delete": False,
            },
            "user": {
                "can_create": False,
                "can_read": False,
                "can_update": False,
                "can_delete": False,
            },
            "billing": {
                "can_create": False,
                "can_read": False,
                "can_update": False,
                "can_delete": False,
            },
            "analytics": {
                "can_create": False,
                "can_read": False,
                "can_update": False,
                "can_delete": False,
            },
        }

        for code, perms in free_matrix.items():
            FeaturePermission.objects.update_or_create(
                tier=free,
                feature=feature_objs[code],
                defaults=perms
            )

        self.stdout.write("Tiers and permissions created successfully")
