from django.db import models
from accounts.models import User

class Project(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class ProjectRole(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ("project", "name")


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roles = models.ManyToManyField(ProjectRole)

    class Meta:
        unique_together = ("project", "user")


from features.models import Feature

class ProjectRolePermission(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.ForeignKey(ProjectRole, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)

    can_create = models.BooleanField(default=False)
    can_read = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    class Meta:
        unique_together = ("project", "role", "feature")
