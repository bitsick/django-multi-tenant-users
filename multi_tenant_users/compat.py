"""Provides support for django-tenat-schemas and django-tenants."""
try:
    from django_tenants.utils import schema_context  # NOQA: F401
except ImportError:
    from tenant_schemas.utils import schema_context  # NOQA: F401
