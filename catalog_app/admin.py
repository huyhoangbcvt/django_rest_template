from django.contrib import admin
# from .models.category_model import Category
# from .models.product_model import Product
from .models.catalog_model import (Product, Category)

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
