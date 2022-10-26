from django.contrib import admin
from django.utils.html import mark_safe
from .models.catalog_model import (Product, Category, Contact)
from .modules import forms_category_ctrl, forms_product_ctrl


class CategoryAdmin(admin.ModelAdmin):
    form = forms_category_ctrl.CatalogForm

    class Meta:
        css = {
            'all': ('/static/css/style_admin.css', )
        }
        js = ('/static/js/admin.js', )

    list_display = ["id", "name", "code", "image", "active", "content", "product", "created_at"]
    search_fields = ["name", "code", "product__name", "created_at"]
    list_filter = ["created_at", "active"]
    ordering = ("-created_at", "name", "-id", )
    readonly_fields = ["display_category_demo"]

    @staticmethod
    def display_category_demo(category):
        if category:
            return mark_safe("<img src='/media/{img_url}' width='150' alt='{avatar}' />".format(img_url=category.image.name, avatar=category.name) )
        return None

    # Override
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


class ProductAdmin(admin.ModelAdmin):
    form = forms_product_ctrl.ProductForm

    class Meta:
        css = {
            'all': ('/static/css/style_admin.css', )
        }
        js = ('/static/js/admin.js', )

    list_display = ["id", "name", "code", "image", "description", "active", "category", "country", "created_at"]  # , "contact"
    search_fields = ["name", "code", "category__name", "created_at", "contact__name", "contact__phone_number"]
    list_filter = ["created_at", "active"]
    readonly_fields = ["display_product_demo"]

    @staticmethod
    def display_product_demo(category):
        if category:
            return mark_safe("<img src='/media/{img_url}' width='150' alt='{avatar}' />".format(img_url=category.image.name, avatar=category.name))
        return None

    # Override
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


class ProductInlineAdmin(admin.StackedInline):
    model = Product
    pk_name = 'category'


# class CategoryInlineAdmin(admin.ModelAdmin):
#     inlines = (ProductInlineAdmin,)


# Register your models here.
admin.site.register(Category, CategoryAdmin)
# admin.site.register(Category, CategoryInlineAdmin)
admin.site.register(Contact)
admin.site.register(Product, ProductAdmin)
