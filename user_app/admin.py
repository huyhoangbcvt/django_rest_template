# Register your models here.
from django.contrib import admin
from django.utils.html import mark_safe
from .models.account_model import Profile, Social
from .modules import form_auth_ctrl
from catalog_app.models.catalog_model import Category, Product, Comment
from catalog_app.admin import CategoryAdmin, ProductAdmin
from upload_app.models import UploadFile
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm


class UserAdmin(admin.ModelAdmin):
    form = UserCreationForm
    list_display = ["username", "email", "first_name", "last_name", "is_active", "date_joined"]
    search_fields = ["username", "email", "first_name", "last_name"]
    list_filter = ["date_joined", "is_active"]
    ordering = ("-date_joined", "-id",)


class ProfileAdmin(admin.ModelAdmin):
    form = form_auth_ctrl.ProfileForm

    class Meta:
        css = {
            'all': ('/static/css/style_admin.css', )
        }
        js = ('/static/js/admin.js', )

    list_display = ["birthday", "phone_number", "image", "address", "description", "website", "role"]
    search_fields = ["phone_number", "address", "created_at", "user__username"]
    list_filter = ["created_at", "user__is_active"]
    readonly_fields = ["display_avatar"]
    ordering = ("-created_at", "-id",)

    @staticmethod
    def display_avatar(profile):
        if profile:
            return mark_safe("<img src='/media/{img_url}' width='150' alt='{avatar}' />".format(img_url=profile.image.name, avatar=profile.name))
        return None


class SocialAdmin(admin.ModelAdmin):
    form = form_auth_ctrl.SocialForm

    class Meta:
        css = {
            'all': ('/static/css/style_admin.css', )
        }
        js = ('/static/js/admin.js', )

    list_display = ["username_social", "social_type", "birthday", "image", "phone_number", "address", "website"]
    search_fields = ["username_social", "phone_number", "address", "created_at"]
    list_filter = ["created_at", "username_social"]
    readonly_fields = ["display_avatar"]
    ordering = ("-created_at", "-id",)

    @staticmethod
    def display_avatar(social):
        if social:
            return mark_safe("<img src='/media/{img_url}' width='150' alt='{avatar}' />".format(img_url=social.image.name, avatar=social.name))
        return None


class DjangoAdminSite(admin.AdminSite):
    site_header = 'HDWEBSOFT QUẢN TRỊ HỆ THỐNG TRAINING DJANGO REST - TEMPLATE'


# Register your models here
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Social, SocialAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
# admin.site.register(Contact, ContactAdmin)
admin.site.register(Comment)
admin.site.register(UploadFile)

admin_site = DjangoAdminSite('django_rest_template')
# admin_site.register(User, UserAdmin)
# admin_site.register(Group)
# admin_site.register(Profile, ProfileAdmin)
# admin_site.register(Social, SocialAdmin)
#
# admin_site.register(Category, CategoryAdmin)
# admin_site.register(Product, ProductAdmin)
# admin_site.register(Contact, ContactAdmin)
# admin_site.register(Comment)
# admin_site.register(UploadFile)
