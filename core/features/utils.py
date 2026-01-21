from features.models import Feature, FeaturePermission

def has_permission(user, feature_code, action):
    if not user.is_authenticated:
        return False

    if action not in ["create", "read", "update", "delete"]:
        return False

    try:
        feature = Feature.objects.get(code=feature_code)
    except Feature.DoesNotExist:
        return False

    user_perm = FeaturePermission.objects.filter(
        user=user,
        feature=feature
    ).first()

    if user_perm:
        return getattr(user_perm, f"can_{action}", False)

    if not user.tier:
        return False

    tier_perm = FeaturePermission.objects.filter(
        tier=user.tier,
        feature=feature
    ).first()

    if not tier_perm:
        return False

    return getattr(tier_perm, f"can_{action}", False)
