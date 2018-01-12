"""example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from .products import views as products_views
from . import views


urlpatterns = [
    url(
        r'^login',
        auth_views.login,
        {'template_name': 'login.html'},
        name='login',
    ),
    url(
        r'^logout',
        auth_views.logout,
        {'next_page': '/'},
        name='logout',
    ),
    url(r'^admin/', admin.site.urls),
    url(
        r'^categories/(?P<pk>[0-9]+)',
        products_views.category_detail,
        name='category_detail',
    ),
    url(
        r'^categories',
        products_views.category_list,
        name='category_list',
    ),
    url(
        r'^products/(?P<pk>[0-9]+)',
        products_views.product_detail,
        name='product_detail',
    ),
    url(
        r'^products',
        products_views.product_list,
        name='product_list',
    ),
    url(r'^$', views.index, name='index'),
]
