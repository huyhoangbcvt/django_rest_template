from rest_framework import serializers
from ..models.catalog_model import (Product, Category)
from django import forms
from user_app.serializers.user_serializer import UserSerializer
# from .product_serializer import ProductSerializer
from django.contrib.auth.models import User
from django.db import transaction
from ..util.fields import MultipleChoiceField


# Rest framework support HyperlinkedModelSerializer, Serializer, ModelSerializer, ListSerializer
class CategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    # products = ProductSerializer(many=True)

    class Meta:
        model = Category
        # fields = '__all__'
        fields = ['id', 'name', 'code', 'image', 'content', 'active', 'products', 'user']


class CustomPKRelatedField(serializers.PrimaryKeyRelatedField):
    """A PrimaryKeyRelatedField derivative that uses named field for the display value."""
    def __init__(self, **kwargs):
        self.display_field = kwargs.pop("display_field", "name")
        super(CustomPKRelatedField, self).__init__(**kwargs)

    def display_value(self, instance):
        # Use a specific field rather than model stringification
        return getattr(instance, self.display_field)


class CategoryAddSerializer(serializers.ModelSerializer):
    # user = UserSerializer
    # def get_field_choices():
    #     return sorted([
    #         (p.id, p.name) for p in Product.objects.all()
    #     ])
    # products = serializers.MultipleChoiceField(choices=get_field_choices(), required=False,)
    products = CustomPKRelatedField(queryset=Product.objects.all(), many=True)
    # products = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=Product.objects.all())

    class Meta:
        model = Category
        # fields = '__all__'
        fields = ['name', 'code', 'image', 'content', 'user', 'products']

    @transaction.atomic
    def save(self, request):
        # category = Category(**self.validated_data)
        _category = Category.objects.create(
                            name=self.validated_data.get('name'),
                            code=self.validated_data.get('code'),
                            image=self.validated_data.get('image'),
                            content=self.validated_data.get('content'),
                            user=self.validated_data.get('user'),)
        # _category = category.save()  # category.refresh_from_db()
        _products = request.data.get('products')
        print(_products)
        if _products:
            product_set = []
            for product in _products:
                product_set.append(product)
                # _category.products.add(category)
            _category.products.set(product_set)  # _category.products.save()
        return _category
