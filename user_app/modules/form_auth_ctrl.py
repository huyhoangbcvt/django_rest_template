"""
Definition of forms.
"""

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm,  # send mail
    SetPasswordForm, PasswordChangeForm, AdminPasswordChangeForm,
)
from ..models.account_model import Profile, Social
from django.conf import settings
from django.template.defaultfilters import default
# from .widgets
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.utils.translation import gettext_lazy as _


# ========== FORM Authentication =============
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


# =========== FORM registration ============
class SignUpForm(UserCreationForm):  # UserCreationForm  or forms.Form
    # Custom
    first_name = forms.CharField(label="Tên (*)", max_length=254,
                                 widget=forms.TextInput({
                                     'class': 'form-control',
                                     'placeholder': 'Tên'}))
    last_name = forms.CharField(label="Họ đệm (*)", max_length=254,
                                widget=forms.TextInput({
                                    'class': 'form-control',
                                    'placeholder': 'Họ tên lót'}))
    email = forms.CharField(label="Mail điện tử (*)", max_length=100, required=True,
                            widget=forms.TextInput({
                                'class': 'form-control',
                                'placeholder': 'Email'}))
    birthday = forms.DateField(label="Ngày sinh", required=False,
                               help_text='(định dạng mm/dd/yyyy)',
                               widget=forms.DateInput(format='%m/%d/%Y', attrs={'type': 'date', 'id': 'datepicker'}),
                               input_formats=settings.DATE_INPUT_FORMATS)

    phone_number = forms.CharField(label="Số điện thoại", max_length=20, required=False,
                                   widget=forms.TextInput({
                                       'class': 'form-control',
                                       'placeholder': 'Số điện thoại'}))
    username = forms.CharField(label="Tên đăng nhập (*)", max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Tên đăng nhập'}))
    # first_name = forms.CharField(max_length=100, help_text='Last Name')
    password1 = forms.CharField(label="Mật khẩu (*)",
                                widget=forms.PasswordInput({
                                    'class': 'form-control',
                                    'placeholder': 'Mật khẩu'}))
    password2 = forms.CharField(label="Re-Password (*)",
                                widget=forms.PasswordInput({
                                    'class': 'form-control',
                                    'placeholder': 'Gõ lại mật khẩu'}))


# ======================== FORM change password to send email ===============================
class ResetPassToEmailForm(PasswordResetForm):  # PasswordResetForm
    """Authentication form which uses boostrap CSS."""
    email = forms.CharField(label="Mail điện tử (*)", max_length=100,
                            widget=forms.TextInput({
                                'class': 'form-control',
                                'placeholder': 'Nhập email để lấy lại mật khẩu'}))


# ======================== FORM reset password =============================== forms.Form
class ResetPassForm(SetPasswordForm):  # SetPasswordForm  #forms.Form
    """Authentication form which uses boostrap CSS."""
    new_password1 = forms.CharField(label="Mật khẩu mới", min_length=6,
                                    widget=forms.PasswordInput({
                                        'class': 'form-control',
                                        'placeholder': 'Mật khẩu mới'}))
    new_password2 = forms.CharField(label="Xác nhận mật khẩu mới", min_length=6,
                                    widget=forms.PasswordInput({
                                        'class': 'form-control',
                                        'placeholder': 'Gõ lại mật khẩu mới'}))


# ======================== FORM password change =============================== forms.Form
class PassChangeForm(PasswordChangeForm):  # PasswordChangeForm
    """Authentication form which uses boostrap CSS."""
    old_password = forms.CharField(label="Mật khẩu cũ (*)",
                                   widget=forms.PasswordInput({
                                       'class': 'form-control',
                                       'placeholder': 'Mật khẩu cũ'}))
    new_password1 = forms.CharField(label="Mật khẩu mới (*)", min_length=6,
                                    widget=forms.PasswordInput({
                                        'class': 'form-control',
                                        'placeholder': 'Mật khẩu mới'}))
    new_password2 = forms.CharField(label="Xác nhận mật khẩu mới (*)", min_length=6,
                                    widget=forms.PasswordInput({
                                        'class': 'form-control',
                                        'placeholder': 'Gõ lại mật khẩu mới'}))


# ============ FORM profile ================
class UserForm(ModelForm):  # UserCreationForm
    email = forms.CharField(label="Mail điện tử", help_text='Yandex/ Gmail/ Outlook', max_length=100, required=False,
                            widget=forms.TextInput({
                                'class': 'form-control',
                                'placeholder': 'Email'}))
    first_name = forms.CharField(label="Tên (*)", max_length=254,
                                 widget=forms.TextInput({
                                     'class': 'form-control',
                                     'placeholder': 'Tên'}))
    last_name = forms.CharField(label="Họ đệm (*)", max_length=254,
                                widget=forms.TextInput({
                                    'class': 'form-control',
                                    'placeholder': 'Họ tên lót'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )
        labels = {'first_name': _('Tên (*)'), 'last_name': _('Họ đệm (*)')}


class ProfileForm(ModelForm):
    # GOOGLE, FACEBOOK, LINKEDIN = range(3)
    # social_network = forms.ChoiceField(label="Mạng xã hội", choices=SOCIAL_CHOICES)
    # social_network = forms.TypedChoiceField(null=True, default=0, blank=True)
    phone_number = forms.CharField(label="Số điện thoại", max_length=20, required=False,
                                  widget=forms.TextInput({
                                      'class': 'form-control',
                                      'placeholder': 'Số điện thoại'}))
    address = forms.CharField(label="Địa chỉ", max_length=30, required=False,
                              widget=forms.TextInput({
                                  'class': 'form-control',
                                  'placeholder': 'Nhập địa chỉ'}))
    description = forms.CharField(label="Mô tả", max_length=100, required=False,
                                  widget=forms.Textarea({
                                      "rows": 3, "cols": 10,
                                      'class': 'form-control',
                                      'placeholder': 'Mô tả'}))
    website = forms.URLField(label="Link cá nhân", required=False,
                             widget=forms.TextInput({
                                 'class': 'form-control',
                                 'placeholder': 'Link cá nhân'}))
    # widget=forms.SelectDateWidget
    birthday = forms.DateField(label="Ngày sinh", required=False,
                               help_text='(định dạng dd/mm/yyyy)',
                               widget=forms.DateInput(
                                   format='%d/%m/%Y',
                                   attrs={'type': 'date', 'id': 'datepicker'}
                               ), input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Profile
        fields = ('birthday', 'phone_number', 'address', 'description', 'website', 'image')
        labels = {'birthday': _('Ngày sinh'), 'image': _('Hình ảnh Avatar')}
        help_texts = {'birthday': _('Nhập vào một ngày sinh định dạng mm/dd/yyyy (mặc định 01/01/2020).'),
                      'image': _('Chọn một file từ thiết bị làm Avatar.')}


class SocialForm(ModelForm):
    GOOGLE = 1
    FACEBOOK = 2
    LINKEDIN = 3
    SOCIAL_CHOICES = (
        (GOOGLE, 'Google'),
        (FACEBOOK, 'Facebook'),
        (LINKEDIN, 'Linkedin'),
    )
    social_type = forms.ChoiceField(label="Mạng xã hội", choices=SOCIAL_CHOICES)

    class Meta:
        model = Social
        fields = ('username_social', 'social_type', 'birthday', 'image', 'phone_number', 'address', 'note', 'website', 'user')
        labels = {'username_social': _('Tài khoản mạng xã hội (*)'), 'social_type': _('Loại xã hội'),
                  'birthday': _('Ngày sinh'), 'image': _('Hình ảnh Avatar'), 'user': _('Tài khoản local (nếu có)')}
        help_texts = {'birthday': _('Nhập vào một ngày sinh định dạng mm/dd/yyyy (mặc định 01/01/2020).'),
                      'image': _('Chọn một file từ thiết bị làm Avatar.')}


class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datepicker-input',
            'data-target': '#datetimepicker1'
        })
    )


class DateTimeForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M:%S'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
