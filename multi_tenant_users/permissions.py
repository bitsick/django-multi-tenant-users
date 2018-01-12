"""Defines per-tenant authorization functionality."""
from django.conf import settings
from django.contrib.auth.models import Group, Permission, PermissionsMixin
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils import get_permissions_model


class TenantPermissionsMixin(PermissionsMixin):
    """Maps a user instance to per-tenant permissions.

    This class overrides the `groups` and `user_permissions` many-to-many
    fields of the `PermissionsMixin` class to assign more appropriate related
    name values. This also avoids a conflict with
    `django.contrib.auth.models.User`'s reverse accessors.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tenant_permissions',
        related_query_name='tenant_permissions',
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='tenant_permissions_set',
        related_query_name='tenant_permissions',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='tenant_permissions_set',
        related_query_name='tenant_permissions',
    )

    is_anonymous = False

    class Meta:
        abstract = True


class TenantPermissionsDelegator(object):
    """Delegates permission checks to a user's per-tenant permissions.

    This class's API is identical to that of Django's `PermissionMixin`, but
    all implementations delegate functionality to the related permissions
    instance's user instance.
    """
    _PermissionsModel = None

    @property
    def PermissionsModel(self):
        if not self._PermissionsModel:
            self._PermissionsModel = get_permissions_model()
        return self._PermissionsModel

    @property
    def tenant_permissions(self):
        """The tenant-specific permissions object for this user."""
        return self.PermissionsModel.objects.get(user_id=self.id)

    @property
    def is_superuser(self):
        """
        Designates that this user has all permissions without explicitly
        assigning them.
        """
        try:
            return self.tenant_permissions.is_superuser
        except self.PermissionsModel.DoesNotExist:
            return False

    @is_superuser.setter
    def is_superuser(self, value):
        try:
            self.tenant_permissions.is_superuser = value
            self.tenant_permissions.is_superuser.save()
        except self.PermissionsModel.DoesNotExist:
            if self.id:
                permissions = self.PermissionsModel(
                    user_id=self.id,
                    is_superuser=value,
                )
                permissions.save()

    @property
    def groups(self):
        """
        The groups this user belongs to. A user will get all permissions
        granted to each of their groups.
        """
        try:
            return self.tenant_permissions.groups
        except self.PermissionsModel.DoesNotExist:
            return Group.objects.none()

    @groups.setter
    def groups(self, value):
        try:
            self.tenant_permissions.groups = value
            self.tenant_permissions.save()
        except self.PermissionsModel.DoesNotExist:
            if self.id:
                permissions = self.PermissionsModel(
                    user_id=self.id,
                    groups=value,
                )
                permissions.save()

    @property
    def user_permissions(self):
        """Specific permissions for this user."""
        try:
            return self.tenant_permissions.user_permissions
        except self.PermissionsModel.DoesNotExist:
            return Permission.objects.none()

    @user_permissions.setter
    def user_permissions(self, value):
        try:
            self.tenant_permissions.user_permissions = value
            self.tenant_permissions.save()
        except self.PermissionsModel.DoesNotExist:
            if self.id:
                permissions = self.PermissionsModel(
                    user_id=self.id,
                    user_permissions=value,
                )
                permissions.save()

    def get_group_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their
        groups. Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        try:
            return self.tenant_permissions.get_group_permissions(obj=obj)
        except self.PermissionsModel.DoesNotExist:
            return set()

    def get_all_permissions(self, obj=None):
        try:
            return self.tenant_permissions.get_all_permissions(obj=obj)
        except self.PermissionsModel.DoesNotExist:
            return set()

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        try:
            return self.tenant_permissions.has_perm(perm, obj=obj)
        except self.PermissionsModel.DoesNotExist:
            return False

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        try:
            return self.tenant_permissions.has_perms(perm_list, obj=obj)
        except self.PermissionsModel.DoesNotExist:
            return False

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use simlar logic as has_perm(), above.
        """
        try:
            return self.tenant_permissions.has_module_perms(app_label)
        except self.PermissionsModel.DoesNotExist:
            return False
