import os
from setuptools import setup



def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='django-multi-tenant-users',
    version='0.1.0',
    license='Apache Software License',

    description='Enables global user accounts in multi-tenant Django environments.',
    long_description=read('README.rst'),

    url='https://github.com/bitsick/django-multi-tenant-users',
    author='Bitsick Productions LLC',
    author_email='contact@bitsick.com',

    packages=['multi_tenant_users'],
    include_package_data=True,
    install_requires=['Django >= 1.11'],

    keywords='django tenants django-tenants django-tenant-schemas',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
