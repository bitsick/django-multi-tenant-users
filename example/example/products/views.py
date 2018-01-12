from django.shortcuts import get_object_or_404, render

from ..views import tenant_view
from .models import Category, Product


def category_detail(request, pk=None):
    context = {
        'user': request.user,
        'tenant': request.tenant,
        'category': get_object_or_404(Category, pk=pk),
    }
    return render(request, 'products/category_detail.html', context)


def category_list(request):
    context = {
        'user': request.user,
        'tenant': request.tenant,
        'categories': Category.objects.order_by('name'),
    }
    return render(request, 'products/category_list.html', context)


def product_detail(request, pk):
    context = {
        'user': request.user,
        'tenant': request.tenant,
        'product': get_object_or_404(Product, pk=pk),
    }
    return render(request, 'products/product_detail.html', context)


def product_list(request):
    context = {
        'user': request.user,
        'tenant': request.tenant,
        'products': Product.objects.order_by('name'),
    }
    return render(request, 'products/product_list.html', context)
