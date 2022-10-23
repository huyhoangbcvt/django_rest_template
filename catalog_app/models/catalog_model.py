from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from django import forms


class BaseProductCategoryModel(models.Model):
    class Meta:
        abstract = True
    name = models.CharField(max_length=100, default=None)
    code = models.CharField(max_length=50, unique=True)
    # Allow None null=True
    image = models.ImageField(upload_to='catalogs/%Y/%m/', null=True, default=None, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(null=True, auto_now=True, blank=True)  # default=datetime.now


# @python_2_unicode_compatible
class Product(BaseProductCategoryModel):
    class Meta:
        unique_together = {'name', 'category'}
    description = models.TextField(max_length=1000, null=True, default=None, blank=True)
    country = models.CharField(max_length=50, null=True, default=None, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='Product')  # Not delete Category
    # category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='Product')
    # category = models.ManyToManyField(Category, related_name='catalog_products')
    # middles = models.ManyToManyField('Category', related_name='catalog_products', through='catalog_product_category')
    # category = models.ManyToManyField(Category, help_text='Select a Category for this Product')
    # middles = models.ManyToManyField('Category', related_name='Product', through='Middleship')
    active = models.BooleanField(
        _("post status"),
        default=True,
        help_text=_("Open - close status post with user"),
    )

    def __str__(self):
        return self.p_title
        # return f"{self.p_title}, {self.p_name}, {self.p_code}, {self.p_date}, {self.p_country}"

    # def __unicode__(self):
    #     return u"%s" % self.user

    class Meta:
        managed = True
        ordering = ['-created_at', 'name']
        # db_table = 'catalog_product'
        # verbose_name = 'catalog_product'
        # verbose_name_plural = 'catalog_products'


# Create your models here.
class Category(BaseProductCategoryModel):
    class Meta:
        unique_together = {'name', 'product'}
    # Allow None null=True
    content = models.TextField(max_length=1000, null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='Category')
    # product_map = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, default=0, related_name='Middleship')
    # product = models.ManyToManyField(Product, help_text='Select a Product for this Catalog')
    # product_map = models.PositiveSmallIntegerField(null=True, default=0, blank=True)
    active = models.BooleanField(
        _("post status"),
        default=True,
        help_text=_("Open - close status post with user"),
    )

    # Ko có cái này thì table tạo ra theo appname_classmodel
    class Meta:
        managed = True
        ordering = ['-created_at', 'name']
        # db_table = 'catalog_category'
        # verbose_name = 'catalog_category'
        # verbose_name_plural = 'catalog_categories'

    def __str__(self):
        return self.title
        # return f"{self.title}, {self.image}, {self.body}, {self.user}"


# class Middleship(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     date_joined = models.DateField(null=True, default=datetime.now)
#
#     def __str__(self):
#         return "{}_{}".format(self.Product.__str__(), self.Category.__str__())
#
#     class Meta:
#         managed = True
#         db_table = 'catalog_product_category'
#         verbose_name = 'catalog_product_category'
#         verbose_name_plural = 'catalog_product_categories'
