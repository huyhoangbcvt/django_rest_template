from rest_framework import serializers
from ..models.catalog_model import (Product, Category)
from ..serializers.category_serializer import CategorySerializer
# from ..serializers.contact_serializer import ContactSerializer
from user_app.serializers.user_serializer import UserSerializer


class ProductSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    categories = CategorySerializer
    # contacts = ContactSerializer(many=True)

    class Meta:
        model = Product
        # fields = '__all__'country
        fields = ['id', 'name', 'code', 'image', 'description', 'country', 'active', 'user', 'categories']


class ProductAddSerializer(serializers.ModelSerializer):
    # categories = serializers.PrimaryKeyRelatedField(queryset=Product.objects.prefetch_related('catalog_products'))
    user = UserSerializer(required=True)
    categories = CategorySerializer

    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['name', 'code', 'image', 'description', 'country', 'user', 'categories']


class ProductCategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    categories = CategorySerializer(many=True)
    # contacts = ContactSerializer(many=True)

    class Meta:
        model = Product
        # fields = '__all__'country
        fields = ['id', 'name', 'code', 'image', 'description', 'country', 'active', 'user', 'categories']