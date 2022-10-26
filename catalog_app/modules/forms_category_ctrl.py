# from ..models.category_model import Category
# from ..models.product_model import (Product, Middleship)
from ..models.catalog_model import Category, Product
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.utils import create_namedtuple_class
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget


class CatalogForm(forms.ModelForm):
    def __init__(self, *args, user=None, product=None, **kwargs):
        super(CatalogForm, self).__init__(*args, **kwargs)
        if user is not None and not user.is_superuser:
            self.fields['user'].queryset = User.objects.filter(username=user.username)
        # if product is not None and not user.is_superuser:

    # def get_form_class(self):
    #     # interrogate the DB to get a list of categories, or categories and labels.
    #     choices = list(enumerate(product))  # [ (0,'cat0'), (1,'cat1'), ...]
    #     choicefield = forms.ChoiceField(choices=choices)
    #     return type('My_runtime_form',
    #                 (Category,),
    #                 {'product_map': choicefield}
    #                 )
    #
    name = forms.CharField(required=True)
    code = forms.CharField(required=True)
    image = forms.ImageField(required=False)
    content = forms.CharField(required=False, widget=CKEditorUploadingWidget())  # forms.CharField(required=False, widget=forms.Textarea())

    class Meta:
        model = Category
        # PRODUCT_CHOICES = (fields['product_map'])
        # product_map = forms.ChoiceField(choices='product_map')
        # model['product'] = forms.ChoiceField(label="Chọn sản phẩm", choices=Product.objects.all())
        fields = ['name', 'code', 'image', 'content', 'product', 'user']
        labels = {'name': _('Tên Category (*)'), 'code': _('Mã Category (*)'), 'image': _('Hình ảnh category'), 'content': _('Nội dung'),
                  'product': _('Chọn sản phẩm (nếu có)'), 'user': _('Tài khoản tạo (*)')}
        widgets = {
            # 'product': forms.ChoiceField(attrs={'required': False}),
            # 'image': forms.ImageField(attrs={'required': False}),
            # 'content': forms.Textarea()
        }


