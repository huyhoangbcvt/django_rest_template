from rest_framework import serializers
from user_app.models.account_model import Profile
# from .models.category_model import Category
# from .models.product_model import Product
from .models.catalog_model import (Product, Category)


class User_appSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class Category_appSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class Product_appSerializer(serializers.ModelSerializer):
    catalog = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'