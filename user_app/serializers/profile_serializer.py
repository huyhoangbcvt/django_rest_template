from rest_framework import serializers
from ..models.account_model import Profile
from django.contrib.auth.models import User
from .user_serializer import UserSerializer, CustomUserForeignKey


class ProfileSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.select_related('user'))
    # print('vao', user)
    # user = UserSerializer(required=True)   # Note required=True
    # user = CustomUserForeignKey
    user = serializers.CharField(read_only=True, source="user.username")
    social_network = serializers.IntegerField(read_only=True, label="Loại tài khoản")

    class Meta:
        model = Profile
        # fields = '__all__'
        fields = ['images', 'birthday', 'social_network', 'phone_number', 'address', 'role', 'description', 'user']

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
