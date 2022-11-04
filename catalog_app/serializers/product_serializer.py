from rest_framework import serializers
from ..models.catalog_model import (Product, Category)
from ..serializers.category_serializer import CategorySerializer
# from ..serializers.contact_serializer import ContactSerializer
from user_app.serializers.user_serializer import UserSerializer
from django.db import transaction


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    user = UserSerializer(required=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Product
        # fields = '__all__'country
        fields = ['id', 'name', 'code', 'image', 'description', 'country', 'active', 'user', 'categories']


class CustomPKRelatedField(serializers.PrimaryKeyRelatedField):
    """A PrimaryKeyRelatedField derivative that uses named field for the display value."""
    def __init__(self, **kwargs):
        self.display_field = kwargs.pop("display_field", "name")
        super(CustomPKRelatedField, self).__init__(**kwargs)

    def display_value(self, instance):
        # Use a specific field rather than model stringification
        return getattr(instance, self.display_field)


class ProductAddSerializer(serializers.ModelSerializer):
    # def get_field_choices():
    #     return sorted([
    #         (p.id, p.name) for p in Category.objects.all()
    #     ])
    # categories = serializers.MultipleChoiceField(choices=get_field_choices(), required=False, )
    # categories = CustomPKRelatedField(queryset=Category.objects.all(), many=True)
    categories = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=Category.objects.all())

    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['name', 'code', 'image', 'description', 'country', 'user', 'categories']

    # def get_categories(self, obj):
    #     return obj.categories.all().values("name")

    @transaction.atomic
    def save(self, request):
        _product = Product.objects.create(
                            name=self.validated_data.get('name'),
                            code=self.validated_data.get('code'),
                            image=self.validated_data.get('image'),
                            description=self.validated_data.get('description'),
                            user=self.validated_data.get('user'),)
        # _product = product.save()  # product.refresh_from_db()
        _categories = request.data.getlist('categories')
        print(_categories)
        if _categories:
            category_set = []
            for category in _categories:
                # _product.categories.add(category)
                category_set.append(category)
            _product.categories.set(category_set)  # _product.categories.save()
        return _product


class ProductCategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    categories = CategorySerializer(many=True)
    # contacts = ContactSerializer(many=True)

    class Meta:
        model = Product
        # fields = '__all__'country
        fields = ['id', 'name', 'code', 'image', 'description', 'country', 'active', 'user', 'categories']
