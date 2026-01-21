from django.db import models
from accounts.models import User, Tier

class Feature(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

class FeaturePermission(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    can_create = models.BooleanField(default=False)
    can_read = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(tier__isnull=False, user__isnull=True) |
                    models.Q(tier__isnull=True, user__isnull=False)
                ),
                name="tier_or_user_only"
            )
        ]
