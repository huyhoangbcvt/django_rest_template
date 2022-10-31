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

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (LoginView, LogoutView,
    PasswordChangeView, PasswordChangeDoneView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView,
)
from django.urls import path, reverse_lazy
from datetime import datetime, date
from user_app.modules import form_auth_ctrl, views_auth_ctrl

schema_view = get_schema_view(
    openapi.Info(
        title="Django-Training HDWebsoft",
        default_version="V-1.0",
        description="APIs for Django",
        contact=openapi.Contact(email="it.hoanghh@gmail.com"),
        license=openapi.License(name="Hà Huy Hoàng - HDWebsoft - %s" % datetime.now().year),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

from user_app.modules import views_auth
from rest_framework import routers, permissions
# router = routers.DefaultRouter()
# router.register('', views_auth.HomeViewSet)
from user_app.admin import admin_site

urlpatterns = [
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # =============| APIs |============
    path('__debug__/', include(debug_toolbar.urls)),
    # path('admin/', admin_site.urls),
    path('admin/', admin.site.urls),
    # path('', include(router.urls)),
    # =============| app endpoints |============
    # path('', views_auth.index_userapp, name='index'),
    path(r'user/', include("user_app.urls")),
    path(r'catalog/', include("catalog_app.urls")),
    path(r'upload/', include("upload_app.urls")),
    #
    re_path('^ckeditor/', include('ckeditor_uploader.urls')),
    re_path('^api/swagger(?P<format>\.json\.yaml)$', schema_view.with_ui(cache_timeout=0), name='schema-json'),
    re_path('^api/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    re_path('^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # =============| Web |============
    path(r'', views_auth_ctrl.index, name='index_admin'),
    path(r'login/', views_auth_ctrl.index_redirect_local, name='index_login'),

    path('user/password-reset/', PasswordResetView.as_view(
                title='Lấy lại mật khẩu',
                form_class = form_auth_ctrl.ResetPassToEmailForm,
                template_name='registration/password_reset_form_new.html',
                extra_context={'next':'/login/', 'crumbs': [('Trang chủ', reverse_lazy('index')), ('Đăng nhập', reverse_lazy('login')), ('Lấy lại mật khẩu', reverse_lazy('password_reset'))],'year':datetime.now().year},
                success_url='done/',
        ), name="password_reset"),
    path('user/password-reset/done/', PasswordResetDoneView.as_view(
                title='Gửi yêu cầu thành công. Vào email để lấy lại mật khẩu',
                template_name="registration/password_reset_done_new.html",
                extra_context={'next': '/login/', 'crumbs': [('Trang chủ', reverse_lazy('index')), ('Đăng nhập', reverse_lazy('login')), ('Gửi yêu cầu thành công. Vào email để lấy lại mật khẩu', reverse_lazy('password_reset_done'))],'year':datetime.now().year},
        ), name="password_reset_done"),
    #path('user/reset/<uidb64>/<token>/', ctrl_auth.PassResetView.as_view(), name="password_reset_confirm"),
    #Link được send vào mail
    path('user/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
                title='Đặt lại mật khẩu mới',
                form_class=form_auth_ctrl.ResetPassForm,
                template_name='registration/password_reset_confirm_new.html',
                extra_context={'next': '/login/', 'crumbs': [('Trang chủ', reverse_lazy('index')), ('Đăng nhập', reverse_lazy('login')), ('Đặt lại mật khẩu mới', reverse_lazy('password_reset_confirm'))],'year':datetime.now().year},
                success_url='/user/reset/done/',
        ), name="password_reset_confirm"),
    path('user/reset/done/', PasswordResetCompleteView.as_view(
                title='Đổi mật khẩu thành công',
                template_name="registration/password_reset_complete_new.html",
                extra_context={'next': '/login/', 'crumbs': [('Trang chủ', reverse_lazy('index')), ('Đăng nhập', reverse_lazy('login')), ('Đổi mật khẩu thành công', reverse_lazy('password_reset_complete'))],'year':datetime.now().year},
        ), name="password_reset_complete"),

]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
