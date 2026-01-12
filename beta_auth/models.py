from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
import uuid


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID"))
    name = models.CharField(max_length=255, verbose_name=_("Role Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    reference_code = models.CharField(max_length=20, unique=True, blank=True, editable=False, verbose_name=_("Reference Code"))
    permissions = models.ManyToManyField(Permission, related_name='roles')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Created"))
    modified_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"))
    deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey('beta_auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name="roles_created", verbose_name=_("Created By"))

    class Meta:
        ordering = ['created_at']
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.reference_code:
                with transaction.atomic():
                    last_role = Role.objects.select_for_update().order_by('created_at').last()
                    new_code_number = 1 if not last_role else int(last_role.reference_code.split('-')[-1]) + 1
                    self.reference_code = f"IDBMS-ROLE-{new_code_number:04d}"

            if not self.created_by:
                request = kwargs.pop('request', None)
                if request and hasattr(request, 'user'):
                    self.created_by = request.user
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Organization(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    email = models.EmailField(verbose_name=_('Contact Email'), blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name=_('Contact Phone'))
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.name
    

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID"))
    email = models.EmailField(unique=True, verbose_name=_("Email Address"))
    name = models.CharField(max_length=255, verbose_name=_('Full Name'), null=True)
    role = models.ManyToManyField('beta_auth.Role', blank=True, related_name='users', verbose_name=_("Roles"))
    organization = models.ForeignKey('beta_auth.Organization', verbose_name=_('Organization'), on_delete=models.CASCADE, related_name='organization_users', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Created"))
    modified_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"))
    created_by = models.ForeignKey('beta_auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name="users_created", verbose_name=_("Created By"))
    deleted = models.BooleanField(default=False)
    password_changed = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def save(self, *args, **kwargs):
        if not self.created_by and self._state.adding:
            request = kwargs.pop('request', None)
            if request and hasattr(request, 'user'):
                self.created_by = request.user
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

class DefaultPassword(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID"))
    password = models.CharField(max_length=20, verbose_name=_("Password"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Current"), editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Created"))
    modified_at = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"))
    created_by = models.ForeignKey('beta_auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name="passwords_created", verbose_name=_("Created By"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Default Password")
        verbose_name_plural = _("Default Passwords")

    def save(self, *args, **kwargs):
        DefaultPassword.objects.exclude(id=self.id).update(is_active=False)
        if not self.created_by and self._state.adding:
            request = kwargs.pop('request', None)
            if request and hasattr(request, 'user'):
                self.created_by = request.user
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.password
    
class UserSession(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_hidden = True
    
    def __str__(self):
        return f"{self.user.email} - {self.session_key}"
    
    class Meta:
        verbose_name = _("User Session")
        verbose_name_plural = _('User Sessions')
        ordering = ['-created_at']
    
class ForgotPassword(models.Model):
    email = models.CharField(max_length=255)
    link = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Forgot Passwords'
        ordering = ['-date']
    
    def __str__(self):
        return self.email
    