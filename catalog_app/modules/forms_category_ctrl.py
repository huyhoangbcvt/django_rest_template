# from ..models.category_model import Category
# from ..models.product_model import (Product, Middleship)
from ..models.catalog_model import Category, Product
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.utils import create_namedtuple_class
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget
from django.utils.datastructures import MultiValueDict, MultiValueDictKeyError


class CatalogForm(forms.ModelForm):
    name = forms.CharField(required=True)
    code = forms.CharField(required=True)
    image = forms.ImageField(required=False)
    content = forms.CharField(required=False,
                              widget=CKEditorUploadingWidget())  # forms.CharField(required=False, widget=forms.Textarea())
    # products = forms.ModelMultipleChoiceField(widget=M2MSelect, required=True, queryset=Product.objects.all())
    products = forms.ModelMultipleChoiceField(required=False, widget=forms.SelectMultiple, queryset=Product.objects.all())

    def __init__(self, *args, user=None, product=None, **kwargs):
        super(CatalogForm, self).__init__(*args, **kwargs)
        if user is not None and not user.is_superuser:
            self.fields['user'].queryset = User.objects.filter(username=user.username)
        # if product is not None and not user.is_superuser:
        # selected_products = kwargs.pop('selected_products', None)  # queryset returned from function
        # self.fields['products'].queryset = selected_products
        # self.fields['orders'].queryset = OrderModal.objects.filter(pk=2)
        # print(product)
        # if product is not None:
        #     # self.fields['products'].queryset = product
        #     self.fields['products'] = forms.ModelMultipleChoiceField(required=False, queryset=product)

    class Meta:
        model = Category
        # PRODUCT_CHOICES = (fields['product_map'])
        # product_map = forms.ChoiceField(choices='product_map')
        # model['product'] = forms.ChoiceField(label="Chọn sản phẩm", choices=Product.objects.all())
        fields = ['name', 'code', 'image', 'content', 'user', 'products']
        labels = {'name': _('Tên Category (*)'), 'code': _('Mã Category (*)'), 'image': _('Hình ảnh category'), 'content': _('Nội dung'),
                  'user': _('Tài khoản tạo (*)')}
        # widgets = {
        #     'products': forms.SelectMultiple(attrs={'required': False})
        # }
        # widgets = {
        #     'product': forms.ChoiceField(attrs={'required': False}),
        #     'image': forms.ImageField(attrs={'required': False}),
        #     'content': forms.Textarea()
        # }


class M2MSelect(forms.SelectMultiple):
    allow_multiple_selected = False


# class M2MSelect(forms.Select):
#     def value_from_datadict(self, data, files, name):
#         if isinstance(data, (MultiValueDict, MultiValueDictKeyError)):
#             return data.getlist(name)
#         return data.get(name, None)


# class M2MSelect(forms.SelectMultiple):
#     def render(self, name, value, attrs=None, choices=()):
#         rendered = super(M2MSelect, self).render(name, value=value, attrs=attrs, choices=choices)
#         return rendered.replace(u'multiple="multiple"', u'')
