from rest_framework import serializers
from ..models.catalog_model import Comment
from user_app.serializers.user_serializer import UserSerializer


class CommentRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        # fields = '__all__'
        fields = ['id', 'content', 'created_at', 'updated_at']