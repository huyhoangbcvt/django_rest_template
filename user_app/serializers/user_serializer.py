from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.contrib.auth.models import User, Group
from rest_framework.authentication import authenticate
from ..models.account_model import Profile
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):  # serializers.HyperlinkedModelSerializer
    last_login = serializers.DateTimeField(read_only=True, format='%m-%d-%YT%H:%M:%S', label="Lần cuối đăng nhập")  # , style={'input_type':'hidden'}
    date_joined = serializers.DateTimeField(read_only=True, format='%m-%d-%YT%H:%M:%S', label="Ngày tham gia")
    is_active = serializers.BooleanField(read_only=True, label="Kích hoạt")

    class Meta:
        model = User
        # fields = '__all__'
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined', 'is_active', 'groups', 'user_permissions']
        # labels = {'last_login': _('Lần đăng nhập cuối'), 'date_joined': _('Ngày tham gia')}


class UserRegisterSerializer(serializers.ModelSerializer):  # serializers.HyperlinkedModelSerializer
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        # labels = {'last_login': _('Lần đăng nhập cuối'), 'date_joined': _('Ngày tham gia')}


class TokenUserSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['lifetime'] = int(refresh.access_token.lifetime.total_seconds())
        return data

    # password = serializers.CharField(
    #     write_only=True,
    #     required=True,
    #     help_text='password',
    #     style={'input_type': 'password', 'placeholder': 'Password'}
    # )
    #
    # class Meta:
    #     model = User
    #     fields = ['username', 'password']


class TokenRefreshUserSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return data


class CustomUserForeignKey(serializers.PrimaryKeyRelatedField):
    # def __init__(self, **kwargs):
    #     self.model = kwargs.pop('model')
    #     assert hasattr(self.model, 'owner')
    #     super().__init__(**kwargs)

    class Meta:
        model = User
        fields = '__all__'

    # def get_queryset(self):
    #     return User.objects.filter(username=self.request.user.username)
    #     # return User.objects.filter(user=self.context['request'].user)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        # fields = ['id', 'name']


class LoginSerializer(serializers.Serializer):
    # email = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )
    username = serializers.CharField(max_length=255)
    # password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data

    # class Meta:
    #     model = User
    #     fields = ['username', 'password', ]


# Custom Serializer for custom jwt
# noinspection PyAbstractClass
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Override get_token of TokenObtainPairSerializer
    @classmethod  # need to user this decorator to run MyTokenObtainPairSerializer.get_token(user=user) without error
    def get_token(cls, user):
        # Get token from TokenObtainPairSerializer
        token = super().get_token(user)
        # Adding role to token
        token['role'] = user.profile.role
        return token
