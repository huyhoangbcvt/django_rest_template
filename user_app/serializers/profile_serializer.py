from rest_framework import serializers
from ..models.account_model import Profile
from django.contrib.auth.models import User
from .user_serializer import UserSerializer, UserRegisterSerializer, CustomUserForeignKey
from ..modules.form_auth import RegistrationUserForm
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image', 'birthday', 'social_type']


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True,
        help_text='password',
        style={'input_type': 'password', 'placeholder': 'password'}
    )
    # re_password = serializers.CharField(
    #     required=True,
    #     help_text='password',
    #     style={'input_type': 'password', 'placeholder': 're password'}
    # )
    email = serializers.CharField(required=True, )
    # phone_number = serializers.CharField(source="profile.phone_number", required=False, )
    # birthday = serializers.DateField(source="profile.phone_number", required=False, )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email', 'first_name', 'last_name', ]
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }

    def create(self, validated_data):
        user = get_user_model()(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.select_related('user'))
    # user = UserSerializer(required=True)   # Note required=True
    # user = CustomUserForeignKey
    user = serializers.CharField(read_only=True, source="user.username")
    social_type = serializers.IntegerField(read_only=True, label="Loại tài khoản")

    class Meta:
        model = Profile
        # fields = '__all__'
        fields = ['image', 'birthday', 'social_type', 'phone_number', 'address', 'role', 'description', 'user']

    # def get_queryset(self):
    #     _id = self.request.user.id
    #     print(_id)
    #     user = UserSerializer(required=True,  queryset=Profile.objects.filter(id=_id))
    #     return user

    # Override
    # def create(self, validated_data):  # override
    #     profile = Profile(**validated_data)
    #     profile.set_password(validated_data['password'])
    #     profile.save()
    #     return profile

    # def create(self, validated_data):
    #     """
    #     Overriding the default create method of the Model serializer.
    #     :param validated_data: data containing all the details of student
    #     :return: returns a successfully created student record
    #     """
    #     user_data = validated_data.pop('user')
    #     user = UserSerializer.create(UserSerializer(), validated_data=user_data)
    #     profile, created = Profile.objects.update_or_create(user=user, phone_number=validated_data.pop('phone_number'))
    #     return profile
