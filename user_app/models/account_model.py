from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime


# @python_2_unicode_compatible
class Profile(models.Model):
    # id = models.AutoField(primary_key=True, serialize=False)  # phiên bản python 3.9 bắt buộc phải đ/n khóa chính
    # id = models.AutoField(auto_create=True, serialize=False)
    social_network = models.PositiveSmallIntegerField(null=True, default=0, blank=True)
    birthday = models.DateField(null=True, default=None, blank=True)
    phone_number = models.CharField(max_length=20, null=True, default=None, blank=True)
    images = models.ImageField(upload_to='images', null=True, default=None, blank=True)
    address = models.CharField(max_length=150, null=True, default=None, blank=True)
    description = models.CharField(max_length=100, null=True, default=None, blank=True)
    website = models.URLField(max_length=256, null=True, default=None, blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  # id table user
    role = models.CharField(max_length=20, default='Guess', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True) # default=datetime.now
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)  # auto_now_add=True

    class Meta:
        ordering = ['created_at', 'birthday']
        # managed = True
        db_table = 'profile'
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def __str__(self):
        return self.user.username


# Run update_profile() after the end of the save() method
# create_or_update_user_profile
# post_save: Gửi signal khi kết thúc hàm save()
# sender=User: chỉ nhận signal từ User Model
# instance: instance được lưu
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # If the user is created successfully
    if created:
        # Create user profile
        Profile.objects.create(user=instance)
    instance.profile.save()
