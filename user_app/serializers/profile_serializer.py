from rest_framework import serializers
from ..models.account_model import Profile
from .user_serializer import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(many=False, queryset=Profile.objects.select_related('user'))
    user = UserSerializer(required=True)   # Note required=True

    class Meta:
        model = Profile
        # fields = '__all__'
        fields = ['images', 'birthday', 'social_network', 'phone_number', 'address', 'role', 'description', 'user']

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
