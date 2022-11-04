from django.urls import path, re_path, include, reverse
from .modules import (
    views_catalog, views_category, views_product, views_contact, views_comment,
    views_catalog_ctrl, views_category_ctrl, views_product_ctrl,
)
# from .admin import admin_site
app_name = 'catalog'

# determine the name from the viewset, as it does not have a `.queryset` attribute.
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'categories', views_category.CategoryViewSet, basename="category")
router.register(r'products', views_product.ProductViewSet, basename="product")
router.register(r'comments', views_comment.CommentViewSet, basename="comment")
# router.register(r'contacts', views_contact.ContactViewSet, basename="contact")

urlpatterns = [
    # path('admin/', admin_site.urls),
    # =============| APIs |============
    path(r'api/', include(router.urls)),  # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # =============| Web |============
    path('', views_catalog_ctrl.CatalogView.as_view(), name="catalog"),
    path('categories/', views_category_ctrl.category_list, name="categories"),
    path('categories/add-category/', views_category_ctrl.AddCategory.as_view(), name='category_form'),
    path('categories/<int:pk>/change/', views_category_ctrl.ChangeCategory.as_view(), name='category_change'),
    path('categories/<int:pk>/view/', views_category_ctrl.CategoryDisplay.as_view(), name='category_detail'),

    path('products/', views_product_ctrl.product_list, name="products"),
    # path('', RedirectView.as_view(url='catalog-detail/', permanent=True)),
    path('products/<int:pk>/change/', views_product_ctrl.ChangeProduct.as_view(), name='product_change'),
    path('products/add-product/', views_product_ctrl.AddProduct.as_view(), name='product_form'),
    path('products/<int:pk>/view/', views_product_ctrl.ProductDisplay.as_view(), name='product_detail'),

]