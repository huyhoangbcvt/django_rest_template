from datetime import datetime
from django.shortcuts import render, resolve_url, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import login, logout
from rest_framework import generics, status, viewsets, status, viewsets, permissions, renderers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import api_view, action, permission_classes, authentication_classes, renderer_classes
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
# from django_filter import FilterSet
from ..apis import category_ws
from ..serializers.category_serializer import CategorySerializer
# from ..serializers.contact_serializer import ContactSerializer
# from ..models.category_model import Category
from ..models.catalog_model import (Product, Category)
from django.views.decorators.csrf import csrf_exempt
from ..util.pagination import BasePagination


# Neu dung ViewSet ko phai ModelViewSet thi phai tu lam GET, POST, DETAIL, PUT, PATH, DELETE
# class ContactViewSet(viewsets.ViewSet):
#     # authentication_classes = TokenAuthentication  # Token access
#     permission_classes = [IsAuthenticated]  # Basic Auth
#     queryset = Contact.objects.all().order_by('-date_joined')
#     serializer_class = ContactSerializer
#     # http_method_names = ['get', 'post', 'put', 'patch', 'head', 'delete']
#     # swagger_schema = None
#     charset = 'UTF-8'
#
#     def get_permissions(self):
#         if self.action == 'list':
#             return [permissions.AllowAny()]
#         return [permissions.IsAuthenticated()]
#
#     def list(self, request):  # GET
#         print('GET list')
#         queryset = Contact.objects.all().order_by('-date_joined')
#         serializer = ContactSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def create(self, request):  # POST
#         print('POST create')
#         return HttpResponse('POST create done')
#
#     def retrieve(self, request, pk=None):  # Detail  GET co param id
#         print('GET')
#         return HttpResponse('GET Detail done')
#
#     def update(self, request, pk=None):  # PUT
#         print('PUT')
#         return HttpResponse('PUT update done')
#
#     def partial_update(self, request, pk=None):  # PATH update 1 phan
#         print('PATH')
#         return HttpResponse('PATH partial_update 1 phan done')
#
#     def destroy(self, request, pk=None):  # Delete
#         print('DELETE')
#         return HttpResponse('DELETE destroy done')
#
#     # def post(self, request, *args, **kwargs):
#     #     print(self.request.data)
#     #     return self.create(request, *args, **kwargs)


# class CreateProfile(CreateModelMixin, GenericAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         # print(self.request.data)
#         # print(self.request.data.get("name"))
#         return self.create(request, *args, **kwargs)
#
#     # def perform_create(self, serializer):
#     #    _id = self.request.data.get('id')
#     #    comment = get_object_or_404(Profile, pk=_id)
#     #    print(comment)