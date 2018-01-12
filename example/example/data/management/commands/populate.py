from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand
from multi_tenant_users.utils import add_user
from tenant_schemas.utils import schema_context

from example.products.models import Category, Product
from example.users.models import Tenant, User


class Command(BaseCommand):
    COMMAND_NAME = 'populate'

    help = 'Populate the database with example data.'

    def handle(self, *args, **options):
        # Create tenants
        public = Tenant.objects.get_or_create(
            name='Public Tenant',
            domain_url='local.bitsick.com',
            schema_name='public',
        )[0]
        globochem = Tenant.objects.get_or_create(
            name='GloboChem',
            domain_url='globochem.local.bitsick.com',
            schema_name='globochem',
        )[0]
        initech = Tenant.objects.get_or_create(
            name='Initech',
            domain_url='initech.local.bitsick.com',
            schema_name='initech',
        )[0]

        # Create users
        try:
            admin = User.objects.get(username='admin')
        except User.DoesNotExist:
            admin = User.objects.create_user(
                'admin',
                'admin@example.com',
                'Password!',
            )

        try:
            bill = User.objects.get(username='bill')
        except User.DoesNotExist:
            bill = User.objects.create_user(
                'bill',
                'bill@example.com',
                'Password!',
            )

        try:
            bob = User.objects.get(username='bob')
        except User.DoesNotExist:
            bob = User.objects.create_user(
                'bob',
                'bob@example.com',
                'Password!',
            )

        try:
            david = User.objects.get(username='david')
        except User.DoesNotExist:
            david = User.objects.create_user(
                'david',
                'david@example.com',
                'Password!',
            )

        try:
            michael = User.objects.get(username='michael')
        except User.DoesNotExist:
            michael = User.objects.create_user(
                'michael',
                'michael@example.com',
                'Password!',
            )

        try:
            peter = User.objects.get(username='peter')
        except User.DoesNotExist:
            peter = User.objects.create_user(
                'peter',
                'peter@example.com',
                'Password!',
            )

        try:
            samir = User.objects.get(username='samir')
        except User.DoesNotExist:
            samir = User.objects.create_user(
                'samir',
                'samir@example.com',
                'Password!',
            )

        # Add users to tenants
        add_user(admin, public, is_superuser=True, is_staff=True)
        add_user(admin, globochem, is_superuser=True, is_staff=True)
        add_user(admin, initech, is_superuser=True, is_staff=True)
        add_user(bill, initech, is_superuser=True, is_staff=True)
        add_user(bob, globochem, is_staff=True)
        add_user(david, globochem, is_staff=True)
        add_user(michael, globochem)
        add_user(michael, initech)
        add_user(peter, initech, is_staff=True)
        add_user(samir, globochem)
        add_user(samir, initech)

        # Add user permissions and product data
        with schema_context(globochem.schema_name):
            add_category = Permission.objects.get(codename='add_category')
            change_category = Permission.objects.get(codename='change_category')
            delete_category = Permission.objects.get(codename='delete_category')
            add_product = Permission.objects.get(codename='add_product')
            change_product = Permission.objects.get(codename='change_product')
            delete_product = Permission.objects.get(codename='delete_product')

            bob.tenant_permissions.user_permissions.add(*[
                add_category,
                change_category,
                delete_category,
                add_product,
                change_product,
                delete_product,
            ])
            david.tenant_permissions.user_permissions.add(*[
                add_category,
                change_category,
                delete_category,
                add_product,
                change_product,
                delete_product,
            ])

            consumer = Category.objects.get_or_create(name='Consumer')[0]
            food = Category.objects.get_or_create(name='Food')[0]
            corporate = Category.objects.get_or_create(name='Corporate')[0]

            bag_hutch = Product.objects.get_or_create(
                name='Bag Hutch',
                price=19.99,
            )[0]
            bag_hutch.categories.add(consumer)

            burger = Product.objects.get_or_create(
                name='Ding Dong Burger',
                price=3.99,
            )[0]
            burger.categories.add(food)

            biscuit = Product.objects.get_or_create(
                name="Gramma Betsy's Biscuit Powder",
                price=5.99,
            )[0]
            biscuit.categories.add(food)

            techcorp = Product.objects.get_or_create(
                name='TECHCORP Consulting',
                price=1499000,
            )[0]
            techcorp.categories.add(corporate)

            pitpat = Product.objects.get_or_create(
                name='Pit-Pat Brand Sponsorship',
                price=299999
            )[0]
            pitpat.categories.add(corporate)

        with schema_context(initech.schema_name):
            add_category = Permission.objects.get(codename='add_category')
            change_category = Permission.objects.get(codename='change_category')
            delete_category = Permission.objects.get(codename='delete_category')
            add_product = Permission.objects.get(codename='add_product')
            change_product = Permission.objects.get(codename='change_product')
            delete_product = Permission.objects.get(codename='delete_product')

            peter.tenant_permissions.user_permissions.add(*[
                add_product,
                change_product,
                delete_product,
            ])

            hardware = Category.objects.get_or_create(name='Hardware')[0]
            software = Category.objects.get_or_create(name='Software')[0]
            services = Category.objects.get_or_create(name='Services')[0]

            swingline = Product.objects.get_or_create(
                name='Red Swingline Stapler',
                price=11.39,
            )[0]
            swingline.categories.add(hardware)

            tetris = Product.objects.get_or_create(
                name='Tetris',
                price=0.99,
            )[0]
            tetris.categories.add(software)

            virus = Product.objects.get_or_create(
                name='A virus that could rip this place off big time',
                price=305326.13,
            )[0]
            virus.categories.add(software)

            y2k = Product.objects.get_or_create(
                name='Y2K Readiness Consulting',
                price=499999.99,
            )[0]
            y2k.categories.add(services)

        saas = Category.objects.get_or_create(name='SaaS Platform')[0]

        basic = Product.objects.get_or_create(
            name='Basic Plan',
            price=5,
        )[0]
        basic.categories.add(saas)

        standard = Product.objects.get_or_create(
            name='Standard Plan',
            price=10,
        )[0]
        standard.categories.add(saas)

        premium = Product.objects.get_or_create(
            name='Premium Plan',
            price=25,
        )[0]
        premium.categories.add(saas)
