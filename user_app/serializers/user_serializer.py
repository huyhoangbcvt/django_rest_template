from abc import ABC

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User, Group
from rest_framework.authentication import authenticate
from ..models.account_model import Profile


class UserSerializer(serializers.ModelSerializer):  # serializers.HyperlinkedModelSerializer
    class Meta:
        model = User
        fields = '__all__'
        # fields = ['username', 'first_name', 'last_name', 'email']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        # fields = ['id', 'name']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validators(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        print(username)

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data


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
