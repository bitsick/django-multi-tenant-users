from django.db import models
from django.utils.translation import gettext_lazy as _
from multi_tenant_users.permissions import TenantPermissionsMixin


class TenantPermissions(TenantPermissionsMixin):
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_("Designates whether the user "
                    "can log into this tenant's admin site."),
    )

    @property
    def is_active(self):
        """
        Designates whether this user should be treated as active.
        """
        return self.user.is_active

    @is_active.setter
    def is_active(self, value):
        self.user.is_active = value
        self.user.is_active.save()
