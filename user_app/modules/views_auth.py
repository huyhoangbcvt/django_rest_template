from datetime import datetime
from django.shortcuts import render, resolve_url, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.views.generic import FormView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout

from rest_framework import status, views, viewsets, mixins, generics, permissions, renderers
# from rest_framework.views import View, APIView
# from rest_framework.generics import (GenericAPIView,
#     CreateAPIView, ListAPIView, RetrieveAPIView,
#     DestroyAPIView, UpdateAPIView, ListCreateAPIView,
#     RetrieveUpdateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
# )
# from rest_framework.viewsets import ModelViewSet

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, action, permission_classes

from ..serializers.user_serializer import UserSerializer, GroupSerializer, LoginSerializer
from ..serializers.profile_serializer import ProfileSerializer
from .form_auth import RegistrationUserForm, LoginForm
from ..models.account_model import Profile
from ..util import utilities


@api_view(['POST'])
@csrf_exempt
def register(request):
    form = RegistrationUserForm(request.data)
    if form.is_valid():
        user = form.save()
        # Refresh the database
        user.refresh_from_db()
        # Set role for created user
        user.profile.role = form.cleaned_data.get('role')
        # Get token for user
        token = utilities.generate_tokens(user)
        # return token to user
        return Response(token, status=status.HTTP_201_CREATED)

    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }, status=status.HTTP_200_OK)


class LoginAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"Token": token.key}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # authentication_classes = TokenAuthentication  # Token access
    permission_classes = [permissions.IsAuthenticated]  # Basic Auth
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-date_joined')
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'delete']
    # swagger_schema = None

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    # def filter_queryset(self, queryset):
    #     # queryset = self.queryset.filter(username=request.data.username)
    #     _id = self.request.user.id
    #     if _id:
    #         queryset = self.queryset.filter(id=_id)
    #         return queryset
    #     return self.queryset

    # def get_queryset(self):
    #     # username = self.request.query_params.get('username', None)
    #     username = self.request.user.username
    #     _id = self.request.user.id
    #     print('get_queryset', _id, username)
    #     queryset = self.queryset  # self.UserSerializer.Meta.User.objects.all()
    #     queryset = queryset.filter(id=_id)  # is_active=active
    #     return queryset

    # @action(methods=['GET'], detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    # @action(methods=['POST'], detail=True)
    # def add(self, request):
    #     # snippet = self.get_object()
    #     # return Response(snippet.highlighted)
    #     return register(request)


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # authentication_classes = TokenAuthentication  # Token access
    permission_classes = [permissions.IsAuthenticated]  # Basic Auth
    queryset = Profile.objects.all().order_by('created_at')
    serializer_class = ProfileSerializer
    http_method_names = ['get', 'put', 'patch', 'head']

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    # def get_queryset(self):
    #     _user = self.request.user
    #     print(_user.id)
    #     queryset = self.queryset.filter(user_id=_user.id)
    #     # query_set = Profile.objects.filter(profile__user_id=_user)
    #     return queryset

    # def filter_queryset(self, queryset):
    #     _user = self.request.user
    #     if _user:
    #         queryset = self.queryset.filter(user_id=_user.id)
    #         return queryset
    #     return self.queryset


class UserDetail(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]  # Basic Auth
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-date_joined')
    # swagger_schema = None


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    # authentication_classes = TokenAuthentication  # Token access
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'delete']

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    # def list(self, request, *args, **kwargs):
    #     serializer = GroupSerializer(Group.objects.all())
    #     return Response(serializer.data)

    # def get_extra_actions(self, request):
    #     return None


# class HomeViewSet(viewsets.ModelViewSet):
#     # status_code = 307
#     # permission_classes = [permissions.IsAuthenticated]
#     serializer_class = GroupSerializer
#     queryset = Group.objects.all()


# class LoginView(FormView):
#     """
#     Provides the ability to login as a user with a username and password
#     """
#     form_class = LoginForm  # AuthenticationForm
#     # redirect_field_name = REDIRECT_FIELD_NAME
#     template_name = 'login.html'
#     success_url = '/'  # reverse_lazy('user:index')
#     extra_context = {
#         'title': "Đăng nhập",
#         'year': datetime.now().year
#     }
#     authentication_form = None
#     redirect_authenticated_user = False


def index_userapp(request):
    print('User APIs: Run ok')
    # return redirect('user/')
    if request.user.is_authenticated:
        return HttpResponse('Webcome to HDWebshoft')
    return render(request, "index.html",
                  {
                      'title': "Index page",
                      # 'next':'/home/',
                      'content': "Example app page for Django.",
                      'year': datetime.now().year,
                      'design': "Hà Huy Hoàng"
                  }
                  )


def index(request):
    # profile = request.session.get('profile')
    # print("____: "+json.dumps(profile)+profile['first_name'] )
    print('User: Run ok')
    if request.user.is_authenticated:
        return HttpResponse('Webcome to HDWebshoft')
        # return redirect('user:home')

    return render(request, "index.html",
                  {
                      'title': "Index page",
                      # 'next':'/home/',
                      'content': "Example app page for Django.",
                      'year': datetime.now().year,
                      'design': "Hà Huy Hoàng"
                  }
            )