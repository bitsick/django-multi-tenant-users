"""Defines utility functions for multi-tenant user environments."""
from django.apps import apps
from django.conf import settings
from django.db import transaction

from .compat import schema_context


@transaction.atomic
def add_user(user=None, tenant=None, **kwargs):
    user.tenants.add(tenant)
    with schema_context(tenant.schema_name):
        try:
            PermissionsModel = get_permissions_model()
            permissions = PermissionsModel.objects.get(user_id=user.id)
        except PermissionsModel.DoesNotExist:
            permissions = PermissionsModel(user=user, **kwargs)
            permissions.save()


def get_permissions_model():
    try:
        model_name = settings.MULTI_TENANT_USERS_PERMISSIONS_MODEL
        return apps.get_model(model_name, require_ready=False)
    except AttributeError:
        raise ImproperlyConfigured(
            _('MULTI_TENANT_USERS_PERMISSIONS_MODEL '
              'must be defined in settings.')
        )
    except LookupError:
        raise ImproperlyConfigured(
            _('Failed to import the model specified in '
              'settings.MULTI_TENANT_USERS_PERMISSIONS_MODEL.')
        )


@transaction.atomic
def remove_user(user=None, tenant=None):
    user.tenants.remove(tenant)
    with schema_context(tenant.schema_name):
        PermissionsModel = get_permissions_model()
        permissions = PermissionsModel.objects.filter(user_id=user.id).first()
        if permissions:
            permissions.delete()
