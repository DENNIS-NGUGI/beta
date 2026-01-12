from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Role, DefaultPassword, ForgotPassword
from .forms import UserForm, RoleForm, DefaultPasswordForm, LoginForm, ChangePasswordForm, ForgotPasswordForm, RecoverPasswordForm
from audit.views import log_action, log_sanitize
from audit.models import AuditLog
import json
from django.db.models import Q
from django.db import transaction
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from .logic import permission_list
from .decorators import role_permission_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from smtplib import SMTPException
from django.conf import settings
import os


@login_required
@role_permission_required('view_user')
def user_list(request):
    users = User.objects.exclude(Q(is_superuser=True) & Q(is_staff=True))
    admin_roles = ['Administator']
    user_is_admin = request.user.is_superuser or request.user.role.filter(name__in=admin_roles).exists()
    if not user_is_admin:
        users = [request.user]
    return render(request, 'beta_auth/user_list.html', {'users': users, 'user_is_admin':user_is_admin})

@login_required
@role_permission_required('add_user')
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        role, _ = Role.objects.get_or_create(
            name='Staff',
            defaults={'description': 'Staff Roles'}
        )
        password_obj = DefaultPassword.objects.filter(is_active=True).first()
        if password_obj:            
            password = password_obj.password
        else:
            next_url = request.get_full_path()
            messages.error(request, 'Create a default password first.')
            return redirect(f"{reverse('add_password')}?next={next_url}")
        if form.is_valid():
            with transaction.atomic():
                obj = form.save(commit=False)
                obj.set_password(password)
                obj.save(request=request)
                form.save_m2m()
                if not obj.role.filter(name='Staff').exists():
                    obj.role.add(role)
                changes_str = json.dumps({
                    str(obj.id): f"Added user {obj.email}"
                })
                file_path = os.path.join(settings.BASE_DIR, 'users_file.txt')
                with open(file_path, 'a') as users_file:
                    users_file.write(f'Email: {obj.email}, Password: {password}' + '\n')
                log_action(request.user, 'Users', obj.id, f"Added user {obj.email}", changes_str)
                messages.success(request, "User added successfully!")
                return redirect('user_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserForm()

    return render(request, 'beta_auth/user_form.html', {'form': form})

@login_required
@role_permission_required('change_user')
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    logs_objects = AuditLog.objects.filter(object_id=user.id,model_name='Users')
    logs = []
    for log in logs_objects:
        logs.append(log_sanitize(log))
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            changes = []
            original_user = get_object_or_404(User, id=user_id)

            for field in form.changed_data:
                if field == 'role':
                    old_value = ', '.join(original_user.role.values_list('name', flat=True))
                    new_value = ', '.join(form.cleaned_data['role'].values_list('name', flat=True))
                else:
                    old_value = getattr(original_user, field, '')
                    new_value = form.cleaned_data[field]

                changes.append(f'{field.upper()}: {old_value} -> {new_value}')
                
            if changes:
                changes_str = json.dumps({user_id: changes})
                log_action(request.user, 'Users', user.id, f"Edited user {user.email}", changes_str)
                form.save()
                messages.success(request, "User updated successfully!")
                return redirect('user_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserForm(instance=user)

    return render(request, 'beta_auth/user_form.html', {'form': form, 'logs': logs})

@login_required
@role_permission_required('delete_user')
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.deleted = True
    user.save()
    changes_str = json.dumps({
        str(user_id): f"Deleted user {user.email}"
    })
    log_action(request.user, 'Users', user.id,f"Deleted user {user.email}", changes_str)
    messages.success(request, "User deleted successfully!")
    return redirect('user_list')


@login_required
@role_permission_required('view_role')
def role_list(request):
    roles = Role.objects.exclude(deleted=True).order_by('-created_at')
    return render(request, 'beta_auth/role_list.html', {'roles': roles})

@login_required
@role_permission_required('add_role')
def add_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.name = form.cleaned_data['name'].title()
            obj.save(request=request)
            changes_str = json.dumps({
                str(obj.id): f"Added role {obj.name}"
            })
            log_action(request.user, 'Roles', obj.id, f"Added role {obj.name}", changes_str)
            messages.success(request, "Role added successfully!")
            return redirect('role_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RoleForm()
    return render(request, 'beta_auth/role_form.html', {'form': form})

@login_required
@role_permission_required('change_role')
def edit_role(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    perm_list = permission_list()
    role_perms = role.permissions.values_list('id', flat=True)
    logs_objects = AuditLog.objects.filter(object_id=role.id)
    logs = []
    for log in logs_objects:
        logs.append(log_sanitize(log))
        
    context = {
        'logs': logs, 
        'permission_list':perm_list,
        'role_permission_list':role_perms
    }
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        context['form'] = form
        if form.is_valid():
            original_role = get_object_or_404(Role, id=role_id)
            obj = form.save(commit=False)
            if 'name' in form.changed_data:
                obj.name = form.cleaned_data['name'].title()
            obj.save()
            changes = []
            for field in form.changed_data:
                old_value = getattr(original_role, field)
                new_value = getattr(obj, field)
                changes.append(f"{field.upper()}: {old_value} -> {new_value}")
            
            changes_str = json.dumps({
                str(role.id): changes
            })
            if changes:
                log_action(request.user, 'Roles', role.id, f"Edited role {obj.name}", changes_str)
                messages.success(request, "Role updated successfully!")
                return redirect('role_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RoleForm(instance=role)
        context['form'] = form
    return render(request, 'beta_auth/role_form.html', context)

@login_required
@role_permission_required('delete_role')
def delete_role(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    role.deleted = True
    role.save()
    changes_str = json.dumps({
        str(role.id): f"Deleted role {role.name}"
    })
    log_action(request.user, 'Roles', role.id, f"Deleted role {role.name}", changes_str)
    messages.success(request, "Role deleted successfully!")
    return redirect('role_list')


@login_required
@role_permission_required('view_defaultpassword')
def password_list(request):
    passwords = DefaultPassword.objects.all()
    logs = [log_sanitize(log) for log in AuditLog.objects.filter(model_name='Default Passwords')]
    return render(request, 'beta_auth/password_list.html', {'passwords':passwords,'logs':logs})

@login_required
@role_permission_required('add_defaultpassword')
def add_password(request):
    next_url = request.GET.get('next')
    if request.method == 'POST':
        form = DefaultPasswordForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save(request=request)
            changes_str = json.dumps({
                str(obj.id):f"Created default password {obj.password}"
            })
            log_action(request.user, 'Default Passwords', obj.id, f"Created default password {obj.password}", changes_str)
            messages.success(request, "Default password created successfully!")
            redirect_url = request.POST.get('next')
            if redirect_url == 'None' or not redirect_url:
                redirect_url = 'password_list'
            return redirect(redirect_url)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DefaultPasswordForm()

    return render(request, 'beta_auth/password_form.html', {'form': form, 'next':next_url})


def login_view(request):
    next_url = request.GET.get('next')
    if request.user.is_authenticated:
       return redirect(next_url or 'dashboard')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                u = get_object_or_404(User, email=email)
                if not u.password_changed and not u.is_superuser:
                    return redirect(reverse('change_password', args=(u.id,)))
                login(request, user)
                return redirect(next_url or 'dashboard')
            else:
                messages.error(request, "Invalid credentials.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()

    return render(request, 'beta_auth/login.html', {'form': form})

def change_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.password_changed:
        messages.error(request, "Unauthorized action detected. This attempt has been recorded.")
        return redirect('login')     
    if request.method == "POST":
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get("new_password1")
            user.set_password(new_password)
            user.password_changed = True
            user.save()
            messages.success(request, "Your password has been updated successfully!")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ChangePasswordForm(user)
    
    return render(request, 'beta_auth/change_password.html', {'form': form})
    

def logout_view(request):
    logout(request)
    return redirect('login')


class ExpiringTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"

token_generator = ExpiringTokenGenerator()

def forgot_password_view(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.get(email=email)

            # Generate a token that includes a timestamp
            timestamp = int((now() + timedelta(hours=2)).timestamp())  # Expires in 2 hours
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            expiry_data = urlsafe_base64_encode(force_bytes(json.dumps({"exp": timestamp})))

            reset_link = request.build_absolute_uri(reverse("recover_password", args=[uid, token, expiry_data]))
            email_subject = "Password Reset Request"
            email_body = f"Click the link below to reset your password:\n{reset_link}\n\nThis link will expire in 2 hours."
            try:
                # send_mail(
                #     subject=email_subject,
                #     message=email_body,
                #     from_email=settings.EMAIL_HOST_USER,
                #     recipient_list=[email],
                #     fail_silently=False,
                # )
                ForgotPassword.objects.create(email=email,link=reset_link)
                file_path = os.path.join(settings.BASE_DIR, 'links_file.txt')
                with open(file_path, 'a') as links_file:
                    links_file.write(reset_link + '\n')
                    
                messages.success(request, 'Password recovery was successful. Check your email for further instruction.')
                return redirect("login")
            except (SMTPException, TimeoutError, Exception):
                messages.error(request, 'Could not complete your request. Try again later.')
    else:
        form = ForgotPasswordForm()
    return render(request, "beta_auth/forgot_password.html", {"form": form})

def recover_password_view(request, uidb64, token, expiry_data):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        expiry_info = json.loads(force_str(urlsafe_base64_decode(expiry_data)))
        expiry_time = expiry_info.get("exp")
        
        if not expiry_time or now().timestamp() > expiry_time:
            return render(request, "beta_auth/invalid_token.html", {"message": "This reset link has expired."})

        user = User.objects.get(pk=uid)
        
        if not token_generator.check_token(user, token):
            return render(request, "beta_auth/invalid_token.html", {"message": "Invalid or used reset link."})

    except (User.DoesNotExist, ValueError, TypeError, json.JSONDecodeError):
        return render(request, "beta_auth/invalid_token.html", {"message": "Invalid reset link."})

    if request.method == "POST":
        form = RecoverPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data["new_password1"])
            user.save()
            messages.success(request, 'Your password was changed successfully. Login with your new password.')
            return redirect("login")
    else:
        form = RecoverPasswordForm()
    
    return render(request, "beta_auth/recover_password.html", {"form": form})

@login_required
def new_change_password(request, user_id):
    user = get_object_or_404(User, id=user_id)   
    if request.method == "POST":
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get("new_password1")
            user.set_password(new_password)
            user.password_changed = True
            user.save()
            messages.success(request, "Your password has been updated successfully!")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ChangePasswordForm(user)
    
    return render(request, 'beta_auth/new_change_password.html', {'form': form})
