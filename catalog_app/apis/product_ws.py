from django.shortcuts import render
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin
from django.http import HttpResponse
# from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import json
from datetime import datetime
from django.db import transaction
from django.core import exceptions
from django.db.models import F
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAuthenticated

from user_app.models.account_model import Profile
from ..serializers.product_serializer import ProductSerializer, ProductAddSerializer
# from ..models.product_model import Product
from ..models.catalog_model import (Product, Category)


# Create your views here.
@permission_classes([IsAuthenticated])
def GetProductInfo(request):
    user = request.user
    # Get Product info from database # Product.objects.all()
    product_info = Product.objects.filter(user_id=user.id, active=True).order_by(F('created_at').desc(nulls_last=True))
    # Using Serializer to convert data
    # Set many=True to serializer queryset or list of objects instead of a single object instance, context={'request':request}
    product_serializer = ProductSerializer(product_info, many=True)
    return Response(product_serializer.data)


@permission_classes([IsAuthenticated])
def GetProductInfoDetail(request, pk):
    user = request.user
    # Get Product info from database # Product.objects.all()
    product_info = Product.objects.filter(id=pk, user_id=user.id, active=True).order_by(F('created_at').desc(nulls_last=True))
    # Using Serializer to convert data
    # Set many=True to serializer queryset or list of objects instead of a single object instance, context={'request':request}
    product_serializer = ProductSerializer(product_info, many=True)
    return Response(product_serializer.data)


@permission_classes([IsAuthenticated])
def UpdateProduct(request, pk):
    try:
        user = request.user
        # Get Category info from database # Category.objects.all()
        product_obj = Product.objects.get(id=pk, user_id=user.id, active=True)
        product_obj.active = False
        product_obj.save()
    except UpdateProduct.DoesNotExists:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(ProductSerializer(product_obj).data, status=status.HTTP_200_OK)


# @transaction.non_atomic_requests
@transaction.atomic
@permission_classes([IsAuthenticated])
def AddProduct(request):
    # Get data from post request
    data = request.data
    user = request.user
    # json_string = json.dumps(data)
    # print(json_string)
    # use Serializer to deserialize data
    serializer = ProductAddSerializer(data=data)
    # Check if validation is successful
    if serializer.is_valid():
        # Save the data to database
        try:
            product_save = serializer.save()
            # instance = Middleship(
            #     product_id=product_save.id,
            #     category_id=data['category']
            #     # date_joined=datetime.now
            # )
            # instance.save()
        except exceptions as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

