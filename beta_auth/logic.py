from django.contrib.auth.models import Permission
from django.shortcuts import render
from urllib.parse import unquote
from django.contrib.auth.decorators import login_required
from django.apps import apps
from .models import Role
import json
from audit.views import log_action
from django.http import HttpResponse

def access_denied(request, message):
    decoded_message = unquote(message)
    return render(request, 'pages/cr_auth/access_denied.html', {'message': decoded_message})

def get_perm_code_names(model):
    return list(
        Permission.objects.filter(content_type__model=model).values_list('codename', flat=True)
    )

def permission_list():
    app_names = ['beta_auth']

    model_perms = dict()

    for app_name in app_names:
        try:
            app_config = apps.get_app_config(app_name)
        except LookupError:
            continue

        model_names = [
            model.__name__.lower()
            for model in app_config.get_models()
            if not getattr(model, 'is_hidden', False)
        ]
        for model_name in model_names:
            perms = Permission.objects.filter(content_type__model=model_name)
            if app_name == 'audit' and model_name == 'auditlog':
                perms = perms.filter(codename='view_auditlog')
            model_perms[model_name] = perms
      
    return model_perms

@login_required
def model_permissions_settings(request, role_id):
    if request.method == 'POST':
        permission_id = request.POST.get('permission_id')
        action = request.POST.get('action')
        try:
            role = Role.objects.get(id=role_id)
            permission = Permission.objects.get(id=permission_id)
           
            if action == 'add':
                role.permissions.add(permission)
                changes_str = json.dumps({
                    str(role.id): f"Added permission {permission.codename}"
                })
                log_action(request.user, 'Roles', role.id, f"Added permission {permission.codename}", changes_str)
                
            elif action == 'remove':
                role.permissions.remove(permission)
                changes_str = json.dumps({
                    str(role.id): f"Removed permission {permission.codename}"
                })
                log_action(request.user, 'Roles', role.id, f"Removed permission {permission.codename}", changes_str)
        
        except (Role.DoesNotExist, Permission.DoesNotExist):
            pass
        finally:
              return HttpResponse('')
