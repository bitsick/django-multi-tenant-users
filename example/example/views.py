from django.shortcuts import redirect, render
from functools import wraps


def tenant_view(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        can_view = (
            request.user.is_authenticated and
            request.tenant in request.user.tenants.all()
        )
        if can_view:
            return func(request, *args, **kwargs)
        else:
            return redirect('http://local.bitsick.com:8000')
    return inner


def index(request):
    context = { 'user': request.user }
    return render(request, 'index.html', context)


@tenant_view
def tenant(request):
    context = { 'user': request.user, 'tenant': request.tenant }
    return render(request, 'tenant.html', context)
