from django.contrib.auth import backends
from django.contrib.auth.models import Permission

from .utils import get_permissions_model


class ModelBackend(backends.ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.

    This class overrides `_get_group_permissions` to find permissions based on
    the user's per-tenant `settings.MULTI_TENANT_USERS_PERMISSIONS_MODEL`
    instance's group memberships instead of the user's direct group
    memberhsips.
    """
    def _get_group_permissions(self, user_obj):
        """
        Returns a set of permission strings the user `user_obj` has from the
        groups they belong to through their
        `settings.MULTI_TENANT_USERS_PERMISSIONS_MODEL` instance.
        """
        PermissionsModel = get_permissions_model()
        groups_field = PermissionsModel._meta.get_field('groups')
        groups_query = 'group__%s' % groups_field.related_query_name()
        return Permission.objects.filter(**{groups_query: user_obj})
