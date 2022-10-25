# Generated by Django 4.1.2 on 2022-10-25 06:33

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
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=100)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='catalogs/%Y/%m/')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=True, help_text='Open - close status post with user', verbose_name='post status')),
                ('content', models.TextField(default=None, max_length=1000, null=True)),
            ],
            options={
                'ordering': ['-created_at', 'name'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('phone_number', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('date_joined', models.DateField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['-date_joined', 'name'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=100)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='catalogs/%Y/%m/')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=True, help_text='Open - close status post with user', verbose_name='post status')),
                ('description', models.TextField(blank=True, default=None, max_length=1000, null=True)),
                ('country', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='catalog_app.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at', 'name'],
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='category',
            name='contact',
            field=models.ManyToManyField(blank=True, null=True, to='catalog_app.contact'),
        ),
        migrations.AddField(
            model_name='category',
            name='product',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to='catalog_app.product'),
        ),
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
