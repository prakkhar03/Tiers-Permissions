from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Feature, FeaturePermission
class PermissionListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = []

        features = Feature.objects.all()

        for feature in features:
            user_perm = FeaturePermission.objects.filter(
                user=user,
                feature=feature
            ).first()

            if user_perm:
                perm = user_perm
                source = "user"
            else:
                perm = FeaturePermission.objects.filter(
                    tier=user.tier,
                    feature=feature
                ).first()
                source = "tier"

            if not perm:
                continue

            data.append({
                "feature": feature.code,
                "can_create": perm.can_create,
                "can_read": perm.can_read,
                "can_update": perm.can_update,
                "can_delete": perm.can_delete,
                "source": source
            })

        return Response(data)
