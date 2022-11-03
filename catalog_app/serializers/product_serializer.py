from rest_framework import serializers
from ..models.catalog_model import (Product, Category)
from ..serializers.category_serializer import CategorySerializer
# from ..serializers.contact_serializer import ContactSerializer
from user_app.serializers.user_serializer import UserSerializer
from django.db import transaction


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    user = UserSerializer(required=True)
    categories = CategorySerializer

    class Meta:
        model = Product
        # fields = '__all__'country
        fields = ['id', 'name', 'code', 'image', 'description', 'country', 'active', 'user', 'categories']


class ProductAddSerializer(serializers.ModelSerializer):
    # user = UserSerializer(required=True)
    # categories = serializers.PrimaryKeyRelatedField(required=False, queryset=Category.objects.prefetch_related('products'))
    # categories = serializers.PrimaryKeyRelatedField(required=False, queryset=Category.objects.all())
    # categories = CategorySerializer(many=True)
    # categories = serializers.MultipleChoiceField(required=False, choices=Category.objects.all())
    # categories = serializers.SerializerMethodField('get_categories')

    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['name', 'code', 'image', 'description', 'country', 'user', 'categories']

    # def get_categories(self, obj):
    #     return obj.categories.all().values("name")

    @transaction.atomic
    def save(self, request):
        _product = Product(**self.validated_data)
        # print(product)
        # product = Product.objects.create(product)
        _product = _product.save()  # product.refresh_from_db()
        # print(_product)
        # print(self.validated_data)
        categories = request.data.get('categories')
        if categories:
            category_set = []
            for category in categories:
                category_set.append(category)
            Category.products.set(category_set)
            # _product.products.save()
        return _product


class ProductCategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    categories = CategorySerializer(many=True)
    # contacts = ContactSerializer(many=True)

    class Meta:
        model = Product
        # fields = '__all__'country
        fields = ['id', 'name', 'code', 'image', 'description', 'country', 'active', 'user', 'categories']