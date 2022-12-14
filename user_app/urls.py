from django.urls import path, re_path, include, reverse
from .modules import views_auth, views_auth_ctrl, form_auth_ctrl
from rest_framework import viewsets
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
)
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from datetime import datetime, date
app_name = 'user'

# If using routers to register ViewSet, it will see Binding ViewSets to urls explicitly
from rest_framework import routers
# router = routers.DefaultRouter(trailing_slash=False)
router = routers.DefaultRouter()
router.register(r'users', views_auth.UserViewSet, basename="users")
router.register(r'profiles', views_auth.ProfileViewSet, basename="profiles")
router.register(r'groups', views_auth.GroupViewSet, basename="user_groups")
router.register(r'token', views_auth.GetTokenViewSet, basename="token_access_obtaiwn")
router.register(r'refresh-token', views_auth.TokenRefreshViewSet, basename='token_refresh'),
router.register(r'sign-up', views_auth.SignupViewSet, basename="sign_up")
router.register(r'login', views_auth.LoginViewSet, basename="login_api")

# If not register ViewSet, it only to see urls detail
urlpatterns = [
    # =============| APIs |============
    path(r'api/', include(router.urls)),  # path('api/', include((router.urls, 'user_app'))),
    # path(r'api/token/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Để cấp mới access token với refresh token, ta thực hiện POST request
    # path(r'api/token/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    # path(r'api/sign-up/', views_auth.register, name='sign_up'),
    # path(r"api/login/", views_auth.CustomAuthToken.as_view(), name="login_api"),
    # =============| Web |============
    path('', views_auth_ctrl.index, name='index'),
    path('home/', views_auth_ctrl.Homepage.as_view(), name='home'),
    path('login/', views_auth_ctrl.LoginView.as_view(), name="login"),
    path('social/', views_auth_ctrl.index_redirect_social, name="social"),
    path('login-social', views_auth_ctrl.LoginSocialView.as_view(), name="login_social"),

    path('logout/', auth_views.LogoutView.as_view(
            # template_name="registration/logged_out.html",
            next_page=reverse_lazy('user:login'),  # next_page='/',
        ), name='logout'),
    path('sign-up/', views_auth_ctrl.RegistrationUser.as_view(), name='sign_up'),  # path('sign_up/', MySignUpView.as_view(), name='sign_up'),

    path('profile/', views_auth_ctrl.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views_auth_ctrl.EditUserProfileView.as_view(), name='profile_edit'),
    path('profile/<int:gu_id>/edit/', views_auth_ctrl.edit_profile_pk, name='profile_edit_pk'),

    path('password-change/', PasswordChangeView.as_view(
                title='Thay đổi mật khẩu',
                form_class=form_auth_ctrl.PassChangeForm,
                template_name='registration/password_change_form_accounts.html',
                extra_context={'next': reverse_lazy('user:password_change_done'), 'crumbs': [('Trang chủ', reverse_lazy('user:home')), ('Thông tin cá nhân', reverse_lazy('user:profile')), ('Thay đổi mật khẩu', reverse_lazy('user:password_change'))],'year':datetime.now().year},
                success_url='done/',
        ), name="password_change"),
    path('password-change/done/', PasswordChangeDoneView.as_view(
                title='Thay đổi mật khẩu thành công',
                template_name='registration/password_change_done_accounts.html',
                extra_context={'next': reverse_lazy('user:profile'), 'crumbs': [('Trang chủ', reverse_lazy('home')), ('Thông tin cá nhân', reverse_lazy('user:profile')), ('Thay đổi mật khẩu', reverse_lazy('user:password_change')), ('Thay đổi mật khẩu thành công', reverse_lazy('user:password_change_done'))],'year':datetime.now().year},
        ), name="password_change_done"),

]

# urlpatterns += router.urls
