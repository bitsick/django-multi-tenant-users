=========================
django-multi-tenant-users
=========================

django-multi-tenant-users is a Django app that enables global user accounts
with per-tenant permissions in multi-tenant environments. It is based on
`django-tenant-users <https://github.com/Corvia/django-tenant-users>`_ but aims
to make fewer assumptions and offer more flexibility.

**NOTE:** This is pre-alpha software. Use with caution.

Table of Contents
=================

1. `Overview <overview_>`_
2. `Getting Started <getting_started_>`_
    1. `Prerequisites <prerequisites_>`_
    2. `Installation <installation_>`_
3. `Usage <usage_>`_
    1. `Basic <usage_basic_>`_
    2. `With ModelBackend and Django's Admin <usage_extended_>`_
4. `API <api_>`_
5. `Examples <examples_>`_
6. `Contributing <contributing_>`_
7. `Versioning <versioning_>`_
8. `License <license_>`_

.. _overview:

Overview
========

Django's built-in ``django.contrib.auth`` package provides a user
authentication and authorization framework backed by the ``User``, ``Group``,
and ``Permission`` models. In a typical Django project using either
`django-tenants <https://github.com/tomturner/django-tenants>`_ or
`django-tenant-schemas <https://github.com/bernardopires/django-tenant-schemas>`_,
``django.contrib.auth`` can either be installed in ``SHARED_APPS``—meaning
users authenticate and have permissions set in the public schema that apply to
all tenants—or ``TENANT_APPS``, meaning users log in to and have permissions
set by each individual tenant.

By decoupling user authentication and authorization,
``django-multi-tenant-users`` enables global user accounts stored in the public
schema to access tenants according to the permissions set in each tenant's
schema. Compatibility with Django's built-in auth mechanisms is retained by
delegating model fields and methods to related objects in the public and tenant
schemas as appropriate.

.. _getting_started:

Getting Started
===============

.. _prerequisites:

Prerequisites
-------------

``django-multi-tenant-users`` is compatible with Django 1.11 and above. As with
Django 1.11, Python 2.7 and Python 3.4+ are supported. It is assumed that this
app will be used alongside either
`django-tenants <https://github.com/tomturner/django-tenants>`_ or
`django-tenant-schemas <https://github.com/bernardopires/django-tenant-schemas>`_.

.. _installation:

Installation
------------

``django-multi-tenant-users`` is not yet available on PyPI, but may still be
installed from GitHub until a packages is available.

.. code-block:: bash

    $ pip install git+git://github.com/bitsick/django-multi-tenant-users

.. _usage:

Usage
=====

At its core, ``django-multi-tenant-users`` simply provides a means of
separating authentication and authorization. Because it's not possible to
predict how all developers will use this package, including how or even if
they use certain model fields and methods, the default behavior is quite
minimal.

If a project has its own authentication system and doesn't rely on Django's
admin interface, the ``django-multi-tenant-users`` base models can easily be
inherited from to add multi-tenant user functionality.

If a project is using Django's ``ModelBackend`` for auth and makes use of
Django's admin interface, ``django-multi-tenant-users`` provides some additional
classes to achieve compatibility. Both scenarios are outlined below. Users
may find that they need something in between, and that will work too.

.. _usage_basic:

Basic
-----

Begin by creating a user model. This will be analogous to
``django.contrib.auth.models.User``. At a minimum, the user model must inherit
from ``multi_tenant_uesrs.users.TenantUser``. This will ensure the user model
implements the functionality Django expects, whether by virtue of inheriting
from ``django.contrib.auth.base_user.AbstractBaseUser`` or by delegating
functionality.

Because the model must be installed in ``SHARED_APPS`` and is directly related
to the tenant model, defining the user model alongside the tenant model is
recommended. For example:

.. code-block:: python

  # myproject/users/models.py

  from django.db import models
  from multi_tenant_users.users import TenantUser
  from tenant_schemas.models import TenantMixin


  class Tenant(TenantMixin):
      name = models.CharField(max_length=100)


  class User(TenantUser):
      pass

Next, create a tenant permissions model. This model will be be assigned
permissions and group memberships within tenants and as such must be
installed in ``TENANT_APPS``. It must inherit from
``multi_tenant_users.permissions.TenantPermissionsMixin`` to implement the
authorization functionality Django expects. For example:

.. code-block:: python

  # myproject/permissions/models.py

  from multi_tenant_users.permissions import TenantPermissionsMixin


  class TenantPermissions(TenantPermissionsMixin):
      pass

Finally, update the project's settings to install the user and permissions
models and tell ``django-multi-tenant-users`` which models to use.

.. code-block:: python

  # myproject/settings.py

  SHARED_APPS = (
      'tenant_schemas',  # or django_tenants
      'myproject.users',  # or wherever the user model is defined

      'django.contrib.contenttypes',
      'django.contrib.auth',
      # ...
  )

  TENANT_APPS = (
      'django.contrib.contenttypes',
      'django.contrib.auth',

      'myproject.permissions',  # or wherever the permissions model is defined
      # ...
  )

  INSTALLED_APPS = (
      'tenant_schemas',
      'myproject.users',

      'django.contrib.contenttypes',
      'django.contrib.auth',

      'myproject.permissions',
      # ...
  )

  # Set this to the user model defined earlier. This tells Django to use the
  # custom model instead of django.contrib.auth.models.User.
  AUTH_USER_MODEL = 'users.User'

  # Set this to the permissions model defined earlier. This tells
  # ``django-multi-tenant-users`` where to get users' per-tenant permissions.
  MULTI_TENANT_USERS_PERMISSIONS_MODEL = 'permissions.TenantPermissions'

.. _usage_extended:

With ``ModelBackend`` and Django's Admin
----------------------------------------

For compatibility with Django's ``ModelBackend``, the user model must have an
``is_active`` field. To access Django's admin interface, the user model must
have an ``is_staff`` field set to ``True``, but this should of course be
stored on a per-tenant basis. Finally, to check what permissions a user has
from group memberships, ``ModelBackend`` needs to check the tenant permissions
object's membership instead of the user object's membership.

To add the necessary fields and store them in the correct location:

1. Add ``is_staff`` to the tenant permissions model
2. Add ``is_active`` to the user model
3. Delegate ``is_staff`` on the user model to the tenant permissions model
4. Delegate ``is_active`` on the tenant permissions model to the user model
5. Replace ``ModelBackend`` with an implementation that's aware of the
   tenant permission model

Fortunately, this only requires a few additional lines of codes on the models
and the use of some additional classes provided by
``django-multi-tenant-users``.

Begin by adjusting the user model. The simplest means of adding the fields
Django's admin interface expects is to inherit from
``multi_tenant_users.useres.AbstractUserMixin``. The ``is_staff`` delegators
can be copied from below, as can the additional ``__init__`` and
``get_short_name`` methods.

.. code-block:: python

  # myproject/users/models.py

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
          # The AbstractUserMixin implementation is hidden by the
          # TenantUser class, so this must be re-added here.
          return self.first_name or self.username

Next, adjust the tenant permissions model. Add the ``is_staff`` field
and ``is_active`` delegators as shown below:

.. code-block:: python

  # myproject/permissions/models.py

  from django.db import models
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

Finally, update the project's settings to use the modified
``ModelBackend`` provided by ``django-multi-tenant-users``:

.. code-block:: python

  # myproject/settings.py

  AUTHENTICATION_BACKENDS = ['multi_tenant_users.backends.ModelBackend']

.. _api:

API
===

Full API documentation is not yet available. Please see the docstrings
in the package source for documentation in the meantime.

Examples
========
See the `example <./example>`_ directory for a complete working example,
including compatibility with Django's admin interface.

Contributing
============
See `CONTRIBUTING.md <./CONTRIBUTING.md>`_ for details on making contributions.

.. _versioning:

Versioning
==========

This repository uses
`GitFlow <http://datasift.github.io/gitflow/IntroducingGitFlow.html>`_
and `semantic versioning <https://semver.org/>`_. See the [tags](./tags) in
the `master` branch for the available versions.

.. _license:

License
=======

Apache License 2.0
