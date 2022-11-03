from rest_framework import serializers
from ..models.catalog_model import (Product, Category)
from django import forms
from user_app.serializers.user_serializer import UserSerializer
# from .product_serializer import ProductSerializer
from django.contrib.auth.models import User
from django.db import transaction


# Rest framework support HyperlinkedModelSerializer, Serializer, ModelSerializer, ListSerializer
class CategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    # products = ProductSerializer(many=True)

    class Meta:
        model = Category
        # fields = '__all__'
        fields = ['id', 'name', 'code', 'image', 'content', 'active', 'products', 'user']


class CategoryAddSerializer(serializers.ModelSerializer):
    # user = UserSerializer
    # products = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=Product.objects.all())

    class Meta:
        model = Category
        # fields = '__all__'
        fields = ['name', 'code', 'image', 'content', 'user', 'products']

    @transaction.atomic
    def save(self, request):
        category = Category(**self.validated_data)
        # category = Category.objects.create(category)
        category = category.save()  # category.refresh_from_db()
        products = request.data.get('products')
        if products:
            product_set = []
            for product in products:
                product_set.append(product)
            category.products.set(product_set)  # category.products.save()
        return category
