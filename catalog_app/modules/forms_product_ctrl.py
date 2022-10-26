from ..models.catalog_model import Product
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget


class ProductForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        if user is not None and not user.is_superuser:
            self.fields['user'].queryset = User.objects.filter(username=user.username)

    name = forms.CharField(required=True)
    code = forms.CharField(required=True)
    image = forms.ImageField(required=False)
    description = forms.CharField(required=False, widget=CKEditorUploadingWidget())
    # description = forms.CharField(required=False, widget=forms.Textarea())

    class Meta:
        model = Product
        fields = ['name', 'code', 'image', 'description', 'country', 'category', 'user', 'contact']
        labels = {'name': _('Tên sản phẩm (*)'), 'code': _('Mã sản phẩm (*)'),
                  'image': _('Hình ảnh sản phẩm'), 'description': _('Mô tả sản phẩm'),
                  'country': _('Xuất xứ'), 'category': _('Chọn Category (*)'), 'user': _('Tài khoản tạo'), 'contact': _('Gắn liên hệ')}