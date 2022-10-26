# Register your models here.
from django.contrib import admin
from django.utils.html import mark_safe
from .models.account_model import Profile, Social
from .modules import form_auth_ctrl


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

    @staticmethod
    def display_avatar(social):
        if social:
            return mark_safe("<img src='/media/{img_url}' width='150' alt='{avatar}' />".format(img_url=social.image.name, avatar=social.name))
        return None


# Register your models here
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Social, SocialAdmin)
