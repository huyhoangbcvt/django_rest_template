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
router.register(r'contacts', views_contact.ContactViewSet, basename="contact")
router.register(r'comments', views_comment.CommentViewSet, basename="comment")

urlpatterns = [
    # path('admin/', admin_site.urls),
    # =============| APIs |============
    path(r'api/', include(router.urls)),  # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Category
    # path(r"api/categories/", views_category.GetCategoryInfo, name="category_list"),
    # path(r"api/category/add/", views_category.AddCategory, name="category_add"),
    # path(r"api/category/create/", views_category.CreateCategory.as_view(), name="create_category"),
    # path(r'/api/category/view/<int:pk>/', None, name='category_detail'),
    # Product
    # path(r"/api/products/", views_product.GetProductInfo, name="product_list"),
    # path(r"api/product/add/", views_product.AddProduct, name="product_add"),
    # path(r"api/category/create/", views_product.CreateProduct.as_view(), name="create_product"),
    # path(r'api/category/view/<int:pk>/', None, name='product_detail'),

    # =============| Web |============
    # path('', views_catalog.index, name='index'),
    path('', views_catalog_ctrl.CatalogView.as_view(), name="catalog"),
    path('categories/', views_category_ctrl.category_list, name="categories"),

    path('categories/add-category/', views_category_ctrl.AddCategory.as_view(), name='upload_template'),
    path('categories/<int:pk>/change/', views_category_ctrl.ChangeCategory.as_view(), name='category_edit'),
    path('categories/view/<int:pk>/', views_category_ctrl.CategoryDisplay.as_view(), name='view_upload_template_page'),

    path('products/', views_product_ctrl.product_list, name="products"),
    # path('', RedirectView.as_view(url='catalog-detail/', permanent=True)),
    path('products/<int:pk>/change/', views_product_ctrl.ChangeProduct.as_view(), name='product_edit'),
    path('products/add-product/', views_product_ctrl.AddProduct.as_view(), name='upload_p_template'),
    path('products/view/<int:pk>/', views_product_ctrl.ProductDisplay.as_view(), name='view_upload_p_template_page'),

]