# Generated by Django 4.1.2 on 2022-11-01 01:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Social',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username_social', models.CharField(help_text='Required. 150 characters or fewer. Letters, digits and ./+/-/_ only.', max_length=150, verbose_name='username_social')),
                ('social_type', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('birthday', models.DateField(blank=True, default=None, null=True)),
                ('phone_number', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='images')),
                ('address', models.CharField(blank=True, default=None, max_length=150, null=True)),
                ('website', models.URLField(blank=True, default=None, max_length=256, null=True)),
                ('note', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Social', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'social',
                'verbose_name_plural': 'socials',
                'db_table': 'social',
                'ordering': ['created_at', 'birthday'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_type', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('birthday', models.DateField(blank=True, default=None, null=True)),
                ('phone_number', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='images')),
                ('address', models.CharField(blank=True, default=None, max_length=150, null=True)),
                ('description', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('website', models.URLField(blank=True, default=None, max_length=256, null=True)),
                ('role', models.CharField(blank=True, default='Guess', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
                'db_table': 'profile',
                'ordering': ['created_at', 'birthday'],
            },
        ),
    ]
