from django import forms
from .models import User, Role, DefaultPassword,Organization
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name','organization','role']
        widgets = {
            'email': forms.EmailInput(),
            'role': forms.SelectMultiple(attrs={'class': 'multi-select'}),
            'name': forms.TextInput(),
            'organization': forms.Select(attrs={'class': 'single-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['role'].queryset = Role.objects.filter(deleted=False)
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()
            field.required = True

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(),
            'description': forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            
    def clean_name(self):
        name = self.cleaned_data.get('name')
        instance = self.instance
        if instance and instance.name:
            if Role.objects.filter(name__iexact=name, deleted=False).exclude(pk=instance.pk).exists():
                raise forms.ValidationError("A role with this name already exists.")
        else:
            if Role.objects.filter(name__iexact=name, deleted=False).exists():
                raise forms.ValidationError("A role with this name already exists.")
        return name
    
class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(),
            'email': forms.EmailInput(),
            'phone': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['name'].required = True
        self.fields['email'].required = True

    def clean_name(self):
        name = self.cleaned_data.get('name')
        instance = self.instance
        if instance and instance.name:
            if Organization.objects.filter(name__iexact=name).exclude(pk=instance.pk).exists():
                raise forms.ValidationError("An organization with this name already exists.")
        else:
            if Organization.objects.filter(name__iexact=name).exists():
                raise forms.ValidationError("An organization with this name already exists.")
        return name


class DefaultPasswordForm(forms.ModelForm):
    class Meta:
        model = DefaultPassword
        fields = ['password']
        widgets = {
            'password': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email Address", max_length=254)
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Your current password was entered incorrectly. Please try again.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        old_password = self.cleaned_data.get('old_password')

        if new_password1 and new_password2:
            if new_password1 == old_password:
                self.add_error('new_password1', "Your old password cannot be your new password.")
            else:
                if new_password1 != new_password2:
                    self.add_error('new_password1', "The new passwords do not match.")
                    self.add_error('new_password2', "The new passwords do not match.")
                else:
                    try:
                        validate_password(new_password1)
                    except ValidationError as e:
                        self.add_error('new_password1', e)
        return cleaned_data

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No account found with this email.")
        return email

class RecoverPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                self.add_error('new_password1', "The new passwords do not match.")
                self.add_error('new_password2', "The new passwords do not match.")
            else:
                try:
                    validate_password(new_password1)
                except forms.ValidationError as e:
                    self.add_error('new_password1', e)

        return cleaned_data
    