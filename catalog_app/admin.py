from django.contrib import admin
from django.utils.html import mark_safe
# from .models.category_model import Category
# from .models.product_model import Product
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
    readonly_fields = ["image_display_demo"]

    def image_display_demo(self, category):
        if category:
            return mark_safe("<img src='/media/{img_url}' width='150' alt='{avatar}' />"
                             .format(img_url=category.image.name, avatar=category.name) )
        return None


class ProductAdmin(admin.ModelAdmin):
    form = forms_product_ctrl.ProductForm

    class Meta:
        css = {
            'all': ('/static/css/style_admin.css', )
        }
        js = ('/static/js/admin.js', )

    list_display = ["id", "name", "code", "image", "active", "description", "category", "country", "created_at"]
    search_fields = ["name", "code", "category__name", "created_at"]
    list_filter = ["created_at", "active"]
    readonly_fields = ["image_display_demo"]

    def image_display_demo(self, category):
        if category:
            return mark_safe("<img src='/media/{img_url}' width='150' alt='{avatar}' />"
                             .format(img_url=category.image.name, avatar=category.name))
        return None


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Contact)
admin.site.register(Product, ProductAdmin)
