"""django_api_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, re_path, include, reverse
from django.conf.urls import include
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Django-Training HDWebsoft",
        default_version="V-1.0",
        description="APIs for Django",
        contact=openapi.Contact(email="it.hoanghh@gmail.com"),
        license=openapi.License(name="Hà Huy Hoàng - HDWebsoft - 2022"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

from user_app.modules import views_auth
from rest_framework import routers, permissions

router = routers.DefaultRouter()
# router.register('', views_auth.HomeViewSet)

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    # =============| app endpoints |============
    # path('', views_auth.index_userapp, name='index'),
    path(r'user/', include("user_app.urls")),
    path(r'catalog/', include("catalog_app.urls")),

    re_path('^django/ckeditor/', include('ckeditor_uploader.urls')),
    re_path('^django/swagger(?P<format>\.json\.yaml)$', schema_view.with_ui(cache_timeout=0), name='schema-json'),
    re_path('^django/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    re_path('^django/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
