from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from django import forms
from ckeditor.fields import RichTextField


class BaseProductCategoryModel(models.Model):
    class Meta:
        abstract = True
    name = models.CharField(max_length=100, default=None)
    code = models.CharField(max_length=50, unique=True)
    # Allow None null=True
    image = models.ImageField(upload_to='catalogs/%Y/%m/', null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)  # default=datetime.now
    active = models.BooleanField(
        _("post status"),
        default=True,
        help_text=_("Open - close status post with user"),
    )


# Create your models here.
class Category(BaseProductCategoryModel):
    class Meta:
        unique_together = {'name', 'products'}
    # Allow None null=True
    content = RichTextField(max_length=1000, null=True, default=None)  # models.TextField(max_length=1000, null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True, default=0, related_name='categories')
    # products = models.ManyToManyField('Product', null=True, blank=True, related_name='categories', through='Middleship')

    # No Meta then table will create default via appname_classmodel
    class Meta:
        managed = True
        ordering = ['-created_at', 'name']
        # db_table = 'catalog_category'
        # verbose_name = 'catalog_category'
        # verbose_name_plural = 'catalog_categories'

    def __str__(self):
        return self.name
        # return f"{self.name}, {self.image}, {self.body}, {self.user}"


# @python_2_unicode_compatible
class Product(BaseProductCategoryModel):
    class Meta:
        unique_together = {'name'}
    description = RichTextField(max_length=1000, null=True, default=None, blank=True)  # models.TextField(max_length=1000, null=True, default=None, blank=True)
    country = models.CharField(max_length=50, null=True, default=None, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')  # Not delete Product
    # contacts = models.ManyToManyField('Contact', null=True, blank=True, related_name='products')
    categories = models.ManyToManyField(Category, null=True, blank=True, related_name='products', through='Middleship')

    def __str__(self):
        return self.name

    # def __unicode__(self):
    #     return u"%s" % self.user

    class Meta:
        managed = True
        ordering = ['-created_at', 'name']
        # db_table = 'catalog_product'
        # verbose_name = 'catalog_product'
        # verbose_name_plural = 'catalog_products'


# class Contact(models.Model):
#     class Meta:
#         unique_together = {'name', 'phone_number'}
#     name = models.CharField(max_length=100, unique=True)
#     phone_number = models.CharField(max_length=20, null=True, default=None, blank=True)
#     date_joined = models.DateField(auto_now_add=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         managed = True
#         ordering = ['-date_joined', 'name']


class Comment(models.Model):
    content = RichTextField(max_length=1000, null=True, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)  # default=datetime.now


class Middleship(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_joined = models.DateField(null=True, default=datetime.now)

    def __str__(self):
        return "{}_{}".format(self.Product.__str__(), self.Category.__str__())

    class Meta:
        managed = True
        db_table = 'catalog_product_categories'
        verbose_name = 'catalog_product_categories'
        verbose_name_plural = 'catalog_product_categories'
