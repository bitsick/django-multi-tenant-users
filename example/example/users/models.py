from django.db import models
from multi_tenant_users.users import AbstractUserMixin, TenantUser
from tenant_schemas.models import TenantMixin


class Tenant(TenantMixin):
    name = models.CharField(max_length=100)


class User(TenantUser, AbstractUserMixin):
    def __init__(self, *args, **kwargs):
        # is_staff and is_superuser may be provided by some of Django's
        # built-in components when creating objects. They're not valid __init__
        # keyword args for this model because they're not model fields, so they
        # need to be removed.
        kwargs.pop('is_staff', None)
        kwargs.pop('is_superuser', None)
        super(User, self).__init__(*args, **kwargs)

    @property
    def is_staff(self):
        """
        Designates whether the user can log into this tenant's admin site.
        """
        try:
            return self.tenant_permissions.is_staff
        except self.PermissionsModel.DoesNotExist:
            return False

    @is_staff.setter
    def is_staff(self, value):
        try:
            self.tenant_permissions.is_staff = value
            self.tenant_permissions.is_staff.save()
        except self.PermissionsModel.DoesNotExist:
            if self.id:
                permissions = self.PermissionsModel(
                    user_id=self.id,
                    is_staff=value,
                )
                permissions.save()

    def get_short_name(self):
        return self.first_name or self.username
