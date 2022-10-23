from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class RegistrationUserForm(UserCreationForm):
    role = forms.CharField(max_length=20, required=False)
    email = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password1', 'password2', 'role')


class LoginForm(AuthenticationForm):  # AuthenticationForm
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(label="Tên đăng nhập (*)", max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Tên đăng nhập'}))
    password = forms.CharField(label=_("Password") + " (*)",
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Mật khẩu'}))
