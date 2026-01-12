from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import quote

def role_permission_required(permission_codename):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.is_superuser or user.role.filter(permissions__codename=permission_codename).exists():
                return view_func(request, *args, **kwargs)
            
            message = f'You do not have permission to {permission_codename.replace("_", " ").title()}'
            encoded_message = quote(message)
            return redirect(reverse('access_denied', args=(encoded_message,)))
        return _wrapped_view
    return decorator
