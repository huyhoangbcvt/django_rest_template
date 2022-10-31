from rest_framework import serializers
from ..models.catalog_model import (Product, Category)
from django import forms
from user_app.serializers.user_serializer import UserSerializer
from .product_serializer import ProductCategorySerializer
from django.contrib.auth.models import User


# Rest framework support HyperlinkedModelSerializer, Serializer, ModelSerializer, ListSerializer
class CategorySerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user = UserSerializer(required=True)
    products = ProductCategorySerializer(many=True)
    # products = forms.ModelMultipleChoiceField(queryset=Product.objects.all())

    class Meta:
        model = Category
        # fields = '__all__'
        fields = ['id', 'name', 'code', 'image', 'content', 'active', 'products', 'user']


class CategoryAddSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # product_map = serializers.StringRelatedField(read_only=True)
    user = UserSerializer
    # product_map = forms.ModelChoiceField(
    #     queryset=Product.objects.all(),
    #     widget=forms.Select
    # )
    # products = ProductSerializer
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all())

    class Meta:
        model = Category
        # fields = '__all__'
        fields = ['name', 'code', 'image', 'content', 'user', 'products']
