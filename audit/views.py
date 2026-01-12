from .models import AuditLog
import json
from django.utils.timezone import localtime
from beta_auth.decorators import role_permission_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def log_action(user,model_name, object_id, action, changes):
    AuditLog.objects.create(
        user=user, 
        model_name=model_name, 
        object_id=object_id, 
        action=action, 
        changes=changes
    )

def log_sanitize(log_entry):
    if not log_entry:
        return None

    try:
        user = log_entry.user.email
        model_name = log_entry.model_name
        action = log_entry.action
        object_id = str(log_entry.object_id)
        changes_dict = json.loads(log_entry.changes)
        time = localtime(log_entry.timestamp).strftime('%d-%b-%Y %H:%M').upper()

        changes_list = changes_dict.get(object_id, [])

        if changes_list == action:
            changes_list = []

        return {
            'user': user,
            'model': model_name,
            'action': action,
            'time': time,
            'changes': changes_list
        }
    except Exception as e:
        return None

@login_required
@role_permission_required('view_auditlog')
def audit_logs(request):
    model_names = AuditLog.objects.values_list('model_name', flat=True).distinct()

    logs_by_model = {}

    for name in model_names:
        logs = AuditLog.objects.filter(model_name=name)
        sanitized_logs = [log_sanitize(log) for log in logs]
        page_key = f'{name}_page'
        page_number = request.GET.get(page_key, 1)
        paginator = Paginator(sanitized_logs, 10)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        logs_by_model[name] = page_obj

    return render(request, 'pages/audit/logs.html', {'logs_by_model': logs_by_model})
        