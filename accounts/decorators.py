from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*roles):
    """Decorator to restrict view access to specific roles."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.rol not in roles:
                messages.error(request, 'No tiene permisos para acceder a esta sección.')
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
