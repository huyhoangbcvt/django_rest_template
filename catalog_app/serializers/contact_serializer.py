from django.db import models
from rest_framework import serializers
from ..models.catalog_model import Contact
from django.utils.translation import gettext_lazy as _


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        # fields = '__all__'
        fields = ['name', 'phone_number']
